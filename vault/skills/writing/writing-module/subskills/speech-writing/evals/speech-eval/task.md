---
{
  "id": "speech-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "speech-writing",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:口播",
    "contains:节奏",
    "contains:时长",
    "contains:SPEECH_OK"
  ]
}
---

请把下面这段 5 分钟技术汇报改写成可照读的口播稿，输出 markdown，必须覆盖开场、节奏、时长控制。最后输出 SPEECH_OK。

汇报素材：我们的系统从单体架构迁移到微服务后，峰值 QPS 从 500 提升到 5000，部署时间从 40 分钟降到 8 分钟。本次分享讲三件事：为什么拆、怎么拆、踩过的坑。
