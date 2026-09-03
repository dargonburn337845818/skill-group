/**
 * Agent-facing tools for the skill vault.
 *
 * The public surface is intentionally small and transport-independent:
 *   skill_vault_list     — query catalog by scenario / expert / source / status
 *   skill_vault_enable   — turn on a skill or an entire scenario
 *   skill_vault_disable  — turn off a skill or an entire scenario
 *   skill_vault_add      — prepare a newly distilled skill into the vault (no git)
 */
import { defineTool } from '@deepseek-ai/dsh-tools'
import type { Context } from 'cordis'
import type { SkillVaultManager } from './manager.js'
import type { SwitchScope } from './types.js'

const STRING_ARRAY = {
  type: 'array',
  items: { type: 'string' },
} as const

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
      return { entries: filtered, scenarios: scenarios.filter((s) => !args.scenario || s.id === args.scenario) } as any
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
      scenario: { type: 'string', required: true, description: '目标场景 id：teaching/distillation/research/dsh-ops' },
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
}
