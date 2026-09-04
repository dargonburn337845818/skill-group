#!/usr/bin/env python3
"""Run one capability-improvement -> validation cycle for core-iteration.

Improvement step (current automation level):
  - real/offline info gathering through info_source_cli.py
  - writes a normalized raw_corpus dump for later use

Validation step:
  - validate_contract.py   (contract fields)
  - behavior_test.py       (synthetic six-stage behavior)
  - smoke_test.py          (contract + behavior + scorecard together)

Usage:
  python3 tools/run_improve_validate.py [--offline]
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
OUTPUT = ROOT / "tools" / "output"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def gather(offline: bool, proxy: str | None = None, mode: str | None = None) -> dict:
    """Call all adapters (offline fixtures unless live network is desired)."""
    proxy_args = []
    if proxy:
        proxy_args += ["--proxy", proxy]
    if mode:
        proxy_args += ["--proxy-mode", mode]
    commands = [
        ("github", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github", "--query", "topic:rust stars:>100", "--limit", "3"]),
        ("osv", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["osv", "--package", "example-package", "--version", "1.0.0"]),
        ("pypi", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["pypi", "--package", "example-package"]),
        ("npm", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["npm", "--package", "example-npm-pkg"]),
        ("crates", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["crates", "--package", "example-crate"]),
        ("github-issues", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github-issues", "--query", "repo:rust-lang/rust bug", "--limit", "3"]),
        ("github-releases", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github-releases", "--repo", "rust-lang/rust", "--limit", "3"]),
        ("github-commits", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github-commits", "--repo", "rust-lang/rust", "--limit", "3"]),
        ("github-pr", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github-pr", "--query", "repo:rust-lang/rust type:pr state:open", "--limit", "3"]),
    ]
    if offline or os.environ.get("GITHUB_TOKEN"):
        commands.append(("github-code", [sys.executable, str(TOOLS / "info_source_cli.py")] + proxy_args + (["--offline"] if offline else []) + ["github-code", "--query", "repo:rust-lang/rust fn main", "--limit", "3"]))
    all_corpus = []
    scopes = []
    failures = []
    for source, cmd in commands:
        p = run(cmd)
        if p.returncode != 0:
            failures.append(source + ": " + ((p.stdout or "") + " " + (p.stderr or "")).strip())
            continue
        data = json.loads(p.stdout)
        all_corpus.extend(data.get("raw_corpus", []))
        scopes.append(data.get("source_scope_report", {}))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    dump = {
        "mode": "offline" if offline else "live",
        "raw_corpus_count": len(all_corpus),
        "raw_corpus": all_corpus,
        "source_scope_reports": scopes,
        "failures": failures,
    }
    (OUTPUT / "info_dump.json").write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
    return dump


def main() -> int:
    offline = "--offline" in sys.argv
    proxy = None
    mode = None
    if "--proxy" in sys.argv:
        idx = sys.argv.index("--proxy")
        if idx + 1 < len(sys.argv):
            proxy = sys.argv[idx + 1]
    if "--proxy-mode" in sys.argv:
        idx = sys.argv.index("--proxy-mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]
    print("== IMPROVE: gather info ==")
    dump = gather(offline, proxy, mode)
    print(f"  raw_corpus_count={dump['raw_corpus_count']} failures={dump['failures']}")

    print("== IMPROVE: live benefit-filter ==")
    bf = run([sys.executable, str(TOOLS / "benefit_filter_live.py"), "--input", str(OUTPUT / "info_dump.json")])
    try:
        bfdata = json.loads(bf.stdout)
        ys = bfdata["yield_stats"]
        print(f"  raw={ys['raw_count']} verified_single={ys['verified_single_count']} avg={ys['avg_density_score']} pending={ys['pending_count']}")
    except Exception:
        print(bf.stdout, bf.stderr)

    print("== IMPROVE: live distillation ==")
    dl = run([sys.executable, str(TOOLS / "distill_live.py"), "--input", str(OUTPUT / "info_dump.json")])
    try:
        dldata = json.loads(dl.stdout)
        ds = dldata["distillation_stats"]
        print(f"  nodes={ds['total_nodes']} with_boundary={ds['with_boundary']} avg_quality={ds['avg_quality']}")
    except Exception:
        print(dl.stdout, dl.stderr)

    print("== IMPROVE: live iterator ==")
    it = run([sys.executable, str(TOOLS / "iterator_live.py"), "--input", str(OUTPUT / "info_dump.json")])
    try:
        itdata = json.loads(it.stdout)
        print(f"  accepted={itdata['accepted']} effective_new={itdata['effective_new_count']} risk={itdata['risk_notes'][0][:60]}")
    except Exception:
        print(it.stdout, it.stderr)

    print("== IMPROVE: live validator ==")
    vl = run([sys.executable, str(TOOLS / "validator_live.py"), "--input", str(OUTPUT / "info_dump.json")])
    try:
        vldata = json.loads(vl.stdout)
        print(f"  decision={vldata['decision']} effective={vldata['benefit_summary']['effective_new_nodes']} rules={vldata['triggered_rules']}")
    except Exception:
        print(vl.stdout, vl.stderr)

    print("== IMPROVE: live forensics ==")
    fr = run([sys.executable, str(TOOLS / "forensics_live.py"), "--input", str(OUTPUT / "info_dump.json")])
    try:
        frdata = json.loads(fr.stdout)
        print(f"  root_cause={frdata['diagnosis']['root_cause']} action={frdata['diagnosis']['one_action'][:60]}")
    except Exception:
        print(fr.stdout, fr.stderr)

    print("== VALIDATE: contract ==")
    v = run([sys.executable, str(TOOLS / "validate_contract.py"), str(ROOT)])
    print(v.stdout.strip(), v.stderr.strip())

    print("== VALIDATE: behavior ==")
    b = run([sys.executable, str(TOOLS / "behavior_test.py")])
    print(b.stdout.strip(), b.stderr.strip())

    print("== VALIDATE: smoke ==")
    s = run([sys.executable, str(TOOLS / "smoke_test.py")])
    try:
        sdata = json.loads(s.stdout)
        print("  contract=", sdata.get("contract"), "scorecard=", sdata.get("scorecard_total"), "/", len(sdata.get("per_skill", {}))*20)
    except Exception:
        print(s.stdout, s.stderr)

    ok = v.returncode == 0 and b.returncode == 0 and s.returncode == 0
    print("== CYCLE RESULT ==", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
