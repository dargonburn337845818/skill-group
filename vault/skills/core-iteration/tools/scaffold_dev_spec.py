#!/usr/bin/env python3
"""Scaffold a development spec + path handbook (开发底座的可执行层).

Writes two files into a project directory:

  dev_spec.md       # Frame / Interview / Plan / Spec / Review / Gate / Build / Verify
  path_handbook.md  # 模块地图 + 公开接口 + 测试命令 + 约束 + 未完事项

Usage:
  python3 tools/scaffold_dev_spec.py --project /path/to/project --entry src/index.ts \
    --module "core: 模块核心" --module "api: 对外接口" --test "npm test"
"""
import argparse
import json
from pathlib import Path


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--entry", default="src/index.ts", help="公开入口文件/命令")
    parser.add_argument("--module", action="append", default=[], help="模块地图条目 <name>: <职责>")
    parser.add_argument("--api", action="append", default=[], help="公开接口 <name>|<输入>|<输出>")
    parser.add_argument("--test", default="", help="测试命令")
    parser.add_argument("--out-name", default="dev_spec.md")
    args = parser.parse_args()

    modules = []
    for m in args.module:
        if ":" in m:
            name, desc = m.split(":", 1)
            modules.append((name.strip(), desc.strip()))
        else:
            modules.append((m.strip(), ""))
    apis = [a.split("|") for a in args.api]

    spec = f"""# 开发规格单（Dev Spec）

## Frame / 北极星

- 为谁：
- 处境：
- 可观测结果：
- 非目标：

## Interview / 关键取舍

- [ ] 已确认接口形状
- [ ] 已确认错误策略
- [ ] 已确认配置默认值
- [ ] 已确认兼容范围

## Plan / 模块地图

| 模块 | 职责 | 公开接口 | 测试入口 |
|---|---|---|---|
"""
    for name, desc in modules:
        spec += f"| {name} | {desc} | 待补 | {args.test or '待补'} |\n"
    spec += f"""
## Spec / 验收

- spec：
- accept：
- do：self / subagent / workflow / daemon / mixed
- verify：self / subagent / redteam / dual / workflow

## Adversarial Review

- [ ] BLOCKER：
- [ ] GAP：
- [ ] NOTE：
- [ ] 已跑六项检查（范围/接口/错误/边界/可观测/安全）

## Gate

- [ ] 规格齐全
- [ ] 无未决 BLOCKER
- [ ] 进入执行

## Verify

- [ ] 测试通过公开接口
- [ ] 关键检查见过变红（prove-it-can-fail）
- [ ] 无 in-flight 验证

## DoD / 终验

- [ ] 测试通过
- [ ] 真实启动/冒烟
- [ ] 证据可回溯
- [ ] 无未处理边界
"""

    handbook = f"""# 路径手册（Path Handbook）

```text
project: {args.project}
entry: {args.entry}
module_map:
"""
    for name, desc in modules:
        handbook += f"  - {name} : {desc} : <公开接口>\n"
    handbook += "public_api:\n"
    for api in apis:
        if len(api) == 3:
            handbook += f"  - {api[0]} : 输入={api[1]} / 输出={api[2]}\n"
        elif len(api) == 1:
            handbook += f"  - {api[0]} : 输入=待定 / 输出=待定\n"
    handbook += f"""tests: {args.test or '<待补>'}
constraints: <跨模块/环境/安全约束>
next_steps: <尚未解决的边界或待续工作>
```
"""

    project = Path(args.project).resolve()
    spec_path = project / (args.out_name if args.out_name.endswith(".md") else args.out_name + ".md")
    handbook_path = project / "path_handbook.md"
    write_file(spec_path, spec)
    write_file(handbook_path, handbook)
    result = {
        "ok": True,
        "project": str(project),
        "spec": str(spec_path),
        "handbook": str(handbook_path),
        "modules": [n for n, _ in modules],
        "apis": len(apis),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
