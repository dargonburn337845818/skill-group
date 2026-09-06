/**
 * Agent-facing tools for the skill vault.
 *
 * The public surface is intentionally small and transport-independent:
 *   skill_vault_list     — query catalog by scenario / expert / source / status
 *   skill_vault_enable   — turn on a skill or an entire scenario
 *   skill_vault_disable  — turn off a skill or an entire scenario
 *   skill_vault_add      — prepare a newly distilled skill into the vault (no git)
 *   skill_effect_log     — runtime effect sensor: record / report / stats
 *   skill_doctor         — static health check
 *   skill_governance     — effect-driven governance controller + flow control
 *   skill_domain_recognize — recognize domain and load person-expert team / gap branch
 *   teacher_discussion_start / round / status / finish — round-based teacher discussion runtime
 *   teacher_expert_select — pick expert subset for a teacher session
 */
import { defineTool } from '@deepseek-ai/dsh-tools'
import type { Context } from 'cordis'
import { join } from 'node:path'
import { recognizeDomain } from './domain.js'
import { teacherStore } from './teacher.js'
import { effectLogPath, effectStats, loadEffects, recordEffect } from './effects.js'
import { runDoctor } from './doctor.js'
import { buildGovernanceReport, loadOpenChanges } from './governance.js'
import type { TeacherAdjudication, TeacherConclusion, TeacherConflict, TeacherRoundInput, TeacherSpeak } from './teacher.js'
import type { SkillVaultManager } from './manager.js'
import type { SwitchScope } from './types.js'

const STRING_ARRAY = {
  type: 'array',
  items: { type: 'string' },
} as const

/** Strip undefined fields so tool output passes lossless-JSON validation. */
function lossless<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T
}

export function registerTools(ctx: Context, manager: SkillVaultManager): void {
  ctx.tools.register(defineTool({
    name: 'skill_vault_list',
    description: '列出 dsh-skill-vault 中全部蒸馏 skill、场景分组与启用状态；可按场景/来源专家/启用状态筛选。',
    parameters: {
      scenario: { type: 'string', description: '按场景 id 筛选，如 teaching/distillation/research/dsh-ops' },
      status: { type: 'string', enum: ['enabled', 'disabled'], description: '按启用状态筛选' },
      expert: { type: 'string', description: '按专家名或来源关键词筛选' },
      source: { type: 'string', description: '按来源引用/来源文字筛选' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const rows = value as { entries: any[]; scenarios: any[] }
        const lines: string[] = []
        lines.push(`技能库概览：${rows.entries.length} 个 skill，${rows.scenarios.length} 个场景`)
        for (const s of rows.scenarios as Array<{ id: string; title: string; skillCount: number; enabledCount: number }>) {
          lines.push(`- [${s.id}] ${s.title}: ${s.enabledCount}/${s.skillCount} 已启用`)
        }
        for (const e of rows.entries as Array<Record<string, any>>) {
          const mark = e.enabled ? '●' : '○'
          lines.push(`${mark} ${e.id} | ${e.title} | ${e.scenario} | ${e.description}`)
          if (e.experts?.length) lines.push(`    专家: ${e.experts.join(', ')}`)
          if (e.sourceRefs?.length) lines.push(`    来源: ${e.sourceRefs.join(', ')}`)
        }
        return [{ type: 'text', text: lines.join('\n') }]
      },
    },
    async execute(args) {
      const rows = manager.list()
      const scenarios = manager.scenarios()
      const status = args.status as 'enabled' | 'disabled' | undefined
      const filtered = rows.filter((r) => {
        if (args.scenario && r.scenario !== args.scenario && !r.tags.includes(args.scenario)) return false
        if (status === 'enabled' && !r.enabled) return false
        if (status === 'disabled' && r.enabled) return false
        if (args.expert && !r.experts.some((x) => x.includes(args.expert!)) && !r.description.includes(args.expert)) return false
        if (args.source && !r.sourceRefs.some((x) => x.includes(args.source!)) && !r.description.includes(args.source)) return false
        return true
      })
      return lossless({ entries: filtered, scenarios: scenarios.filter((s) => !args.scenario || s.id === args.scenario) }) as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_domain_recognize',
    description: '从用户自然语言识别领域，并加载该领域已备好的具体人名专家团；无 ready 专家时返回 expert_gap（默认直接使用大模型继续，不弹 DSH 对话框）。',
    parameters: {
      text: { type: 'string', required: true, description: '用户自然语言输入，如“这道算法竞赛题 dp 怎么写”' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; result?: any }
        if (!v.ok) return [{ type: 'text', text: `领域识别失败：${v.error || '未知错误'}` }]
        const r = v.result || {}
        if (!r.recognized) {
          return [{ type: 'text', text: `未识别领域（${r.reason || '低置信度'}），默认按 use_llm_directly 继续；如需指定领域可在回复中说明。` }]
        }
        const d = r.domain || {}
        const lines = [`领域：${d.name}（${d.id}） 置信度=${d.confidence} 命中=${(d.matched_keywords || []).join(', ')}`]
        if (r.decision === 'expert_team') {
          const names = (r.experts || []).map((e: any) => e.displayName || e.name).join(' / ')
          lines.push(`专家团：${names}`)
          lines.push('说明：人名专家为风格/方法论参考，非本人原话，引用保留 sourceRefs。')
        } else {
          lines.push('专家缺口：该领域无 ready 人名专家，默认按 use_llm_directly 继续，不弹窗询问。')
          lines.push(`默认：${r.fallback?.question || '可后续蒸馏该领域专家团'}`)
        }
        return [{ type: 'text', text: lines.join('\n') }]
      },
    },
    async execute(args) {
      return recognizeDomain(String(args.text || '')) as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_vault_enable',
    description: '启用一个蒸馏 skill，或启用整个场景下的所有 skill。默认写入全局配置（持久）；传 scope=session 只影响当前会话。',
    parameters: {
      target: { type: 'string', required: true, description: 'skill id（如 teacher-consensus）或场景 id（如 teaching）' },
      scope: { type: 'string', enum: ['global', 'session'], description: 'global=持久全局（默认），session=仅当前会话' },
    },
    output: {
      schema: {
        type: 'object',
        additionalProperties: false,
        properties: {
          ok: { type: 'boolean' },
          type: { type: 'string' },
          target: { type: 'string' },
          scope: { type: 'string' },
          message: { type: 'string' },
        },
      },
      render: (_args, value) => {
        const v = value as { ok: boolean; type: string; target: string; scope: string; message: string }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute(args) {
      const scope: SwitchScope = args.scope === 'session' ? 'session' : 'global'
      const result = manager.set(args.target, true, scope)
      const message = result.ok
        ? `已启用${result.type === 'scenario' ? '场景' : 'skill'} ${result.target}（${scope}）`
        : `未找到可启用的目标：${args.target}`
      return { ok: result.ok, type: result.type, target: result.target, scope, message }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_vault_disable',
    description: '关闭一个蒸馏 skill，或关闭整个场景下的所有 skill。默认写入全局配置（持久）；传 scope=session 只影响当前会话。',
    parameters: {
      target: { type: 'string', required: true, description: 'skill id 或场景 id' },
      scope: { type: 'string', enum: ['global', 'session'], description: 'global=持久全局（默认），session=仅当前会话' },
    },
    output: {
      schema: {
        type: 'object',
        additionalProperties: false,
        properties: {
          ok: { type: 'boolean' },
          type: { type: 'string' },
          target: { type: 'string' },
          scope: { type: 'string' },
          message: { type: 'string' },
        },
      },
      render: (_args, value) => {
        const v = value as { ok: boolean; type: string; target: string; scope: string; message: string }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute(args) {
      const scope: SwitchScope = args.scope === 'session' ? 'session' : 'global'
      const result = manager.set(args.target, false, scope)
      const message = result.ok
        ? `已关闭${result.type === 'scenario' ? '场景' : 'skill'} ${result.target}（${scope}）`
        : `未找到可关闭的目标：${args.target}`
      return { ok: result.ok, type: result.type, target: result.target, scope, message }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_vault_add',
    description: '把一份已蒸馏的 skill（含 SKILL.md）拷贝进 vault，生成 manifest，供后续审核/提交。此工具不做 git 提交/推送。',
    parameters: {
      sourcePath: { type: 'string', required: true, description: '源目录绝对路径，必须含 SKILL.md' },
      scenario: { type: 'string', required: true, description: '目标场景 id：teaching/teacher/distillation/dev/research/writing/dsh-ops 等' },
      id: { type: 'string', description: 'skill id（默认取源目录名）' },
      title: { type: 'string', description: '显示标题' },
      description: { type: 'string', description: '一句话说明' },
      tags: STRING_ARRAY,
      experts: STRING_ARRAY,
      sourceRefs: STRING_ARRAY,
    },
    output: {
      schema: {
        type: 'object',
        additionalProperties: false,
        properties: {
          ok: { type: 'boolean' },
          error: { type: 'string' },
          id: { type: 'string' },
          path: { type: 'string' },
          message: { type: 'string' },
        },
      },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; id?: string; path?: string; message: string }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute(args) {
      const result = manager.addSkill({
        sourcePath: args.sourcePath,
        scenario: args.scenario,
        id: args.id,
        title: args.title,
        description: args.description,
        tags: args.tags || [],
        experts: args.experts || [],
        sourceRefs: args.sourceRefs || [],
      })
      if (!result.ok) return { ok: false, error: result.error, message: `入库失败：${result.error}` }
      const entry = result.entry!
      return {
        ok: true,
        id: entry.id,
        path: entry.scenario,
        message: `已准备入库 ${entry.id}（场景 ${entry.scenario}）。请审核后手动 git add/commit/push。`,
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_effect_log',
    description: '技能效果传感器：记录一次 skill 使用效果（是否触发/是否使用/结果），或查看明细/统计；用于技能库治理闭环。',
    parameters: {
      action: { type: 'string', enum: ['record', 'report', 'stats'], required: true, description: 'record=记录一次；report=列出明细；stats=按 skill 统计效果率/误触发率' },
      skill: { type: 'string', description: 'skill id；record 必填，report/stats 可选过滤' },
      task: { type: 'string', description: 'record 时：任务简述' },
      triggered: { type: 'boolean', description: 'record 时：是否被触发（出现在 available_skills 或被加载）' },
      used: { type: 'boolean', description: 'record 时：是否真正被采用/影响了行为' },
      outcome: { type: 'string', enum: ['pos', 'neu', 'neg'], description: 'record 时：结果正向/中性/负向' },
      note: { type: 'string', description: 'record 时：备注' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { message: string }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute(args) {
      const action = args.action as 'record' | 'report' | 'stats'
      const skill = (args.skill as string | undefined) || ''
      if (action === 'record') {
        if (!skill) return { ok: false, message: 'skill 必填' } as any
        const entry = recordEffect({
          skill,
          task: String(args.task || ''),
          triggered: Boolean(args.triggered),
          used: Boolean(args.used),
          outcome: (args.outcome as 'pos' | 'neu' | 'neg') || 'neu',
          note: String(args.note || ''),
        })
        return lossless({ ok: true, message: `recorded ${skill} -> ${entry.outcome} (${effectLogPath()})`, entry }) as any
      }
      const entries = loadEffects().filter((e) => !skill || e.skill === skill)
      if (action === 'report') {
        const lines = entries.map((e) => `${e.at} | ${e.skill} | task=${e.task} | triggered=${e.triggered} used=${e.used} outcome=${e.outcome} | ${e.note}`)
        return lossless({ ok: true, count: entries.length, message: lines.join('\n') || 'no entries', entries }) as any
      }
      const rows = effectStats(entries)
      const lines = rows.map((r) => `${r.skill}: total=${r.total} triggered=${r.triggered} used=${r.used} pos=${r.pos} neu=${r.neu} neg=${r.neg}`)
      const total = rows.reduce((a, r) => a + r.total, 0)
      const pos = rows.reduce((a, r) => a + r.pos, 0)
      const message = total ? `effect_rate=${(pos / total * 100).toFixed(1)}% (${pos}/${total})\n` + lines.join('\n') : 'no entries'
      return lossless({ ok: true, rows, message }) as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_doctor',
    description: '技能库健康检查：检查公开 skill 的 SKILL.md/manifest/三件套/CHANGELOG/references，输出问题清单与通过率。',
    parameters: {},
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; pass: number; total: number; message: string; results: any[] }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute() {
      const results = runDoctor(manager.vaultRoot)
      const pass = results.filter((r) => r.ok).length
      const failed = results.filter((r) => !r.ok)
      const lines: string[] = []
      lines.push(`技能库健康：${pass}/${results.length} 通过`)
      for (const r of failed) {
        lines.push(`FAIL ${r.skill}: ${r.issues.join('; ')}`)
      }
      for (const r of results) {
        if (r.warnings.length) lines.push(`~ ${r.skill}: ${r.warnings.join('; ')}`)
      }
      return lossless({ ok: failed.length === 0, pass, total: results.length, message: lines.join('\n'), results }) as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'skill_governance',
    description: '技能库治理控制器：读取 effect-log + 静态 doctor，按效果率/误触发率/质检输出 keep/enable/disable/demote/reduce-trigger/fix/merge 建议，并检查流量控制（开放变更）。',
    parameters: {
      detail: { type: 'boolean', description: 'true 时返回完整每行指标；false 只返回摘要与建议（默认 false）' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; message: string; report?: any }
        return [{ type: 'text', text: v.message }]
      },
    },
    async execute(args) {
      const openChangesFile = join(manager.vaultRoot, '..', 'agent-memory', 'open-changes.json')
      const report = buildGovernanceReport({
        catalog: manager.list(),
        doctorResults: runDoctor(manager.vaultRoot),
        openChanges: loadOpenChanges(openChangesFile),
        openChangesFile,
      })
      const actionable = report.rows.filter((r) => r.actions.some((a) => a.action !== 'keep' && a.action !== 'no_data'))
      const lines = [
        report.summary,
        '',
        '按 skill 建议：',
        ...actionable.map((r) => {
          const acts = r.actions.map((a) => `${a.action}: ${a.reason}`).join(' | ')
          return `- ${r.skill}（${r.enabled ? '已启用' : '已停用'}）${r.total} 条效果 | ${acts}`
        }),
      ]
      if (args.detail) {
        for (const r of report.rows) {
          lines.push(`[detail] ${r.skill}: total=${r.total} effect=${(r.effectRate * 100).toFixed(1)}% misuse=${(r.misuseRate * 100).toFixed(1)}% doctor=${r.doctorOk ? 'ok' : 'fail'} actions=${r.actions.map((a) => a.action).join('/')}`)
        }
      }
      return lossless({ ok: true, message: lines.join('\n'), report }) as any
    },
  }))

  const SPEAK_SCHEMA = {
    type: 'object',
    additionalProperties: true,
    properties: {
      expert_id: { type: 'string', required: true },
      expert_name: { type: 'string', required: true },
      persona_type: { type: 'string' },
      stance: { type: 'string', required: true },
      claims: STRING_ARRAY,
      style_inference: { type: 'boolean' },
      sourceRefs: STRING_ARRAY,
    },
  } as const

  const CONFLICT_SCHEMA = {
    type: 'object',
    additionalProperties: true,
    properties: {
      conflict_id: { type: 'string', required: true },
      topic: { type: 'string', required: true },
      claim_a: { type: 'object', additionalProperties: true, required: true },
      claim_b: { type: 'object', additionalProperties: true, required: true },
      aligned_expert_ids: STRING_ARRAY,
      sources: STRING_ARRAY,
    },
  } as const

  const ADJUDICATION_SCHEMA = {
    type: 'object',
    additionalProperties: true,
    properties: {
      conflict_id: { type: 'string', required: true },
      adjudicator: { type: 'string', required: true },
      decision: { type: 'string', enum: ['adopt_a', 'adopt_b', 'merge', 'reject', 'defer'] },
      reason: { type: 'string' },
    },
  } as const

  const CONCLUSION_SCHEMA = {
    type: 'object',
    additionalProperties: true,
    properties: {
      conclusion_id: { type: 'string' },
      round: { type: 'number' },
      expert_id: { type: 'string' },
      expert_name: { type: 'string' },
      persona_type: { type: 'string' },
      text: { type: 'string' },
      sourceRefs: STRING_ARRAY,
      decision: { type: 'string' },
    },
  } as const

  function renderTeacherSession(session: any): string {
    if (!session) return '暂无教师讨论会话'
    const d = session.domain ? `${session.domain.name}（${session.domain.id}）` : '未识别领域'
    const names = (session.experts || []).map((e: any) => e.displayName || e.name).join(' / ') || '无 ready 专家'
    const st = session.discussion?.status || 'unknown'
    const lines = [
      `教师会话 ${session.session_id} | 状态=${st}`,
      `领域：${d}`,
      `专家团：${names}`,
      `当前轮：${session.discussion?.current_round || 0}`,
    ]
    if (st === 'expert_gap') {
      lines.push(`专家缺口：${session.discussion?.gap_fallback?.question || '该领域暂无 ready 人名专家'}`)
      lines.push('默认：直接用大模型继续，不弹窗询问。')
    }
    for (const r of session.discussion?.rounds || []) {
      lines.push(`R${r.round} ${r.topic}（${r.status}）`)
      for (const s of r.speaks || []) lines.push(`  - ${s.expert_name}: ${s.stance}`)
      for (const c of r.conflicts || []) lines.push(`  冲突 ${c.conflict_id}: ${c.claim_a?.expert_name} vs ${c.claim_b?.expert_name}`)
      for (const c of r.conclusions || []) lines.push(`  结论 ${c.conclusion_id}: [${c.expert_name}] ${c.text}`)
    }
    if (!session.discussion?.rounds?.length && st !== 'expert_gap') lines.push('尚无讨论轮次；请调用 teacher_discussion_round 记录。')
    return lines.join('\n')
  }

  ctx.tools.register(defineTool({
    name: 'teacher_discussion_start',
    description: '开始一个教师回合式讨论会话：从自然语言识别领域，或直接指定 domain_id，加载该领域已 ready 的人名专家团；无 ready 专家时返回 expert_gap 缺口分支，不静默降级。',
    parameters: {
      text: { type: 'string', description: '用户自然语言，如“这道算法竞赛题 dp 怎么写”' },
      domain_id: { type: 'string', description: '直接指定领域 id，如 algorithm / physics / research' },
      expert_ids: STRING_ARRAY,
      adjacent: { type: 'boolean', description: '是否只引入邻近领域专家（跨领域只取邻近，不拉全库）' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; session?: any }
        if (!v.ok) return [{ type: 'text', text: `启动教师会话失败：${v.error || '未知错误'}` }]
        return [{ type: 'text', text: renderTeacherSession(v.session) }]
      },
    },
    async execute(args) {
      try {
        if (!args.text && !args.domain_id) return { ok: false, error: 'text 或 domain_id 必填' } as any
        const expertIds = Array.isArray(args.expert_ids) ? args.expert_ids.map(String) : undefined
        const opts = { adjacent: Boolean(args.adjacent) }
        const session = args.text
          ? teacherStore.startFromText(String(args.text), expertIds, opts)
          : teacherStore.startFromDomain(String(args.domain_id), expertIds, opts)
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'teacher_discussion_round',
    description: '给教师会话追加一轮完整讨论：独立表态 speaks、冲突点表 conflicts、裁决 adjudications、结论 conclusions（每条结论带 expert_id/expert_name）。',
    parameters: {
      session_id: { type: 'string', required: true },
      topic: { type: 'string', required: true, description: '本轮主题' },
      speaks: { type: 'array', items: SPEAK_SCHEMA },
      conflicts: { type: 'array', items: CONFLICT_SCHEMA },
      adjudications: { type: 'array', items: ADJUDICATION_SCHEMA },
      conclusions: { type: 'array', items: CONCLUSION_SCHEMA },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; session?: any }
        if (!v.ok) return [{ type: 'text', text: `记录教师讨论轮失败：${v.error || '未知错误'}` }]
        return [{ type: 'text', text: renderTeacherSession(v.session) }]
      },
    },
    async execute(args) {
      try {
        const input: TeacherRoundInput = {
          topic: String(args.topic),
          speaks: (args.speaks || []) as unknown as TeacherSpeak[],
          conflicts: (args.conflicts || []) as unknown as TeacherConflict[],
          adjudications: (args.adjudications || []) as unknown as TeacherAdjudication[],
          conclusions: (args.conclusions || []) as unknown as TeacherConclusion[],
        }
        const session = teacherStore.addRound(String(args.session_id), input)
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'teacher_discussion_status',
    description: '读取教师讨论会话状态：当前领域、专家团名单、每轮讨论记录；用于侧边栏/过程监视器或继续讨论。',
    parameters: {
      session_id: { type: 'string', description: '缺省返回最近一次会话' },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; sessions?: any[]; current?: any }
        if (!v.ok) return [{ type: 'text', text: `读取教师会话失败` }]
        const lines: string[] = [`会话数：${(v.sessions || []).length}`]
        if (v.current) lines.push(renderTeacherSession(v.current))
        else lines.push('暂无当前教师会话。')
        return [{ type: 'text', text: lines.join('\n') }]
      },
    },
    async execute(args) {
      const payload = teacherStore.payload(args.session_id ? String(args.session_id) : undefined)
      return { ok: true, ...payload } as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'teacher_expert_select',
    description: '在已开始的教师会话中，从该领域 ready 专家里选择/替换专家子集；继续支持后续自行添加/选择专家。',
    parameters: {
      session_id: { type: 'string', required: true },
      expert_ids: { type: 'array', items: { type: 'string' }, required: true },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; session?: any }
        if (!v.ok) return [{ type: 'text', text: `选择专家失败：${v.error || '未知错误'}` }]
        return [{ type: 'text', text: renderTeacherSession(v.session) }]
      },
    },
    async execute(args) {
      try {
        const session = teacherStore.selectExperts(String(args.session_id), (args.expert_ids || []).map(String))
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'teacher_discussion_finish',
    description: '结束一个教师讨论会话，标记为 finished（供过程监视器显示完成态）。',
    parameters: {
      session_id: { type: 'string', required: true },
    },
    output: {
      schema: { type: 'json' },
      render: (_args, value) => {
        const v = value as { ok: boolean; error?: string; session?: any }
        if (!v.ok) return [{ type: 'text', text: `结束教师会话失败：${v.error || '未知错误'}` }]
        return [{ type: 'text', text: renderTeacherSession(v.session) }]
      },
    },
    async execute(args) {
      try {
        const session = teacherStore.finish(String(args.session_id))
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  // ── 专家团标准化别名（任意模块统一入口，实现在 teacherStore 上完全复用） ──
  const aliasRender = (_args: unknown, value: any): Array<{ type: 'text'; text: string }> => {
    const v = value as { ok: boolean; error?: string; session?: any; sessions?: any[]; current?: any }
    if (!v.ok) return [{ type: 'text', text: `专家团操作失败：${v.error || '未知错误'}` }]
    if (v.session) return [{ type: 'text', text: renderTeacherSession(v.session) }]
    const lines = [`会话数：${(v.sessions || []).length}`]
    if (v.current) lines.push(renderTeacherSession(v.current))
    else lines.push('暂无当前专家团会话。')
    return [{ type: 'text', text: lines.join('\n') }]
  }

  ctx.tools.register(defineTool({
    name: 'expert_team_start',
    description: '标准化专家团启动（任意模块通用）：从自然语言识别领域，或直接指定 domain_id，加载该领域 ready 人名专家团；无 ready 专家时返回 expert_gap。',
    parameters: {
      text: { type: 'string', description: '用户自然语言，如“后端架构评审”“文案评审”“蒸馏算法语料”' },
      domain_id: { type: 'string', description: '直接指定领域 id，如 algorithm / frontend / backend / research / writing' },
      expert_ids: STRING_ARRAY,
      adjacent: { type: 'boolean', description: '是否只引入邻近领域专家' },
    },
    output: { schema: { type: 'json' }, render: aliasRender },
    async execute(args) {
      try {
        if (!args.text && !args.domain_id) return { ok: false, error: 'text 或 domain_id 必填' } as any
        const expertIds = Array.isArray(args.expert_ids) ? args.expert_ids.map(String) : undefined
        const opts = { adjacent: Boolean(args.adjacent) }
        const session = args.text
          ? teacherStore.startFromText(String(args.text), expertIds, opts)
          : teacherStore.startFromDomain(String(args.domain_id), expertIds, opts)
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'expert_team_round',
    description: '标准化专家团追加一轮：独立表态 speaks、冲突点表 conflicts、裁决 adjudications、署名结论 conclusions。',
    parameters: {
      session_id: { type: 'string', required: true },
      topic: { type: 'string', required: true, description: '本轮主题' },
      speaks: { type: 'array', items: SPEAK_SCHEMA },
      conflicts: { type: 'array', items: CONFLICT_SCHEMA },
      adjudications: { type: 'array', items: ADJUDICATION_SCHEMA },
      conclusions: { type: 'array', items: CONCLUSION_SCHEMA },
    },
    output: { schema: { type: 'json' }, render: aliasRender },
    async execute(args) {
      try {
        const input: TeacherRoundInput = {
          topic: String(args.topic),
          speaks: (args.speaks || []) as unknown as TeacherSpeak[],
          conflicts: (args.conflicts || []) as unknown as TeacherConflict[],
          adjudications: (args.adjudications || []) as unknown as TeacherAdjudication[],
          conclusions: (args.conclusions || []) as unknown as TeacherConclusion[],
        }
        const session = teacherStore.addRound(String(args.session_id), input)
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'expert_team_status',
    description: '标准化专家团会话状态：当前领域、专家团、每轮讨论记录；供任意模块继续/查看。',
    parameters: {
      session_id: { type: 'string', description: '缺省返回最近一次会话' },
    },
    output: { schema: { type: 'json' }, render: aliasRender },
    async execute(args) {
      const payload = teacherStore.payload(args.session_id ? String(args.session_id) : undefined)
      return { ok: true, ...payload } as any
    },
  }))

  ctx.tools.register(defineTool({
    name: 'expert_team_select',
    description: '标准化专家团选人：在已开始的会话中，从该领域 ready 专家里选择/替换专家子集。',
    parameters: {
      session_id: { type: 'string', required: true },
      expert_ids: { type: 'array', items: { type: 'string' }, required: true },
    },
    output: { schema: { type: 'json' }, render: aliasRender },
    async execute(args) {
      try {
        const session = teacherStore.selectExperts(String(args.session_id), (args.expert_ids || []).map(String))
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))

  ctx.tools.register(defineTool({
    name: 'expert_team_finish',
    description: '结束一个标准化专家团会话，标记为 finished。',
    parameters: {
      session_id: { type: 'string', required: true },
    },
    output: { schema: { type: 'json' }, render: aliasRender },
    async execute(args) {
      try {
        const session = teacherStore.finish(String(args.session_id))
        return { ok: true, session } as any
      } catch (e) {
        return { ok: false, error: String(e) } as any
      }
    },
  }))
}
