#!/usr/bin/env python3
"""领域识别器 + 人名专家库 + 专家缺口分支（共享底座）。

用途
----
从用户自然语言自动识别 domain_id（算法 / 前端 / 后端 / 安全 / 性能 / 数学 /
物理 / 写作等），然后按该领域 expert_ids 从 EXPERT_LIBRARY.json 加载“具体人名
专家团”。若该领域没有 ready 的人名专家，默认返回 use_llm_directly（不弹窗）；
未识别到领域时同样默认继续，不打断用户。

数据
----
- vault/meta/domain-profiles.json  —— 领域字典 + expert_ids + fallback 文案
- vault/meta/EXPERT_LIBRARY.json   —— 统一人名专家库（source of truth）

用法
----
    python3 scripts/domain_recognize.py --text "这道算法竞赛题 dp 怎么写"
    python3 scripts/domain_recognize.py --text "我在做前端 React 页面" --json
    python3 scripts/domain_recognize.py --self-test
    python3 scripts/domain_recognize.py --validate-data

接口约定
--------
输出是一个 JSON 可序列化对象（CLI --json 可直接被 UI/agent 使用）：
{
  "recognized": true,
  "domain": {"id": ..., "name": ..., "confidence": ..., "score": ...},
  "decision": "expert_team" | "expert_gap" | "ask_domain",
  "experts": [已 ready 的完整专家对象],
  "candidate_experts": [未 ready 的候选专家对象],
  "fallback": {"type": "use_llm_directly", "question": ..., "options": [...]} | null
}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

META_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vault", "meta")
DOMAIN_PROFILES_PATH = os.path.join(META_DIR, "domain-profiles.json")
EXPERT_LIBRARY_PATH = os.path.join(META_DIR, "EXPERT_LIBRARY.json")

REQUIRED_EXPERT_FIELDS = ("name", "persona_type", "sourceRefs", "status")
PERSONA_TYPE = "public-figure-style-reference"
STATUS_READY = "ready"


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object")
    return data


def _keyword_hits(text: str, keyword: str) -> bool:
    """小写/边界敏感的关键词匹配。

    纯英文短词使用词边界，避免 'dp' 命中 'edp' 之类；中文和带空格/连字符的
    短语使用子串匹配。
    """
    kw = keyword.lower().strip()
    if not kw:
        return False
    if any("\u4e00" <= ch <= "\u9fff" for ch in kw) or any(ch.isspace() for ch in kw) or "-" in kw:
        return kw in text
    return re.search(r"(?<![a-z0-9])" + re.escape(kw) + r"(?![a-z0-9])", text) is not None


class DomainRecognizer:
    """读取数据文件并在内存中做确定性识别（无 LLM）。"""

    def __init__(self, domain_profiles_path: str = DOMAIN_PROFILES_PATH,
                 expert_library_path: str = EXPERT_LIBRARY_PATH) -> None:
        self.profiles = _load_json(domain_profiles_path)
        self.library = _load_json(expert_library_path)
        self.experts_by_id: Dict[str, Dict[str, Any]] = {}
        for expert in self.library.get("experts", []):
            if isinstance(expert, dict) and expert.get("id"):
                self.experts_by_id[expert["id"]] = expert

    # -- public ---------------------------------------------------------

    def recognize(self, text: str) -> Dict[str, Any]:
        query = (text or "").strip().lower()
        if not query:
            return self._unknown_result("输入为空，无法识别领域")

        best: Optional[Dict[str, Any]] = None
        best_score = 0
        matches: List[str] = []
        for domain in self.profiles.get("domains", []):
            hits = [kw for kw in domain.get("keywords", []) if _keyword_hits(query, kw)]
            # 领域名直接出现视为强信号。
            name = domain.get("name", "")
            if name and name.lower() in query:
                hits.append(name)
            score = len(set(hits))
            if score > best_score:
                best = domain
                best_score = score
                matches = sorted(set(hits))
        if best is None or best_score <= 0:
            return self._unknown_result("未命中任何预置领域关键词")

        confidence = "high" if best_score >= 2 else "medium"
        domain_info = {
            "id": best["id"],
            "name": best.get("name", best["id"]),
            "status": best.get("status", "unknown"),
            "modules": best.get("modules", []),
            "confidence": confidence,
            "score": best_score,
            "matched_keywords": matches,
        }
        return self._resolve_experts(domain_info, best)

    def list_domains(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": d["id"],
                "name": d.get("name", d["id"]),
                "status": d.get("status", "unknown"),
                "modules": d.get("modules", []),
                "expert_ids": d.get("expert_ids", []),
            }
            for d in self.profiles.get("domains", [])
        ]

    def validate_data(self) -> List[str]:
        errors: List[str] = []
        domains = self.profiles.get("domains", [])
        if not isinstance(domains, list) or not domains:
            errors.append("domain-profiles.json: domains 不能为空")

        expert_ids = set(self.experts_by_id.keys())
        for idx, domain in enumerate(domains):
            if not isinstance(domain, dict):
                errors.append(f"domains[{idx}] 不是对象")
                continue
            did = domain.get("id", f"#{idx}")
            for field in ("id", "name", "keywords"):
                if not domain.get(field):
                    errors.append(f"domain {did}: 缺少必须字段 {field}")
            for ref in domain.get("expert_ids", []):
                if ref not in expert_ids:
                    errors.append(f"domain {did}: expert_id 不存在于 EXPERT_LIBRARY: {ref}")

        for idx, expert in enumerate(self.library.get("experts", [])):
            eid = expert.get("id", f"#{idx}") if isinstance(expert, dict) else f"#{idx}"
            if not isinstance(expert, dict):
                errors.append(f"experts[{idx}] 不是对象")
                continue
            missing = [f for f in REQUIRED_EXPERT_FIELDS if not expert.get(f)]
            if missing:
                errors.append(f"expert {eid}: 缺少字段 {', '.join(missing)}")
            if expert.get("persona_type") != PERSONA_TYPE:
                errors.append(f"expert {eid}: persona_type 必须为 {PERSONA_TYPE}")
            refs = expert.get("sourceRefs", [])
            if not isinstance(refs, list) or not refs:
                errors.append(f"expert {eid}: sourceRefs 不能为空")
            if expert.get("status") == STATUS_READY and not refs:
                errors.append(f"expert {eid}: ready 专家必须有 sourceRefs")
        return errors

    # -- internals ------------------------------------------------------

    def _resolve_experts(self, domain_info: Dict[str, Any], domain: Dict[str, Any]) -> Dict[str, Any]:
        refs = domain.get("expert_ids", [])
        # 兼容旧版：域内直接内嵌 experts 对象。
        if not refs and domain.get("experts"):
            refs = [e.get("id") for e in domain["experts"] if isinstance(e, dict) and e.get("id")]

        ready: List[Dict[str, Any]] = []
        candidates: List[Dict[str, Any]] = []
        for ref in refs:
            expert = self.experts_by_id.get(ref)
            if not expert:
                continue
            if self._is_ready(expert):
                ready.append(expert)
            else:
                candidates.append(expert)

        result = {
            "recognized": True,
            "domain": domain_info,
            "domain_id": domain_info["id"],
            "domain_name": domain_info["name"],
            "confidence": domain_info["confidence"],
            "matched_keywords": domain_info["matched_keywords"],
            "modules": domain_info["modules"],
            "decision": "expert_team" if ready else "expert_gap",
            "experts": ready,
            "candidate_experts": candidates,
            "fallback": None,
        }
        if not ready:
            result["fallback"] = self.profiles.get("fallback_action", {
                "type": "use_llm_directly",
                "question": "该领域暂无已备好的人名专家，默认直接用大模型继续；可后续再蒸馏该领域专家团。",
                "options": ["use_llm_directly", "distill_expert"],
            })
        return result

    def _unknown_result(self, reason: str) -> Dict[str, Any]:
        return {
            "recognized": False,
            "domain": None,
            "domain_id": None,
            "domain_name": None,
            "confidence": None,
            "matched_keywords": [],
            "modules": [],
            "decision": "ask_domain",
            "experts": [],
            "candidate_experts": [],
            "reason": reason,
            "suggested_domains": [d["id"] for d in self.profiles.get("domains", [])],
            "fallback": self.profiles.get("unknown_domain_action", {
                "type": "use_llm_directly",
                "question": "没有识别出领域，默认直接用大模型继续；如需指定领域可在回复中说明。",
                "options": ["use_llm_directly", "specify_domain"],
            }),
        }

    @staticmethod
    def _is_ready(expert: Dict[str, Any]) -> bool:
        refs = expert.get("sourceRefs", [])
        return (
            expert.get("status") == STATUS_READY
            and expert.get("persona_type") == PERSONA_TYPE
            and bool(refs)
        )


def _human(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    if result["recognized"]:
        d = result["domain"]
        lines.append(f"领域：{d['name']}（{d['id']}） 置信度={d['confidence']} 命中={d['matched_keywords']}")
        if result["decision"] == "expert_team":
            names = [e.get("displayName") or e.get("name") for e in result["experts"]]
            lines.append(f"专家团：{' / '.join(names)}")
            lines.append("说明：人名专家为风格/方法论参考，不代表本人原话，引用保留 sourceRefs。")
        else:
            lines.append("专家缺口：该领域无 ready 人名专家，默认直接用大模型继续。")
    else:
        lines.append("未识别领域：默认直接用大模型继续；如需指定领域可在回复中说明。")

    fallback = result.get("fallback")
    if fallback:
        lines.append(f"默认处理：{fallback.get('question', '')}")
    return "\n".join(lines)


def _validate_data() -> int:
    recognizer = DomainRecognizer()
    errors = recognizer.validate_data()
    if errors:
        print("Invalid domain data:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"OK: {len(recognizer.list_domains())} domain(s), "
          f"{len(recognizer.library.get('experts', []))} expert(s) validated")
    return 0


def _self_test() -> int:
    r = DomainRecognizer()
    cases = [
        ("这道算法竞赛题 dp 怎么写", True, "algorithm", "expert_team"),
        ("我在做前端 React 页面", True, "frontend", "expert_team"),
        ("后端接口怎么设计？", True, "backend", "expert_team"),
        ("随便聊聊天气", False, None, "ask_domain"),
    ]
    for text, recognized, domain_id, decision in cases:
        out = r.recognize(text)
        assert out["recognized"] is recognized, f"{text}: recognized mismatch"
        assert (out.get("domain") or {}).get("id") == domain_id, f"{text}: domain mismatch"
        assert out["decision"] == decision, f"{text}: decision mismatch"
        for expert in out["experts"]:
            assert expert.get("persona_type") == PERSONA_TYPE
            assert expert.get("sourceRefs")
    print("OK: domain self-test passed (4 cases)")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="用户自然语言输入")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON（数据接口）")
    parser.add_argument("--list-domains", action="store_true", help="列出预置领域")
    parser.add_argument("--self-test", action="store_true", help="跑内置自测")
    parser.add_argument("--validate-data", action="store_true", help="校验领域/专家数据纪律")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()
    if args.validate_data:
        return _validate_data()

    r = DomainRecognizer()
    if args.list_domains:
        print(json.dumps(r.list_domains(), ensure_ascii=False, indent=2))
        return 0
    if args.text is None:
        parser.error("--text 必填（或使用 --list-domains / --self-test / --validate-data）")

    result = r.recognize(args.text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
