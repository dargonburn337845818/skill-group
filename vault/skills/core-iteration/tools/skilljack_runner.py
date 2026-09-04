#!/usr/bin/env python3
"""Real Skill A/B runner for skilljack-evals style task packages.

This runner executes scaffolded eval tasks against a real LLM (DeepSeek by
default) using a minimal agent loop with `loadSkill` / `read_file` /
`write_file` / `bash` tools. It measures:

  - skill discovery     (did the model actually call loadSkill?)
  - deterministic pass  (verifier exit or marker/file checks)
  - output quality      (optional LLM judge, --judge)
  - efficiency          (number of assistant turns, lower is better)

It supports two inputs:
  1. `--task-dir` — a scaffold_eval_task.py package:
       task.md + environment/skills/<skill>/SKILL.md + verifier/verify.mjs
  2. `--tasks-yaml` — a skilljack-evals `tasks.yaml` file.

Output is a `skill_effect_bench.py`-compatible JSON (task metrics with
`*_without` / `*_with`) when `--mode both`, plus a detailed per-run report.

Usage:
  python3 tools/skilljack_runner.py --task-dir evals/demo --mode both --runs 3
  python3 tools/skilljack_runner.py --tasks-yaml evals/demo/tasks.yaml --mode both --runs 3 --output bench.json
  python3 tools/skilljack_runner.py --task-dir evals/demo --mode with-skill --judge
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

DEFAULT_API_BASE = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


# ---------------------------------------------------------------------------
# credentials / API
# ---------------------------------------------------------------------------

def load_deepseek_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    cred_path = Path.home() / ".dsh" / ".credentials.yaml"
    if cred_path.exists() and yaml is not None:
        try:
            data = yaml.safe_load(cred_path.read_text(encoding="utf-8")) or {}
            key = str((data.get("refs") or {}).get("DEEPSEEK_API_KEY", "")).strip()
        except Exception:
            key = ""
    if not key:
        raise SystemExit("DEEPSEEK_API_KEY not found (env or ~/.dsh/.credentials.yaml)")
    return key


def chat_completion(
    api_key: str,
    api_base: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: Optional[list[dict[str, Any]]] = None,
    temperature: float = 0.2,
    max_tokens: int = 4096,
    timeout: int = 120,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return {}, text
    raw = m.group(1).strip()
    body = m.group(2).strip()
    try:
        fm = json.loads(raw)
    except Exception:
        fm = {}
        for line in raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm, body


def parse_task_dir(task_dir: Path) -> dict[str, Any]:
    task_md = task_dir / "task.md"
    if not task_md.exists():
        raise SystemExit(f"task.md not found: {task_md}")
    fm, prompt = parse_frontmatter(task_md.read_text(encoding="utf-8"))
    task_id = str(fm.get("id") or task_dir.name)
    expected_skill = str(fm.get("expected_skill") or fm.get("skill") or "")
    if expected_skill == "none":
        expected_skill = ""
    checks = fm.get("checks") or []
    assertions = fm.get("assertions") or []
    deterministic: dict[str, Any] = {
        "expect_skill_activation": bool(fm.get("expect_skill_invocation", True))
        if expected_skill
        else False,
        "markers": [],
        "files": [],
        "expect_no_tool_calls": [],
    }
    for c in checks:
        text = str(c)
        if text.startswith("contains:"):
            deterministic["markers"].append(text.split(":", 1)[1])
        elif text.startswith("files:"):
            deterministic["files"].append(text.split(":", 1)[1])
    skill_dir = task_dir / "environment" / "skills" / (expected_skill or "skill")
    verifier = task_dir / "verifier" / "verify.mjs"
    workspace = task_dir / "environment" / "workspace"
    return {
        "id": task_id,
        "prompt": prompt,
        "expected_skill": expected_skill,
        "checks": checks,
        "assertions": assertions,
        "deterministic": deterministic,
        "skill_dir": skill_dir if skill_dir.exists() else None,
        "verifier": verifier if verifier.exists() else None,
        "workspace": workspace if workspace.exists() else None,
        "source": "scaffold",
    }


def parse_tasks_yaml(path: Path) -> list[dict[str, Any]]:
    if yaml is None:
        raise SystemExit("PyYAML is required for --tasks-yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    skill_name = str(data.get("skill") or "skill")
    defaults = data.get("defaults") or {}
    tasks = []
    for t in data.get("tasks", []):
        expected = str(t.get("expected_skill_load") or defaults.get("expected_skill_load") or skill_name)
        if expected == "none":
            expected = ""
        det = t.get("deterministic") or {}
        deterministic = {
            "expect_skill_activation": bool(det.get("expect_skill_activation", True))
            if expected
            else False,
            "markers": [det["expect_marker"]] if det.get("expect_marker") else [],
            "files": [],
            "expect_no_tool_calls": det.get("expect_no_tool_calls", []),
            "expect_tool_calls": det.get("expect_tool_calls", []),
        }
        tasks.append({
            "id": str(t.get("id") or f"task-{len(tasks) + 1}"),
            "prompt": str(t.get("prompt") or ""),
            "expected_skill": expected,
            "checks": [],
            "assertions": t.get("golden_checklist", []),
            "deterministic": deterministic,
            "skill_dir": None,
            "verifier": None,
            "workspace": None,
            "source": "yaml",
            "criteria": t.get("criteria") or defaults.get("criteria") or {},
        })
    return tasks


# ---------------------------------------------------------------------------
# agent loop
# ---------------------------------------------------------------------------

def strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    return text[m.end():] if m else text


def build_skill_catalog(skill_dir: Path) -> list[dict[str, Any]]:
    """Return [{name, path, description}] for a skills directory."""
    if not skill_dir or not skill_dir.exists():
        return []
    skills: list[dict[str, Any]] = []
    if (skill_dir / "SKILL.md").exists():
        skills.append({"name": skill_dir.name, "path": skill_dir, "description": ""})
    for child in sorted(skill_dir.iterdir()):
        if child.is_dir() and (child / "SKILL.md").exists():
            skills.append({"name": child.name, "path": child, "description": ""})
    # Fill descriptions from frontmatter when available.
    for s in skills:
        text = (s["path"] / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^description:\s*(.+)$", text, re.M)
        if m:
            s["description"] = m.group(1).strip()
    return skills


def tool_schema() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "loadSkill",
                "description": "Load a skill to get specialized instructions",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file inside the task workspace",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["file_path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file inside the task workspace",
                "parameters": {
                    "type": "object",
                    "properties": {"file_path": {"type": "string"}},
                    "required": ["file_path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "bash",
                "description": "Run a shell command in the task workspace",
                "parameters": {
                    "type": "object",
                    "properties": {"command": {"type": "string"}},
                    "required": ["command"],
                },
            },
        },
    ]


def safe_path(workdir: Path, rel: str) -> Path:
    p = Path(rel)
    if not p.is_absolute():
        p = workdir / p
    p = p.resolve()
    workdir_resolved = workdir.resolve()
    if not str(p).startswith(str(workdir_resolved)):
        raise ValueError(f"path outside workspace: {rel}")
    return p


class AgentSession:
    def __init__(
        self,
        api_key: str,
        api_base: str,
        model: str,
        workdir: Path,
        skills: list[dict[str, Any]],
        with_skill: bool,
        max_steps: int = 20,
        timeout_ms: int = 300000,
    ) -> None:
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.workdir = workdir
        self.skills = skills
        self.with_skill = with_skill
        self.max_steps = max_steps
        self.timeout_ms = timeout_ms
        self.skill_loads: list[str] = []
        self.tool_calls: list[dict[str, Any]] = []
        self.turns = 0
        self.messages: list[dict[str, Any]] = []

    def build_system(self) -> str:
        if not self.with_skill or not self.skills:
            return "You are a helpful AI assistant. Complete the user's request directly."
        lines = ["You are a helpful AI assistant. Available skills:", ""]
        for s in self.skills:
            lines.append(f"- {s['name']}: {s['description'] or '(no description)'}")
        lines += [
            "",
            "Use the `loadSkill` tool only when the user's request clearly falls into a listed skill's domain.",
            "Do not load a skill for unrelated or generic tasks.",
            "After loading a skill, follow its instructions.",
        ]
        return "\n".join(lines)

    def execute_tool(self, name: str, args: dict[str, Any]) -> Any:
        if name == "loadSkill":
            target = str(args.get("name", "")).strip().lower()
            for s in self.skills:
                if s["name"].lower() == target:
                    body = strip_frontmatter((s["path"] / "SKILL.md").read_text(encoding="utf-8"))
                    self.skill_loads.append(s["name"])
                    return {"skill": s["name"], "content": body}
            return {"error": f"Skill not found: {target}"}
        if name == "write_file":
            try:
                p = safe_path(self.workdir, str(args.get("file_path", "output.txt")))
            except ValueError as e:
                return {"error": str(e)}
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(str(args.get("content", "")), encoding="utf-8")
            return {"written": str(p)}
        if name == "read_file":
            try:
                p = safe_path(self.workdir, str(args.get("file_path", "")))
            except ValueError as e:
                return {"error": str(e)}
            if not p.exists():
                return {"error": f"File not found: {p}"}
            return {"content": p.read_text(encoding="utf-8", errors="ignore")[:50000]}
        if name == "bash":
            try:
                proc = subprocess.run(
                    str(args.get("command", "")),
                    shell=True,
                    cwd=str(self.workdir),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return {"stdout": proc.stdout[:10000], "stderr": proc.stderr[:10000], "code": proc.returncode}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Unknown tool: {name}"}

    def run(self, prompt: str) -> dict[str, Any]:
        start = time.time()
        self.messages = [
            {"role": "system", "content": self.build_system()},
            {"role": "user", "content": prompt},
        ]
        tools = tool_schema() if self.with_skill else [t for t in tool_schema() if t["function"]["name"] in ("write_file", "read_file", "bash")]
        output = ""
        deadline = time.time() + self.timeout_ms / 1000.0
        for _ in range(self.max_steps):
            if time.time() > deadline:
                break
            try:
                msg = chat_completion(self.api_key, self.api_base, self.model, self.messages, tools=tools)
            except Exception as e:
                return {
                    "output": output,
                    "is_error": True,
                    "error": str(e),
                    "duration_ms": int((time.time() - start) * 1000),
                    "turns": self.turns,
                    "skill_loads": list(self.skill_loads),
                    "tool_calls": list(self.tool_calls),
                }
            self.turns += 1
            tool_calls = msg.get("tool_calls")
            if tool_calls:
                self.messages.append({
                    "role": "assistant",
                    "content": msg.get("content") or "",
                    "tool_calls": tool_calls,
                })
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    try:
                        args = json.loads(fn.get("arguments") or "{}")
                    except Exception:
                        args = {}
                    result = self.execute_tool(name, args)
                    self.tool_calls.append({
                        "tool": name,
                        "toolUseId": tc.get("id", ""),
                        "input": args,
                        "timestamp": int(time.time() * 1000),
                    })
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc.get("id", ""),
                        "content": json.dumps(result, ensure_ascii=False),
                    })
                continue
            output = str(msg.get("content") or "")
            self.messages.append({"role": "assistant", "content": output})
            break
        # Always persist the final text so verifiers can read it.
        (self.workdir / "output.txt").write_text(output, encoding="utf-8")
        return {
            "output": output,
            "is_error": False,
            "error": "",
            "duration_ms": int((time.time() - start) * 1000),
            "turns": self.turns,
            "skill_loads": list(self.skill_loads),
            "tool_calls": list(self.tool_calls),
        }


# ---------------------------------------------------------------------------
# scoring
# ---------------------------------------------------------------------------

def evaluate_deterministic(task: dict[str, Any], result: dict[str, Any], workdir: Path) -> dict[str, Any]:
    det = task.get("deterministic", {})
    markers = det.get("markers", [])
    files = det.get("files", [])
    expected_activation = bool(det.get("expect_skill_activation", False)) and bool(task.get("expected_skill"))
    skill_loads = [x.lower() for x in result.get("skill_loads", [])]
    expected_name = str(task.get("expected_skill") or "").lower()
    activated = any(expected_name and (expected_name in s or s in expected_name) for s in skill_loads)
    detail: list[str] = []
    if det.get("expect_skill_activation") is not None:
        detail.append(f"skill_activation expected={bool(det['expect_skill_activation'])} actual={activated}")
    for marker in markers:
        found = marker in result.get("output", "")
        detail.append(f"marker '{marker}' found={found}")
        if not found:
            return {"passed": False, "skill_activated": activated, "details": detail}
    for fname in files:
        p = workdir / fname
        exists = p.exists()
        detail.append(f"file '{fname}' exists={exists}")
        if not exists:
            return {"passed": False, "skill_activated": activated, "details": detail}
    if det.get("expect_no_tool_calls"):
        bad = [t for t in det["expect_no_tool_calls"] if any(tc["tool"] == t for tc in result["tool_calls"])]
        if bad:
            detail.append(f"unexpected tool calls: {bad}")
            return {"passed": False, "skill_activated": activated, "details": detail}
    if det.get("expect_tool_calls"):
        missing = [t for t in det["expect_tool_calls"] if not any(tc["tool"] == t for tc in result["tool_calls"])]
        if missing:
            detail.append(f"missing tool calls: {missing}")
            return {"passed": False, "skill_activated": activated, "details": detail}
    # Anti-trigger: a skill must NOT be loaded.
    if not expected_activation and skill_loads:
        detail.append(f"false positive: loaded {skill_loads}")
        return {"passed": False, "skill_activated": True, "details": detail}
    return {"passed": True, "skill_activated": activated, "details": detail}


def run_verifier(verifier: Optional[Path], workdir: Path, result: dict[str, Any]) -> dict[str, Any]:
    if not verifier:
        return {"ran": False, "returncode": None, "passed": None, "output": "", "reward": None}
    env = os.environ.copy()
    env["SKILLJACK_OUTPUT_FILE"] = str(workdir / "output.txt")
    env["SKILLJACK_TRAJECTORY_FILE"] = str(workdir / "trajectory.json")
    env["SKILLJACK_REWARD_FILE"] = str(workdir / "reward.txt")
    try:
        proc = subprocess.run(
            ["node", str(verifier)],
            cwd=str(workdir),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        reward = None
        rf = workdir / "reward.txt"
        if rf.exists():
            try:
                reward = float(rf.read_text(encoding="utf-8").strip())
            except Exception:
                reward = None
        verifier_output = (proc.stdout + proc.stderr).strip()
        # A verifier that crashes (ESM/require errors, syntax errors, missing
        # modules) is not an authoritative FAIL; let deterministic checks decide.
        runtime_error = any(x in verifier_output for x in (
            "ReferenceError", "SyntaxError", "Cannot use import",
            "require is not defined", "ERR_MODULE_NOT_FOUND", "Error:",
        ))
        passed = None if runtime_error and proc.returncode != 0 else proc.returncode == 0
        return {
            "ran": True,
            "returncode": proc.returncode,
            "passed": passed,
            "output": verifier_output,
            "reward": reward,
        }
    except Exception as e:
        return {"ran": True, "returncode": None, "passed": False, "output": str(e), "reward": None}


def judge_result(
    api_key: str,
    api_base: str,
    model: str,
    task: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    prompt = str(task.get("prompt", ""))
    output = str(result.get("output", ""))
    system = (
        "You are a strict skill evaluation judge. Score the agent output.\n"
        "Return ONLY a JSON object: {\"quality\":0-100,\"adherence\":0-100,\"discovery\":0-100,\"reasoning\":\"...\"}.\n"
        "quality = output quality, adherence = followed expected skill/instructions, "
        "discovery = 100 if the agent discovered/loaded the expected skill, otherwise 0."
    )
    user = (
        f"Task: {prompt}\n\nExpected skill: {task.get('expected_skill') or 'none'}\n\n"
        f"Skill loads: {result.get('skill_loads', [])}\n\nAgent output:\n{output[:6000]}\n\n"
        "Judge now."
    )
    try:
        msg = chat_completion(
            api_key, api_base, model,
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            max_tokens=500,
        )
        text = str(msg.get("content") or "")
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            return {"quality": 0, "adherence": 0, "discovery": 0, "reasoning": text[:200]}
        data = json.loads(m.group(0))
        return {
            "quality": max(0, min(100, int(float(data.get("quality", 0))))),
            "adherence": max(0, min(100, int(float(data.get("adherence", 0))))),
            "discovery": max(0, min(100, int(float(data.get("discovery", 0))))),
            "reasoning": str(data.get("reasoning", ""))[:300],
        }
    except Exception as e:
        return {"quality": 0, "adherence": 0, "discovery": 0, "reasoning": f"judge error: {e}"}


def run_single_task(
    task: dict[str, Any],
    api_key: str,
    api_base: str,
    model: str,
    skill_dir: Optional[Path],
    with_skill: bool,
    runs: int,
    use_judge: bool,
    max_steps: int,
    timeout_ms: int,
) -> dict[str, Any]:
    # Resolve skills: prefer task package environment, then explicit --skill-dir.
    skills_path: Optional[Path] = task.get("skill_dir")
    if skills_path is None:
        skills_path = skill_dir
    skills = build_skill_catalog(skills_path) if with_skill else []
    run_details = []
    for i in range(max(1, runs)):
        workdir = Path(tempfile.mkdtemp(prefix=f"skilljack-{task['id']}-"))
        try:
            ws = task.get("workspace")
            if ws and ws.exists():
                for f in ws.iterdir():
                    target = workdir / f.name
                    if f.is_dir():
                        shutil.copytree(f, target, dirs_exist_ok=True)
                    else:
                        shutil.copy2(f, target)
            session = AgentSession(
                api_key=api_key,
                api_base=api_base,
                model=model,
                workdir=workdir,
                skills=skills,
                with_skill=with_skill,
                max_steps=max_steps,
                timeout_ms=timeout_ms,
            )
            result = session.run(task["prompt"])
            det = evaluate_deterministic(task, result, workdir)
            ver = run_verifier(task.get("verifier"), workdir, result)
            # Verifier is authoritative when the task has concrete deterministic
            # requirements. Anti-trigger-only tasks have no marker/file checks,
            # so the placeholder SUCCESS_MARKER verifier must not fail them.
            det_config = task.get("deterministic", {})
            has_explicit_checks = bool(
                task.get("checks")
                or det_config.get("markers")
                or det_config.get("files")
                or det_config.get("expect_tool_calls")
                or det_config.get("expect_no_tool_calls")
            )
            if ver["ran"] and ver["passed"] is not None and has_explicit_checks:
                det["passed"] = ver["passed"]
                det["details"].append(f"verifier rc={ver['returncode']}")
            judge = judge_result(api_key, api_base, model, task, result) if use_judge else None
            run_details.append({
                "run": i + 1,
                "result": result,
                "deterministic": det,
                "verifier": ver,
                "judge": judge,
            })
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    # Aggregate.
    passed = [r["deterministic"]["passed"] for r in run_details]
    activated = [bool(r["result"].get("skill_loads")) for r in run_details]
    turns = [r["result"].get("turns", 0) for r in run_details]
    durations = [r["result"].get("duration_ms", 0) for r in run_details]
    quality = [r["judge"]["quality"] for r in run_details if r["judge"]]
    adherence = [r["judge"]["adherence"] for r in run_details if r["judge"]]
    discovery = [r["judge"]["discovery"] for r in run_details if r["judge"]]

    def mean(xs: list[float]) -> Optional[float]:
        return round(sum(xs) / len(xs), 3) if xs else None

    return {
        "id": task["id"],
        "expected_skill": task.get("expected_skill", ""),
        "runs": len(run_details),
        "success_rate": round(sum(passed) / len(passed), 3) if passed else 0.0,
        "skill_activation_rate": round(sum(activated) / len(activated), 3) if activated else 0.0,
        "avg_turns": mean(turns),
        "avg_duration_ms": mean(durations),
        "avg_quality": mean(quality),
        "avg_adherence": mean(adherence),
        "avg_discovery": mean(discovery),
        "run_details": run_details,
    }


def task_metrics(with_meta: dict[str, Any], without_meta: dict[str, Any], use_judge: bool) -> dict[str, Any]:
    row: dict[str, Any] = {"id": with_meta["id"], "expected_skill": with_meta.get("expected_skill", "")}
    row["success_without"] = without_meta["success_rate"]
    row["success_with"] = with_meta["success_rate"]
    row["coverage_without"] = without_meta["skill_activation_rate"]
    row["coverage_with"] = with_meta["skill_activation_rate"]
    row["efficiency_without"] = without_meta["avg_turns"] or 0
    row["efficiency_with"] = with_meta["avg_turns"] or 0
    if use_judge:
        row["quality_without"] = without_meta["avg_quality"] or 0
        row["quality_with"] = with_meta["avg_quality"] or 0
        row["calibration_without"] = without_meta["avg_discovery"] / 100.0
        row["calibration_with"] = with_meta["avg_discovery"] / 100.0
    return row


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-dir", help="scaffold_eval_task.py package directory")
    parser.add_argument("--tasks-yaml", help="skilljack-evals tasks.yaml path")
    parser.add_argument("--skill-dir", help="explicit skills directory (fallback)")
    parser.add_argument("--mode", choices=["no-skill", "with-skill", "both"], default="both")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default=os.environ.get("EVAL_AGENT_MODEL", DEFAULT_MODEL))
    parser.add_argument("--judge-model", default=os.environ.get("EVAL_JUDGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--api-base", default=os.environ.get("EVAL_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--judge", action="store_true", help="run LLM judge (extra API calls)")
    parser.add_argument("--max-steps", type=int, default=20)
    parser.add_argument("--timeout-ms", type=int, default=300000)
    parser.add_argument("--output", help="output JSON path (default stdout)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not args.task_dir and not args.tasks_yaml:
        raise SystemExit("one of --task-dir / --tasks-yaml is required")
    tasks: list[dict[str, Any]]
    if args.tasks_yaml:
        tasks = parse_tasks_yaml(Path(args.tasks_yaml).resolve())
    else:
        tasks = [parse_task_dir(Path(args.task_dir).resolve())]

    api_key = load_deepseek_key()
    skill_dir = Path(args.skill_dir).resolve() if args.skill_dir else None

    modes = ["no-skill", "with-skill"] if args.mode == "both" else [args.mode]
    per_task: dict[str, dict[str, Any]] = {}
    detail: dict[str, Any] = {"model": args.model, "api_base": args.api_base, "tasks": []}
    for task in tasks:
        task_entry: dict[str, Any] = {"id": task["id"]}
        for mode in modes:
            meta = run_single_task(
                task=task,
                api_key=api_key,
                api_base=args.api_base,
                model=args.model,
                skill_dir=skill_dir,
                with_skill=(mode == "with-skill"),
                runs=args.runs,
                use_judge=args.judge,
                max_steps=args.max_steps,
                timeout_ms=args.timeout_ms,
            )
            task_entry[mode] = meta
            if args.verbose:
                print(f"  [{task['id']} / {mode}] success={meta['success_rate']} activation={meta['skill_activation_rate']} turns={meta['avg_turns']}", flush=True)
        if args.mode == "both":
            task_entry["bench"] = task_metrics(
                task_entry["with-skill"], task_entry["no-skill"], use_judge=args.judge
            )
        detail["tasks"].append(task_entry)

    if args.mode == "both":
        rows = [t["bench"] for t in detail["tasks"]]
        result = {
            "skill": tasks[0].get("expected_skill") or Path(args.task_dir or args.tasks_yaml or "").name,
            "model": args.model,
            "judge_model": args.judge_model,
            "judged": args.judge,
            "runs": args.runs,
            "generated_by": "skilljack_runner.py",
            "tasks": rows,
            "details": detail,
        }
    else:
        result = {"mode": args.mode, "model": args.model, "tasks": detail["tasks"]}

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
