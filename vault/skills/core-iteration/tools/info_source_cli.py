#!/usr/bin/env python3
"""Real info-source calling CLI for the core-iteration meta-capability.

This is the executable layer behind `info-source-adapter`. It calls public
APIs (GitHub REST, OSV, PyPI, npm, crates.io) and normalizes the results into
the `raw_corpus` / `source_scope_report` contract used by
web-research-consensus and benefit-filter.

Real network is used by default. For sandbox/offline testing, pass `--offline`
to read deterministic fixtures from tools/fixtures/ -- the output shape is the
same as a live call.

Examples:
  python3 tools/info_source_cli.py github --query "topic:rust stars:>100" --limit 5
  python3 tools/info_source_cli.py osv --package requests --version 2.31.0
  python3 tools/info_source_cli.py pypi --package requests
  python3 tools/info_source_cli.py npm --package typescript
  python3 tools/info_source_cli.py --offline github --query "demo"
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = TOOLS_DIR / "fixtures"
USER_AGENT = "dsh-core-iteration/0.1 (+https://github.com/dsh-skill-vault)"

# Watt host-proxy mode: (host, port) used for direct --resolve HTTPS calls
CURL_HOST_PROXY: tuple[str, int] | None = None


def is_wsl() -> bool:
    return "microsoft" in Path("/proc/version").read_text(errors="ignore").lower() or bool(os.environ.get("WSL_DISTRO_NAME"))


def detect_windows_host_ip() -> str:
    """In WSL, Windows host is usually the default gateway; otherwise localhost."""
    if is_wsl() and shutil.which("ip"):
        try:
            out = subprocess.check_output(["ip", "route"], text=True, errors="ignore", timeout=3)
            m = re.search(r"default via ([\d.]+)", out)
            if m:
                return m.group(1)
        except Exception:
            pass
    return "127.0.0.1"


def fetch_json_via_curl(url: str, timeout: int = 15, token: str | None = None) -> dict:
    """Fetch JSON through Watt host proxy using curl --resolve (not CONNECT)."""
    global CURL_HOST_PROXY
    if not CURL_HOST_PROXY:
        raise RuntimeError("host proxy not configured")
    host, port = CURL_HOST_PROXY
    parsed = urllib.parse.urlparse(url)
    target_host = parsed.hostname or ""
    target_port = parsed.port or (443 if parsed.scheme == "https" else 80)
    cmd = ["curl", "-s", "-L", "--max-time", str(timeout), "-k",
           "--resolve", f"{target_host}:{target_port}:{host}", "-H", f"Host: {target_host}"]
    if token:
        cmd += ["-H", f"Authorization: Bearer {token}"]
    cmd += [url]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    if proc.returncode != 0:
        raise urllib.error.URLError(f"curl failed: {proc.stderr.strip()}")
    if not proc.stdout.strip() or not proc.stdout.lstrip().startswith(("{", "[")):
        raise urllib.error.URLError(
            f"host proxy did not return JSON for {target_host} (may not be accelerated): {proc.stdout.strip()[:200]}"
        )
    return json.loads(proc.stdout)


def post_json_via_curl(url: str, payload: dict, timeout: int = 15) -> dict:
    global CURL_HOST_PROXY
    if not CURL_HOST_PROXY:
        raise RuntimeError("host proxy not configured")
    host, port = CURL_HOST_PROXY
    parsed = urllib.parse.urlparse(url)
    target_host = parsed.hostname or ""
    target_port = parsed.port or (443 if parsed.scheme == "https" else 80)
    cmd = ["curl", "-s", "-L", "--max-time", str(timeout), "-k",
           "--resolve", f"{target_host}:{target_port}:{host}",
           "-X", "POST", "-H", "Content-Type: application/json",
           "-d", json.dumps(payload, ensure_ascii=False), url]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    if proc.returncode != 0:
        raise urllib.error.URLError(f"curl failed: {proc.stderr.strip()}")
    if not proc.stdout.strip() or not proc.stdout.lstrip().startswith(("{", "[")):
        raise urllib.error.URLError(
            f"host proxy did not return JSON (may not be accelerated): {proc.stdout.strip()[:200]}"
        )
    return json.loads(proc.stdout)


def fetch_json(url: str, timeout: int = 15, token: str | None = None) -> dict:
    if CURL_HOST_PROXY:
        return fetch_json_via_curl(url, timeout=timeout, token=token)
    headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_fixture(name: str) -> dict:
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"fixture missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_source_scope(source_meta: list[dict], failures: list[str], degradation: list[str]) -> dict:
    return {
        "sources_queried": source_meta,
        "total_candidates": sum(int(s.get("results", 0)) for s in source_meta),
        "failures": failures,
        "degradation": degradation,
        "coverage_notes": "offline fixture" if degradation and any("offline" in d for d in degradation) else "live API",
    }


def search_github(query: str, limit: int, offline: bool, token: str | None) -> dict:
    if offline:
        data = load_fixture("github_search.json")
    else:
        if token:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&per_page={limit}"
        else:
            # unauthenticated search is allowed at low rate for repositories
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&per_page={limit}"
        data = fetch_json(url, token=token)
    items = data.get("items", [])[:limit]
    corpus = []
    for it in items:
        url = it.get("html_url", "")
        stars = it.get("stargazers_count", 0)
        forks = it.get("forks_count", 0)
        meta = {
            "stars": stars,
            "forks": forks,
            "language": it.get("language"),
            "topics": it.get("topics", []),
            "license": (it.get("license") or {}).get("spdx_id"),
            "created_at": it.get("created_at"),
            "pushed_at": it.get("pushed_at"),
            "open_issues": it.get("open_issues_count"),
            "archived": it.get("archived", False),
            "default_branch": it.get("default_branch"),
        }
        corpus.append({
            "chunk_id": f"github_repo_{it.get('id', url)}",
            "text": (it.get("description") or it.get("name") or "") + f" [repo: {url}]",
            "source": {
                "type": "github",
                "url": url,
                "title": it.get("full_name", ""),
                "author": (it.get("owner") or {}).get("login", ""),
                "publisher": "GitHub",
                "date": it.get("updated_at", ""),
                "evidence_rank": "repo-metadata",
            },
            "claim": it.get("description") or "",
            "gap_id": None,
            "metadata": meta,
            "popularity_signals": {
                "stars": stars,
                "forks": forks,
                "note": "stars/forks are popularity signals, NOT evidence"
            }
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github", "endpoint": "/search/repositories", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def search_github_issues(query: str, limit: int, offline: bool, token: str | None) -> dict:
    if offline:
        data = load_fixture("github_issues.json")
    else:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page={limit}"
        data = fetch_json(url, token=token)
    items = data.get("items", [])[:limit]
    corpus = []
    for it in items:
        corpus.append({
            "chunk_id": f"github_issue_{it.get('id', it.get('html_url', ''))}",
            "text": (it.get("title") or "") + "\n" + (it.get("body") or "")[:1000],
            "source": {
                "type": "github_issue",
                "url": it.get("html_url", ""),
                "title": it.get("title", ""),
                "author": (it.get("user") or {}).get("login", ""),
                "publisher": "GitHub Issues",
                "date": it.get("created_at", ""),
                "evidence_rank": "issue-thread",
            },
            "claim": it.get("title", ""),
            "gap_id": None,
            "metadata": {
                "state": it.get("state"),
                "comments": it.get("comments"),
                "labels": [l.get("name") for l in it.get("labels", [])],
                "created_at": it.get("created_at"),
                "updated_at": it.get("updated_at"),
                "closed_at": it.get("closed_at"),
            },
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github_issue", "endpoint": "/search/issues", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def list_github_releases(repo: str, limit: int, offline: bool) -> dict:
    if offline:
        data = load_fixture("github_releases.json")
    else:
        url = f"https://api.github.com/repos/{urllib.parse.quote(repo)}/releases?per_page={limit}"
        data = fetch_json(url)
    corpus = []
    for it in data[:limit]:
        tag = it.get("tag_name", "")
        url = it.get("html_url", "")
        corpus.append({
            "chunk_id": f"github_release_{it.get('id', tag)}",
            "text": (it.get("name") or tag or "") + "\n" + (it.get("body") or "")[:1000],
            "source": {
                "type": "github_release",
                "url": url,
                "title": it.get("name") or tag,
                "author": (it.get("author") or {}).get("login", ""),
                "publisher": "GitHub Releases",
                "date": it.get("published_at", ""),
                "evidence_rank": "release-notes",
            },
            "claim": it.get("name") or tag,
            "gap_id": None,
            "metadata": {
                "tag_name": tag,
                "prerelease": it.get("prerelease", False),
                "draft": it.get("draft", False),
                "published_at": it.get("published_at"),
                "created_at": it.get("created_at"),
                "assets_count": len(it.get("assets", [])),
            },
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github_release", "endpoint": f"/repos/{repo}/releases", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def search_github_code(query: str, limit: int, offline: bool, token: str | None) -> dict:
    if not token and not offline:
        raise RuntimeError("GitHub code search requires GITHUB_TOKEN")
    if offline:
        data = load_fixture("github_code.json")
    else:
        url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}&per_page={limit}"
        data = fetch_json(url, token=token)
    items = data.get("items", [])[:limit]
    corpus = []
    for it in items:
        repo = it.get("repository", {}).get("full_name", "")
        path = it.get("path", "")
        url = it.get("html_url", "") or f"https://github.com/{repo}/blob/{it.get('sha','')}/{path}"
        corpus.append({
            "chunk_id": f"github_code_{repo}_{path}",
            "text": f"File: {path} in {repo}" + ("\n" + (it.get("text_match") or "") if it.get("text_match") else ""),
            "source": {
                "type": "github_code",
                "url": url,
                "title": f"{repo}:{path}",
                "author": "",
                "publisher": "GitHub Code Search",
                "date": "",
                "evidence_rank": "code-fragment",
            },
            "claim": f"Code found in {repo} at {path}",
            "gap_id": None,
            "metadata": {
                "repo": repo,
                "path": path,
                "sha": it.get("sha"),
                "language": it.get("language"),
            },
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github_code", "endpoint": "/search/code", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def list_github_commits(repo: str, limit: int, offline: bool) -> dict:
    if offline:
        data = load_fixture("github_commits.json")
    else:
        url = f"https://api.github.com/repos/{urllib.parse.quote(repo)}/commits?per_page={limit}"
        data = fetch_json(url)
    corpus = []
    for it in data[:limit]:
        sha = it.get("sha", "")
        commit = it.get("commit", {})
        author = it.get("author") or {}
        message = commit.get("message", "")
        url = it.get("html_url", f"https://github.com/{repo}/commit/{sha}")
        corpus.append({
            "chunk_id": f"github_commit_{sha}",
            "text": message[:1000],
            "source": {
                "type": "github_commit",
                "url": url,
                "title": sha[:12],
                "author": author.get("login") or (commit.get("author") or {}).get("name", ""),
                "publisher": "GitHub Commits",
                "date": (commit.get("author") or {}).get("date", ""),
                "evidence_rank": "commit-history",
            },
            "claim": message.splitlines()[0] if message else sha,
            "gap_id": None,
            "metadata": {
                "sha": sha,
                "author_name": (commit.get("author") or {}).get("name"),
                "author_login": author.get("login"),
                "date": (commit.get("author") or {}).get("date"),
                "message": message[:500],
            },
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github_commit", "endpoint": f"/repos/{repo}/commits", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def search_github_prs(query: str, limit: int, offline: bool, token: str | None) -> dict:
    if offline:
        data = load_fixture("github_prs.json")
    else:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page={limit}"
        data = fetch_json(url, token=token)
    items = data.get("items", [])[:limit]
    corpus = []
    for it in items:
        pr = it.get("pull_request") or {}
        corpus.append({
            "chunk_id": f"github_pr_{it.get('id', it.get('html_url', ''))}",
            "text": (it.get("title") or "") + "\n" + (it.get("body") or "")[:1000],
            "source": {
                "type": "github_pr",
                "url": it.get("html_url", ""),
                "title": it.get("title", ""),
                "author": (it.get("user") or {}).get("login", ""),
                "publisher": "GitHub PR",
                "date": it.get("created_at", ""),
                "evidence_rank": "pr-thread",
            },
            "claim": it.get("title", ""),
            "gap_id": None,
            "metadata": {
                "state": it.get("state"),
                "comments": it.get("comments"),
                "labels": [l.get("name") for l in it.get("labels", [])],
                "created_at": it.get("created_at"),
                "updated_at": it.get("updated_at"),
                "pr_url": pr.get("html_url"),
                "pr_merged_at": pr.get("merged_at"),
            },
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "github_pr", "endpoint": "/search/issues?type=pr", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def osv_query(package: str, version: str | None, offline: bool) -> dict:
    if offline:
        data = load_fixture("osv.json")
    else:
        body = {"package": {"name": package}, "version": version} if version else {"package": {"name": package}}
        if CURL_HOST_PROXY:
            data = post_json_via_curl("https://api.osv.dev/v1/query", body)
        else:
            req = urllib.request.Request(
                "https://api.osv.dev/v1/query",
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
    vulns = data.get("vulns", [])
    corpus = []
    for v in vulns[:10]:
        vuln_id = v.get("id", "")
        url = f"https://osv.dev/vulnerability/{vuln_id}"
        summary = v.get("summary") or v.get("details") or ""
        corpus.append({
            "chunk_id": f"osv_{vuln_id}",
            "text": summary + f" [source: {url}, package: {package}]",
            "source": {"type": "osv", "url": url, "title": vuln_id, "author": "OSV", "publisher": "OSV", "date": v.get("published", ""), "evidence_rank": "advisory"},
            "claim": summary,
            "gap_id": None,
        })
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "osv", "endpoint": "https://api.osv.dev/v1/query", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def pypi_query(package: str, offline: bool) -> dict:
    if offline:
        data = load_fixture("pypi.json")
    else:
        data = fetch_json(f"https://pypi.org/pypi/{urllib.parse.quote(package)}/json")
    info = data.get("info", {})
    ver = data.get("info", {}).get("version", "")
    url = info.get("project_url", f"https://pypi.org/project/{package}/")
    corpus = [{
        "chunk_id": f"pypi_{package}_{ver}",
        "text": (info.get("summary") or "") + f" [package: {package}@{ver}, source: {url}]",
        "source": {"type": "package_registry", "url": url, "title": package, "author": info.get("author", ""), "publisher": "PyPI", "date": info.get("upload_time") or info.get("release_time") or "", "evidence_rank": "registry-metadata"},
        "claim": info.get("summary") or "",
        "gap_id": None,
    }]
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "package_registry", "endpoint": "PyPI JSON API", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def npm_query(package: str, offline: bool) -> dict:
    if offline:
        data = load_fixture("npm.json")
    else:
        data = fetch_json(f"https://registry.npmjs.org/{urllib.parse.quote(package)}")
    latest = data.get("dist-tags", {}).get("latest", "")
    version = (data.get("versions") or {}).get(latest, {})
    url = f"https://www.npmjs.com/package/{package}"
    corpus = [{
        "chunk_id": f"npm_{package}_{latest}",
        "text": (version.get("description") or "") + f" [package: {package}@{latest}, source: {url}]",
        "source": {"type": "package_registry", "url": url, "title": package, "author": (version.get("author") or {}).get("name", ""), "publisher": "npm", "date": version.get("time", ""), "evidence_rank": "registry-metadata"},
        "claim": version.get("description") or "",
        "gap_id": None,
    }]
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "package_registry", "endpoint": "npm registry", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def crates_query(package: str, offline: bool) -> dict:
    if offline:
        data = load_fixture("crates.json")
    else:
        data = fetch_json(f"https://crates.io/api/v1/crates/{urllib.parse.quote(package)}")
    crate = data.get("crate", {})
    url = crate.get("homepage") or crate.get("repository") or f"https://crates.io/crates/{package}"
    corpus = [{
        "chunk_id": f"crates_{package}_{crate.get('max_version', '')}",
        "text": (crate.get("description") or "") + f" [crate: {package}, source: {url}]",
        "source": {"type": "package_registry", "url": url, "title": package, "author": crate.get("repository", ""), "publisher": "crates.io", "date": crate.get("updated_at", ""), "evidence_rank": "registry-metadata"},
        "claim": crate.get("description") or "",
        "gap_id": None,
    }]
    return {
        "raw_corpus": corpus,
        "source_scope_report": normalize_source_scope(
            [{"type": "package_registry", "endpoint": "crates.io API", "queries": 1, "results": len(corpus), "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }


def detect_system_proxy() -> str | None:
    """Detect Windows/Watt system proxy from registry."""
    env_proxy = os.environ.get("WATT_PROXY")
    if env_proxy:
        return env_proxy if "://" in env_proxy else "http://" + env_proxy
    if shutil.which("reg.exe"):
        try:
            out = subprocess.check_output(
                ["reg.exe", "query", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "/v", "ProxyServer"],
                text=True, errors="ignore", timeout=5,
            )
            m = re.search(r"(?:https?://)?(\d{1,3}(?:\.\d{1,3}){3}:\d{2,5})", out)
            if m:
                return "http://" + m.group(1)
        except Exception:
            pass
    return None


def detect_watt_ports() -> list[int]:
    """Find ports listened by Steam++/Watt Toolkit via tasklist+netstat."""
    try:
        tasklist = subprocess.check_output(["tasklist.exe", "/FO", "CSV", "/NH"], text=True, errors="ignore", timeout=5)
        pid = None
        for line in tasklist.splitlines():
            m = re.search(r'"(?:Steam\+\+|Watt Toolkit)\.exe","(\d+)"', line)
            if m:
                pid = m.group(1)
                break
        if not pid:
            return []
        netstat = subprocess.check_output(["netstat.exe", "-ano"], text=True, errors="ignore", timeout=5)
        ports = set()
        for line in netstat.splitlines():
            if pid in line and "LISTENING" in line:
                m = re.search(r"127\.0\.0\.1:(\d+)", line) or re.search(r"0\.0\.0\.0:(\d+)", line) or re.search(r"\[::1\]:(\d+)", line)
                if m:
                    ports.add(int(m.group(1)))
        return sorted(ports)
    except Exception:
        return []


def detect_host_proxy() -> str | None:
    """Host-proxy mode uses Watt Toolkit's local reverse-proxy ports (80/443).

    On WSL the Windows host is reached via the default gateway, not 127.0.0.1.
    """
    ports = detect_watt_ports()
    if 443 in ports:
        return f"http://{detect_windows_host_ip()}:443"
    if 80 in ports:
        return f"http://{detect_windows_host_ip()}:80"
    return None


def detect_all_proxies() -> dict:
    system = detect_system_proxy()
    host = detect_host_proxy()
    return {
        "system": system,
        "host": host,
        "watt_ports": detect_watt_ports(),
        "selected_default": host or system,
    }


def select_proxy(mode: str | None) -> str | None:
    mode = mode or os.environ.get("WATT_PROXY_MODE") or "auto"
    if mode == "none":
        return None
    if mode == "system":
        return detect_system_proxy()
    if mode == "host":
        return detect_host_proxy()
    # auto: prefer host mode (user's stated preference, avoids WSL breakage)
    return detect_host_proxy() or detect_system_proxy()



def fetch_github_file(repo: str, path: str, offline: bool, token: str | None) -> dict:
    """Fetch a single GitHub file (docs/source/config) via Contents API.

    This closes the gap between “we know a repo has a doc” and “we actually
    have the document text in raw_corpus”, especially for authoring guides and
    best-practices references.
    """
    if offline:
        return {
            "raw_corpus": [],
            "source_scope_report": normalize_source_scope(
                [{"type": "github_file", "endpoint": f"/repos/{repo}/contents/{path}", "queries": 0, "results": 0, "failures": ["no offline fixture for github-file"]}],
                ["github-file offline unsupported, use live or a custom fixture"],
                ["offline fixture used"],
            ),
        }
    url = f"https://api.github.com/repos/{urllib.parse.quote(repo)}/contents/{urllib.parse.quote(path)}"
    data = fetch_json(url, token=token)
    if isinstance(data, list):
        # Directory listing: keep it as a scope note instead of synthesizing text.
        names = [x.get("name") for x in data]
        return {
            "raw_corpus": [],
            "source_scope_report": normalize_source_scope(
                [{"type": "github_file", "endpoint": f"/repos/{repo}/contents/{path}", "queries": 1, "results": len(names), "failures": []}],
                [],
                ["directory listing only; pass a file path to fetch text"],
            ),
        }
    content_b64 = data.get("content", "")
    try:
        text = base64.b64decode(content_b64).decode("utf-8", errors="replace")
    except Exception:
        text = ""
    html_url = data.get("html_url") or f"https://github.com/{repo}/blob/{data.get('sha','')}/{path}"
    item = {
        "chunk_id": f"github_file_{repo}_{path}",
        "text": text[:20000],
        "source": {
            "type": "github_file",
            "url": html_url,
            "title": f"{repo}:{path}",
            "author": repo.split("/")[0],
            "publisher": "GitHub Contents API",
            "date": "",
            "evidence_rank": "docs-file" if path.lower().endswith((".md", ".mdx", ".rst", ".txt")) else "code-fragment",
        },
        "claim": f"文件 {path} @ {repo}",
        "gap_id": None,
        "metadata": {
            "repo": repo,
            "path": path,
            "sha": data.get("sha"),
            "size": data.get("size"),
            "type": data.get("type"),
        },
        "evidence_class": "static",
    }
    return {
        "raw_corpus": [item] if text else [],
        "source_scope_report": normalize_source_scope(
            [{"type": "github_file", "endpoint": f"/repos/{repo}/contents/{path}", "queries": 1, "results": 1 if text else 0, "failures": []}],
            [],
            [] if not offline else ["offline fixture used"],
        ),
    }



def main() -> int:

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="use fixtures instead of live network")
    parser.add_argument("--proxy", default=None, help="HTTP/SOCKS proxy URL, e.g. http://127.0.0.1:7890")
    parser.add_argument("--proxy-mode", choices=["auto", "host", "system", "none"], default=None, help="proxy selection mode (default auto = host first)")
    parser.add_argument("--host-proxy", default=None, help="Watt host-proxy address, e.g. 172.30.160.1:443 (default: auto-detect Windows host IP)")
    parser.add_argument("--detect-proxy", action="store_true", help="print detected Watt/Windows proxy and exit")
    sub = parser.add_subparsers(dest="source", required=False)

    gh = sub.add_parser("github", help="GitHub repository search")
    gh.add_argument("--query", required=True)

    osv = sub.add_parser("osv", help="OSV vulnerability query")
    osv.add_argument("--package", required=True)
    osv.add_argument("--version", default=None)

    pypi = sub.add_parser("pypi", help="PyPI package metadata")
    pypi.add_argument("--package", required=True)

    npm = sub.add_parser("npm", help="npm package metadata")
    npm.add_argument("--package", required=True)

    crates = sub.add_parser("crates", help="crates.io package metadata")
    crates.add_argument("--package", required=True)

    ghi = sub.add_parser("github-issues", help="GitHub issue/PR search")
    ghi.add_argument("--query", required=True)

    ghr = sub.add_parser("github-releases", help="GitHub releases for a repo")
    ghr.add_argument("--repo", required=True)

    ghc = sub.add_parser("github-code", help="GitHub code search (requires GITHUB_TOKEN)")
    ghc.add_argument("--query", required=True)

    ghf = sub.add_parser("github-file", help="Fetch a single GitHub file (docs/source/config) via Contents API")
    ghf.add_argument("--repo", required=True)
    ghf.add_argument("--path", required=True)

    ghm = sub.add_parser("github-commits", help="GitHub commit history for a repo")
    ghm.add_argument("--repo", required=True)

    ghp = sub.add_parser("github-pr", help="GitHub PR search")
    ghp.add_argument("--query", required=True)

    for sp in (gh, osv, pypi, npm, crates, ghi, ghr, ghc, ghf, ghm, ghp):
        sp.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    offline = args.offline
    if args.detect_proxy:
        info = detect_all_proxies()
        info["selected"] = select_proxy(args.proxy_mode)
        print(json.dumps(info, ensure_ascii=False))
        return 0
    if not args.proxy and not offline:
        mode = args.proxy_mode or os.environ.get("WATT_PROXY_MODE") or "auto"
        use_host = mode == "host" or (mode == "auto" and detect_host_proxy() is not None)
        if use_host:
            # Host mode: use direct HTTPS to the Watt reverse proxy via curl --resolve.
            global CURL_HOST_PROXY
            if args.host_proxy:
                if ":" in args.host_proxy:
                    hp, port_s = args.host_proxy.rsplit(":", 1)
                    port = int(port_s)
                else:
                    hp, port = args.host_proxy, 443
            else:
                hp, port = detect_windows_host_ip(), 443
            CURL_HOST_PROXY = (hp, port)
            print(f"# using Watt host proxy via --resolve: {hp}:{port}", file=sys.stderr)
        elif mode == "system":
            args.proxy = detect_system_proxy()
            if args.proxy:
                print(f"# using detected system proxy: {args.proxy}", file=sys.stderr)
        elif mode != "none":
            args.proxy = select_proxy(mode)
            if args.proxy:
                print(f"# using detected proxy ({mode}): {args.proxy}", file=sys.stderr)
    if args.proxy:
        os.environ["HTTP_PROXY"] = args.proxy
        os.environ["HTTPS_PROXY"] = args.proxy
        os.environ["ALL_PROXY"] = args.proxy

    if args.source is None:
        parser.error("a source is required (github/osv/pypi/npm/crates)")

    try:
        if args.source == "github":
            result = search_github(args.query, args.limit, offline, token)
        elif args.source == "osv":
            result = osv_query(args.package, args.version, offline)
        elif args.source == "pypi":
            result = pypi_query(args.package, offline)
        elif args.source == "npm":
            result = npm_query(args.package, offline)
        elif args.source == "crates":
            result = crates_query(args.package, offline)
        elif args.source == "github-issues":
            result = search_github_issues(args.query, args.limit, offline, token)
        elif args.source == "github-releases":
            result = list_github_releases(args.repo, args.limit, offline)
        elif args.source == "github-code":
            result = search_github_code(args.query, args.limit, offline, token)
        elif args.source == "github-file":
            result = fetch_github_file(args.repo, args.path, offline, token)
        elif args.source == "github-commits":
            result = list_github_commits(args.repo, args.limit, offline)
        elif args.source == "github-pr":
            result = search_github_prs(args.query, args.limit, offline, token)
        else:
            parser.error("unknown source")
    except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError) as exc:
        if offline:
            raise
        print(json.dumps({"error": f"network failure: {exc}", "hint": "use --offline for sandbox testing"}, ensure_ascii=False))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
