/**
 * Skill governance controller — pure decision layer.
 *
 * Reads the runtime effect sensor + static doctor, then maps each catalog skill
 * to a small, human-reviewable recommendation:
 *   keep / enable / disable_or_demote / reduce_trigger / fix / no_data / merge_candidate
 *
 * Flow control: if a skill already has an open governance change
 * (open-changes.json or repo branch marker), actionable suggestions are
 * suppressed and the row is marked `flow_control` instead.
 *
 * This module is transport-independent; the tool, API, and CLI all use it.
 */
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import type { EffectEntry, EffectStatsRow } from './effects.js'
import { effectLogPath, effectStats, loadEffects } from './effects.js'
import type { DoctorIssue } from './doctor.js'
import type { CatalogRow } from './types.js'

export interface GovernanceAction {
  action: 'keep' | 'enable' | 'disable_or_demote' | 'reduce_trigger' | 'fix' | 'no_data' | 'merge_candidate' | 'flow_control'
  reason: string
}

export interface SkillGovernanceRow {
  skill: string
  scenario: string
  enabled: boolean
  total: number
  triggered: number
  used: number
  pos: number
  neu: number
  neg: number
  effectRate: number
  misuseRate: number
  lastAt: string | null
  doctorOk: boolean
  doctorIssues: string[]
  doctorWarnings: string[]
  openChange: boolean
  actions: GovernanceAction[]
}

export interface GovernanceReport {
  at: string
  enabledCount: number
  catalogCount: number
  totalEntries: number
  effectLogPath: string
  doctor: { ok: boolean; pass: number; total: number }
  openChanges: string[]
  rows: SkillGovernanceRow[]
  summary: string
}

export interface OpenChangesFile {
  version?: number
  open?: string[]
  changes?: Array<{ skill: string; branch?: string; pr?: string; openedAt?: string }>
}

export function loadOpenChanges(file?: string): string[] {
  const path = file || join(process.env.DSH_HOME || '', 'skill-vault', 'open-changes.json')
  if (!path || !existsSync(path)) {
    // If DSH_HOME was empty and the default file is just a relative path, still
    // allow a repo-local open-changes.json to be supplied by the caller.
    return []
  }
  try {
    const raw = JSON.parse(readFileSync(path, 'utf8')) as OpenChangesFile | string[]
    if (Array.isArray(raw)) return raw.map(String)
    if (Array.isArray(raw.changes)) return raw.changes.map((c) => String(c.skill))
    if (Array.isArray(raw.open)) return raw.open.map(String)
    return []
  } catch {
    return []
  }
}

export function rowDefault(skill: string, enabled: boolean, scenario: string): SkillGovernanceRow {
  return {
    skill,
    scenario,
    enabled,
    total: 0,
    triggered: 0,
    used: 0,
    pos: 0,
    neu: 0,
    neg: 0,
    effectRate: 0,
    misuseRate: 0,
    lastAt: null,
    doctorOk: true,
    doctorIssues: [],
    doctorWarnings: [],
    openChange: false,
    actions: [],
  }
}

export function buildGovernanceReport(args: {
  catalog: CatalogRow[]
  effects?: EffectEntry[]
  doctorResults?: DoctorIssue[]
  openChanges?: string[]
  effectPath?: string
  openChangesFile?: string
}): GovernanceReport {
  const effects = args.effects ?? loadEffects(args.effectPath ?? effectLogPath())
  const doctorResults = args.doctorResults ?? []
  const openChanges = args.openChanges ?? loadOpenChanges(args.openChangesFile)
  const rows = new Map<string, SkillGovernanceRow>()

  for (const skill of args.catalog) {
    rows.set(skill.id, rowDefault(skill.id, skill.enabled, skill.scenario))
  }

  const stats = effectStats(effects)
  const statsBySkill = new Map<string, EffectStatsRow>(stats.map((s) => [s.skill, s]))
  const latest = new Map<string, string>()
  for (const e of effects) {
    const cur = latest.get(e.skill)
    if (!cur || e.at > cur) latest.set(e.skill, e.at)
  }

  for (const row of rows.values()) {
    const st = statsBySkill.get(row.skill)
    if (st) {
      row.total = st.total
      row.triggered = st.triggered
      row.used = st.used
      row.pos = st.pos
      row.neu = st.neu
      row.neg = st.neg
      row.effectRate = row.total > 0 ? row.pos / row.total : 0
      row.misuseRate = row.triggered > 0 ? Math.max(0, (row.triggered - row.used) / row.triggered) : 0
      row.lastAt = latest.get(row.skill) || null
    }
  }

  for (const d of doctorResults) {
    const row = rows.get(d.skill)
    if (!row) continue
    row.doctorOk = d.ok
    row.doctorIssues = d.issues
    row.doctorWarnings = d.warnings
  }

  for (const row of rows.values()) {
    row.openChange = openChanges.includes(row.skill)
    row.actions = decideActions(row)
  }

  const sorted = [...rows.values()].sort((a, b) => a.skill.localeCompare(b.skill))
  const enabledCount = args.catalog.filter((c) => c.enabled).length
  const totalEntries = effects.length
  const pass = doctorResults.filter((d) => d.ok).length
  const doctor = { ok: pass === doctorResults.length, pass, total: doctorResults.length }
  const actionable = sorted.filter((r) => r.actions.some((a) => !['keep', 'no_data', 'merge_candidate', 'flow_control'].includes(a.action)))
  const summary = [
    `技能库治理报告：${enabledCount}/${args.catalog.length} 已启用`,
    `效果日志：${totalEntries} 条（${args.effectPath ?? effectLogPath()}）`,
    `静态质检：${doctor.pass}/${doctor.total} 通过`,
    `开放变更：${openChanges.length ? openChanges.join(', ') : '无'}`,
    `建议动作：${actionable.length} 项`,
    actionable.slice(0, 8).map((r) => `  - ${r.skill}: ${r.actions.map((a) => a.action).join('/')}`).join('\n'),
  ].filter(Boolean).join('\n')

  return {
    at: new Date().toISOString(),
    enabledCount,
    catalogCount: args.catalog.length,
    totalEntries,
    effectLogPath: args.effectPath ?? effectLogPath(),
    doctor,
    openChanges,
    rows: sorted,
    summary,
  }
}

function decideActions(row: SkillGovernanceRow): GovernanceAction[] {
  // Flow control wins: no new governance action while this skill already has an
  // open change. Close the old one first.
  if (row.openChange) {
    return [{ action: 'flow_control', reason: 'skill already has an open governance change; close it before new actions' }]
  }

  const actions: GovernanceAction[] = []
  const evidence = row.total >= 3

  // Static repair always has priority; it is independent of runtime evidence.
  if (row.doctorIssues.length > 0) {
    actions.push({ action: 'fix', reason: `doctor issues: ${row.doctorIssues.join('; ')}` })
  }

  // Merge candidate: overlapping scenario + no runtime data + disabled is a
  // weak signal; keep it as human-review only, never automatic.
  if (!evidence && !row.enabled) {
    actions.push({ action: 'merge_candidate', reason: 'no effect data; possibly redundant with same-scenario skills' })
  }

  if (!evidence) {
    actions.push({ action: 'no_data', reason: row.total === 0 ? 'no effect entries yet' : 'effect sample < 3' })
  } else if (row.enabled) {
    if (row.effectRate < 0.4) {
      actions.push({ action: 'disable_or_demote', reason: `effect_rate=${fmt(row.effectRate)} < 0.40` })
    }
    if (row.misuseRate > 0.3) {
      actions.push({ action: 'reduce_trigger', reason: `misuse_rate=${fmt(row.misuseRate)} > 0.30` })
    }
    if (row.effectRate >= 0.4 && row.misuseRate <= 0.3) {
      actions.push({ action: 'keep', reason: `effect_rate=${fmt(row.effectRate)}, misuse_rate=${fmt(row.misuseRate)}` })
    }
  } else {
    if (row.effectRate >= 0.5 && row.misuseRate <= 0.3) {
      actions.push({ action: 'enable', reason: `effect_rate=${fmt(row.effectRate)} >= 0.50, misuse_rate=${fmt(row.misuseRate)}` })
    } else {
      actions.push({ action: 'no_data', reason: 'disabled and insufficient positive evidence' })
    }
  }

  // Dedup: if an action repeats (fix from issues while also no_data), keep one.
  const seen = new Set<string>()
  return actions.filter((a) => {
    if (seen.has(a.action)) return false
    seen.add(a.action)
    return true
  })
}

function fmt(x: number): string {
  return (x * 100).toFixed(1) + '%'
}
