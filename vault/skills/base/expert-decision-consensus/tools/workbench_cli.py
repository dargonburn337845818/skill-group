#!/usr/bin/env python3
"""workbench_cli.py — LightRead-like research/decision workbench for DSH.

Persistent project ledger + evidence + gates + memory + academic search,
so an agent can run a normalized expert-decision loop with real files.

Commands:
  init, status, search, verify, claim, decision, conflict, gate,
  memory, skill, next
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[3] / "research-workbench"
PROJECTS = BASE / "projects"

STAGES = [
    "0 brief",
    "1 evidence",
    "2 panel",
    "3 conflict",
    "4 adjudicate",
    "5 plan",
    "6 execute",
    "7 verify",
    "8 log-distill",
]

PHASE_TEMPLATE = """# {title}

> project: `{project_id}` · created {created} · updated {updated}

## 目标（Brief）
{goal}

## 非目标
{non_goals}

## 状态
- 当前阶段：{current_stage}
- 未决冲突：{unresolved}
- 已完成 gate：{gates_passed}

## 决策日志
{decisions}

## 待办/下一步
{next_actions}
"""


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def proj_dir(pid: str) -> Path:
    return PROJECTS / pid


def ensure_project(pid: str) -> dict:
    d = proj_dir(pid)
    if not (d / "ledger.json").exists():
        sys.exit(f"[error] project '{pid}' not found. Run: wb init {pid}")
    return json.loads((d / "ledger.json").read_text(encoding="utf-8"))


def save_ledger(pid: str, ledger: dict) -> None:
    d = proj_dir(pid)
    ledger["updated"] = now()
    (d / "ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    render_readme(pid, ledger)


def render_readme(pid: str, ledger: dict) -> None:
    d = proj_dir(pid)
    conflicts = ledger.get("conflicts", [])
    unresolved = [c["id"] for c in conflicts if c.get("resolution") in (None, "defer")]
    gates = [g for g in ledger.get("gates", []) if g.get("pass")]
    decisions = ledger.get("decisions", [])
    nexts = [x for x in ledger.get("next_actions", []) if not x.get("done")]
    pattern = ledger.get("brief", {})
    content = PHASE_TEMPLATE.format(
        title=pattern.get("title", pid),
        project_id=pid,
        created=ledger.get("created", now()),
        updated=ledger.get("updated", now()),
        goal=pattern.get("goal", "（待填写）"),
        non_goals="; ".join(pattern.get("non_goals", [])) or "（待填写）",
        current_stage=ledger.get("current_stage", "0 brief"),
        unresolved=", ".join(unresolved) if unresolved else "无",
        gates_passed=len(gates),
        decisions="\n".join(
            f"- [{x.get('resolution', '?')}] {x.get('decision', '')} （{x.get('adjudicator', '?')}）"
            for x in decisions
        ) or "（暂无）",
        next_actions="\n".join(f"- [{'x' if x.get('done') else ' '}] {x.get('text', '')}" for x in nexts) or "（暂无）",
    )
    (d / "README.md").write_text(content, encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    pid = args.project
    if proj_dir(pid).exists() and not args.force:
        print(f"[skip] project '{pid}' exists (use --force to re-init)")
        return 0
    d = proj_dir(pid)
    for sub in ["evidence", "decisions", "conflicts", "notes", "artifacts"]:
        (d / sub).mkdir(parents=True, exist_ok=True)
    ledger = {
        "id": pid,
        "title": args.title or args.project,
        "created": now(),
        "updated": now(),
        "current_stage": "0 brief",
        "brief": {"goal": "", "non_goals": []},
        "claims": [],
        "decisions": [],
        "conflicts": [],
        "gates": [],
        "next_actions": [],
        "memory": [],
        "rules": [],
        "artifacts": [],
    }
    (d / "ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "rules.md").write_text("# Rules\n\n（可填写项目级规则：引用纪律、交付物要求、风格偏好）\n", encoding="utf-8")
    (d / "memory.md").write_text("# Memory\n\n（项目记忆：跨会话保持的偏好、已决事项、待复核假设）\n", encoding="utf-8")
    render_readme(pid, ledger)
    print(f"[ok] initialised project '{pid}' at {d}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    if args.project:
        pids = [args.project]
    else:
        pids = sorted([p.name for p in PROJECTS.iterdir() if (p / "ledger.json").exists()]) if PROJECTS.exists() else []
    if not pids:
        print("[info] no projects yet. Run: wb init <project-id>")
        return 0
    for pid in pids:
        ledger = ensure_project(pid)
        conflicts = ledger.get("conflicts", [])
        unresolved = [c["id"] for c in conflicts if c.get("resolution") in (None, "defer")]
        gates = ledger.get("gates", [])
        passed = sum(1 for g in gates if g.get("pass"))
        print(f"{pid}: stage={ledger.get('current_stage')} gates={passed}/{len(gates)} "
              f"claims={len(ledger.get('claims', []))} decisions={len(ledger.get('decisions', []))} "
              f"conflicts={len(conflicts)} unresolved={len(unresolved)}")
        if args.verbose:
            for g in gates:
                mark = "PASS" if g.get("pass") else "FAIL"
                print(f"  [{mark}] {g.get('stage')} / {g.get('item')} — {g.get('evidence', '')}")
            for c in conflicts:
                res = c.get("resolution") or "defer"
                print(f"  [conflict] {c.get('id')} {res}: {c.get('topic', '')}")
    return 0


def http_get(url: str, timeout: int = 20) -> dict | list | None:
    req = urllib.request.Request(url, headers={"User-Agent": "dsh-workbench/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        print(f"[warn] request failed: {e}", file=sys.stderr)
        return None


def fetch_arxiv(query: str, limit: int) -> list[dict]:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": f"all:{query}", "max_results": limit, "sortBy": "relevance"})
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            xml = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[warn] arxiv failed: {e}", file=sys.stderr)
        return []
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    out = []
    for ent in entries:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.search(r"<title>(.*?)</title>", ent, re.S).group(1))).strip()
        link = re.search(r"<id>(.*?)</id>", ent, re.S)
        summary = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.search(r"<summary>(.*?)</summary>", ent, re.S).group(1))).strip()
        out.append({"title": title, "url": link.group(1).strip() if link else "", "abstract": summary[:500], "source": "arxiv"})
    return out[:limit]


def fetch_openalex(query: str, limit: int) -> list[dict]:
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": query, "per-page": min(limit, 50)})
    data = http_get(url)
    if not data:
        return []
    out = []
    for w in data.get("results", [])[:limit]:
        out.append({
            "title": w.get("display_name", ""),
            "url": w.get("doi") or w.get("id", ""),
            "abstract": (w.get("abstract_inverted_index") and " ".join(w["abstract_inverted_index"].keys())[:500] or ""),
            "source": "openalex",
            "doi": w.get("doi", ""),
            "year": w.get("publication_year"),
            "citations": w.get("cited_by_count"),
        })
    return out


def fetch_crossref(query: str, limit: int) -> list[dict]:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query": query, "rows": min(limit, 50)})
    data = http_get(url)
    if not data:
        return []
    out = []
    for it in data.get("message", {}).get("items", [])[:limit]:
        title = " ".join(it.get("title", [])) if it.get("title") else ""
        out.append({
            "title": title,
            "url": it.get("URL", ""),
            "doi": it.get("DOI", ""),
            "year": (it.get("issued", {}).get("date-parts", [[None]])[0][0]),
            "source": "crossref",
            "authors": [a.get("family", "") for a in it.get("author", [])][:5],
        })
    return out


def cmd_search(args: argparse.Namespace) -> int:
    sources = args.source.split(",") if args.source else ["all"]
    results = []
    if "all" in sources or "arxiv" in sources:
        results += fetch_arxiv(args.query, args.limit)
    if "all" in sources or "openalex" in sources:
        results += fetch_openalex(args.query, args.limit)
    if "all" in sources or "crossref" in sources:
        results += fetch_crossref(args.query, args.limit)
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.get('title', '')}")
        print(f"   [{r.get('source')}] {r.get('url', '')}")
        if r.get("abstract"):
            print(f"   {r['abstract'][:180]}")
    print(f"\n[info] {len(results)} results")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    query = args.identifier
    if query.startswith("10.") or query.startswith("doi:"):
        doi = query.replace("doi:", "").strip()
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
        data = http_get(url)
        if data and data.get("message"):
            m = data["message"]
            print(json.dumps({"verified": True, "doi": m.get("DOI"), "title": " ".join(m.get("title", [])),
                              "url": m.get("URL")}, ensure_ascii=False, indent=2))
            return 0
        print(json.dumps({"verified": False, "identifier": query}, ensure_ascii=False))
        return 0
    results = fetch_crossref(query, 3)
    if not results:
        print(json.dumps({"verified": False, "query": query}, ensure_ascii=False))
        return 0
    print(json.dumps({"verified": True, "query": query, "candidates": results}, ensure_ascii=False, indent=2))
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    cid = f"claim-{len(ledger['claims']) + 1:03d}"
    ledger["claims"].append({
        "id": cid,
        "text": args.text,
        "source": args.source or "",
        "tag": args.tag or "",
        "ts": now(),
    })
    save_ledger(args.project, ledger)
    print(f"[ok] added {cid} -> {ledger['id']}")
    return 0


def cmd_decision(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    did = f"dec-{len(ledger['decisions']) + 1:03d}"
    ledger["decisions"].append({
        "id": did,
        "decision": args.text,
        "resolution": args.resolution,
        "adjudicator": args.adjudicator,
        "conflicts": args.conflict or [],
        "ts": now(),
    })
    save_ledger(args.project, ledger)
    print(f"[ok] added {did}")
    return 0


def cmd_conflict(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    cid = f"conf-{len(ledger['conflicts']) + 1:03d}"
    ledger["conflicts"].append({
        "id": cid,
        "topic": args.topic,
        "claim_a": args.claim_a,
        "claim_b": args.claim_b,
        "resolution": None,
        "ts": now(),
    })
    save_ledger(args.project, ledger)
    print(f"[ok] added {cid}")
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    gates = ledger.setdefault("gates", [])
    g = {
        "id": f"gate-{len(gates) + 1:03d}",
        "stage": args.stage,
        "item": args.item,
        "pass": bool(args.pass_gate),
        "evidence": args.evidence or "",
        "ts": now(),
    }
    gates.append(g)
    if args.pass_gate:
        # auto-advance stage pointer if stage is lexically later
        current = ledger.get("current_stage", "0 brief")
        if args.stage > current:
            ledger["current_stage"] = args.stage
    save_ledger(args.project, ledger)
    print(f"[ok] gate {'PASS' if args.pass_gate else 'FAIL'} {args.stage} / {args.item}")
    return 0


def cmd_memory(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    if args.action == "add":
        ledger.setdefault("memory", []).append({"text": args.text, "ts": now()})
        save_ledger(args.project, ledger)
        print("[ok] memory added")
    elif args.action == "list":
        for i, m in enumerate(ledger.get("memory", []), 1):
            print(f"{i}. {m.get('text', '')}")
    elif args.action == "search":
        q = args.text.lower()
        hits = [m for m in ledger.get("memory", []) if q in m.get("text", "").lower()]
        if not hits:
            print("[info] no memory match")
        for m in hits:
            print(f"- {m.get('text', '')}")
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    nxt = [x for x in ledger.get("next_actions", []) if not x.get("done")]
    if not nxt:
        print("[info] no pending next actions")
        return 0
    for x in nxt:
        print(f"- {x.get('text', '')}")
    return 0


def cmd_brief(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    b = ledger.setdefault("brief", {"goal": "", "non_goals": []})
    if args.goal:
        b["goal"] = args.goal
    if args.non_goal:
        b.setdefault("non_goals", []).extend(args.non_goal)
    save_ledger(args.project, ledger)
    print(f"[ok] brief updated: goal={b.get('goal', '')!r} non_goals={b.get('non_goals', [])}")
    return 0


def cmd_todo(args: argparse.Namespace) -> int:
    ledger = ensure_project(args.project)
    todos = ledger.setdefault("next_actions", [])
    if args.action == "add":
        todos.append({"text": args.text or "", "done": False, "ts": now()})
        save_ledger(args.project, ledger)
        print("[ok] todo added")
    elif args.action == "done":
        hit = next((t for t in todos if t.get("text") == args.text), None)
        if hit is None:
            print("[warn] todo not found (exact text match required)")
        else:
            hit["done"] = True
            save_ledger(args.project, ledger)
            print("[ok] todo done")
    else:  # list
        for i, t in enumerate(todos, 1):
            mark = "x" if t.get("done") else " "
            print(f"{i}. [{mark}] {t.get('text', '')}")
    return 0


def cmd_skill(args: argparse.Namespace) -> int:
    print("Built-in workbench skills:")
    print("- paper-lookup      : arXiv/OpenAlex/Crossref 检索")
    print("- evidence-verify   : DOI/标题引用核验")
    print("- research-ledger   : 项目台账/claim/decision/conflict/gate")
    print("- project-memory    : 跨会话项目记忆")
    print("- nine-stage-loop   : 0 Brief → 8 Log & Distill")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wb", description="DSH research workbench CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="initialize a project")
    sp.add_argument("project")
    sp.add_argument("--title")
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("status", help="show project status")
    sp.add_argument("project", nargs="?")
    sp.add_argument("--verbose", action="store_true")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("search", help="search academic sources")
    sp.add_argument("query")
    sp.add_argument("--source", default="all", help="arxiv,openalex,crossref,all")
    sp.add_argument("--limit", type=int, default=8)
    sp.add_argument("--format", default="md", choices=["md", "json"])
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("verify", help="verify a DOI or title via Crossref")
    sp.add_argument("identifier")
    sp.set_defaults(func=cmd_verify)

    sp = sub.add_parser("claim", help="add an evidence-linked claim")
    sp.add_argument("project")
    sp.add_argument("text")
    sp.add_argument("--source")
    sp.add_argument("--tag")
    sp.set_defaults(func=cmd_claim)

    sp = sub.add_parser("decision", help="record a decision")
    sp.add_argument("project")
    sp.add_argument("text")
    sp.add_argument("--resolution", default="adopt_a", choices=["adopt_a", "adopt_b", "merge", "reject", "defer"])
    sp.add_argument("--adjudicator", default="user")
    sp.add_argument("--conflict", action="append")
    sp.set_defaults(func=cmd_decision)

    sp = sub.add_parser("conflict", help="record a conflict")
    sp.add_argument("project")
    sp.add_argument("--topic", required=True)
    sp.add_argument("--claim-a", required=True)
    sp.add_argument("--claim-b", required=True)
    sp.set_defaults(func=cmd_conflict)

    sp = sub.add_parser("gate", help="record a stage gate")
    sp.add_argument("project")
    sp.add_argument("--stage", required=True)
    sp.add_argument("--item", required=True)
    sp.add_argument("--pass-gate", dest="pass_gate", action="store_true")
    sp.add_argument("--evidence")
    sp.set_defaults(func=cmd_gate)

    sp = sub.add_parser("memory", help="project memory add/list/search")
    sp.add_argument("project")
    sp.add_argument("action", choices=["add", "list", "search"])
    sp.add_argument("text", nargs="?")
    sp.set_defaults(func=cmd_memory)

    sp = sub.add_parser("next", help="list pending next actions")
    sp.add_argument("project")
    sp.set_defaults(func=cmd_next)

    sp = sub.add_parser("brief", help="set brief goal / non-goals")
    sp.add_argument("project")
    sp.add_argument("--goal")
    sp.add_argument("--non-goal", action="append")
    sp.set_defaults(func=cmd_brief)

    sp = sub.add_parser("todo", help="project todo add/done/list")
    sp.add_argument("project")
    sp.add_argument("action", choices=["add", "done", "list"])
    sp.add_argument("text", nargs="?")
    sp.set_defaults(func=cmd_todo)

    sp = sub.add_parser("skill", help="list built-in workbench skills")
    sp.set_defaults(func=cmd_skill)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    PROJECTS.mkdir(parents=True, exist_ok=True)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
