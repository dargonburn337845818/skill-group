/**
 * Vault catalog reader.
 *
 * Layout contract (one level only, matching DSH's own skill discovery depth):
 *
 *   vaultRoot/skills/<scenario>/<skill-id>/{SKILL.md, manifest.json, ...}
 *
 * The plugin intentionally does not recurse deeper; a skill package is exactly
 * one directory below its scenario directory.
 */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs'
import { join, resolve } from 'node:path'
import type { SkillEntry, SkillManifest } from './types.js'

const SCENARIO_TITLES: Record<string, string> = {
  teaching: '教学引导 / 拆题',
  learning: 'AI 学习 / 自我提升',
  distillation: '内容蒸馏 / 知识化',
  distill: '蒸馏 / 元能力迭代',
  research: '科研 / 组会 / 论文',
  teacher: '教师 / 专家讨论',
  writing: '文稿 / 提示词 / 文案 / 报告',
  'dsh-ops': 'DSH 运维 / 工具',
  base: '常驻底座 / 搜索与共识',
  'core-iteration': '核心迭代元能力 / 价值递归提升',
  github: 'GitHub 开源仓库 / 发布',
}

export function readCatalog(vaultRoot: string): SkillEntry[] {
  const skillsRoot = join(vaultRoot, 'skills')
  if (!existsSync(skillsRoot)) return []
  const entries: SkillEntry[] = []
  const scenarioDirs = readdirSync(skillsRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .sort((a, b) => a.name.localeCompare(b.name))

  for (const scenarioDir of scenarioDirs) {
    const scenario = scenarioDir.name
    const scenarioPath = join(skillsRoot, scenario)
    const skillDirs = readdirSync(scenarioPath, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .sort((a, b) => a.name.localeCompare(b.name))

    for (const skillDir of skillDirs) {
      const id = skillDir.name
      const dir = join(scenarioPath, id)
      const skillPath = join(dir, 'SKILL.md')
      const manifestPath = join(dir, 'manifest.json')
      if (!existsSync(skillPath)) continue

      const manifest = readManifest(manifestPath, id, scenario)
      if (manifest.hidden || manifest.activation === 'internal') continue
      const content = readFileSync(skillPath, 'utf8').replace(/^---[\s\S]*?---\s*/, '').trim()
      entries.push({
        id,
        name: manifest.name || id,
        title: manifest.title || manifest.name || id,
        description: manifest.description || `蒸馏 skill：${id}`,
        whenToUse: manifest.whenToUse,
        boundary: manifest.boundary,
        notWhenToUse: manifest.notWhenToUse,
        scenario,
        scenarioTitle: SCENARIO_TITLES[scenario] || scenario,
        routing: manifest.routing || 'domain',
        qualityCriteria: manifest.qualityCriteria,
        tags: manifest.tags || [],
        experts: manifest.experts || [],
        sourceRefs: manifest.sourceRefs || [],
        activation: manifest.activation || 'catalog',
        hidden: false,
        version: manifest.version || '0.0.0',
        license: manifest.license,
        dir: resolve(dir),
        skillPath: resolve(skillPath),
        content,
      })
    }
  }
  return entries
}

function readManifest(path: string, fallbackId: string, fallbackScenario: string): SkillManifest {
  if (!existsSync(path)) {
    return {
      id: fallbackId,
      description: '',
      scenario: fallbackScenario,
    }
  }
  try {
    const raw = JSON.parse(readFileSync(path, 'utf8')) as Partial<SkillManifest>
    const description = typeof raw.description === 'string' ? raw.description : ''
    const routing = raw.routing === 'base' || raw.routing === 'core' ? raw.routing : raw.routing === 'domain' ? 'domain' : undefined
    return {
      id: typeof raw.id === 'string' ? raw.id : fallbackId,
      name: typeof raw.name === 'string' ? raw.name : undefined,
      title: typeof raw.title === 'string' ? raw.title : undefined,
      description,
      whenToUse: typeof raw.whenToUse === 'string' ? raw.whenToUse : undefined,
      boundary: typeof raw.boundary === 'string' ? raw.boundary : undefined,
      notWhenToUse: typeof raw.notWhenToUse === 'string' ? raw.notWhenToUse : undefined,
      scenario: typeof raw.scenario === 'string' ? raw.scenario : fallbackScenario,
      scenarios: Array.isArray(raw.scenarios) ? raw.scenarios.map(String) : undefined,
      routing,
      qualityCriteria: parseQualityCriteria(raw.qualityCriteria),
      tags: Array.isArray(raw.tags) ? raw.tags.map(String) : undefined,
      experts: Array.isArray(raw.experts) ? raw.experts.map(String) : undefined,
      sourceRefs: Array.isArray(raw.sourceRefs) ? raw.sourceRefs.map(String) : undefined,
      activation: raw.activation === 'always-on' ? 'always-on' : raw.activation === 'internal' ? 'internal' : raw.activation === 'catalog' ? 'catalog' : undefined,
      hidden: raw.hidden === true,
      version: typeof raw.version === 'string' ? raw.version : undefined,
      license: typeof raw.license === 'string' ? raw.license : undefined,
    }
  } catch {
    return {
      id: fallbackId,
      description: '',
      scenario: fallbackScenario,
    }
  }
}


function parseQualityCriteria(v: unknown): SkillManifest['qualityCriteria'] {
  if (!v || typeof v !== 'object' || Array.isArray(v)) return undefined
  const raw = v as Record<string, unknown>
  const strArray = (x: unknown): string[] | undefined => Array.isArray(x) ? x.map(String) : undefined
  const min = typeof raw.minIndependentSources === 'number' ? raw.minIndependentSources : undefined
  return {
    high: strArray(raw.high),
    reject: strArray(raw.reject),
    minIndependentSources: min,
    notes: typeof raw.notes === 'string' ? raw.notes : undefined,
  }
}

export function scenarioExists(vaultRoot: string, scenario: string): boolean {
  const p = join(vaultRoot, 'skills', scenario)
  return existsSync(p) && statSync(p).isDirectory()
}
