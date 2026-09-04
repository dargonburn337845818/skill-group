/**
 * dsh-skill-vault — 领域识别运行时桥。
 *
 * 识别算法以 `scripts/domain_recognize.py` 为唯一实现（数据 + 规则都集中在那里），
 * 本模块只负责：
 *   1. 通过子进程调用 Python 识别器，把 JSON 结果透传给 agent 工具 / Web API。
 *   2. 提供领域/专家元数据读取，供侧边栏“领域 / 专家状态”展示。
 *
 * 这样保持“识别逻辑只写一份”，避免 TS/Python 两套规则漂移。
 */
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const PLUGIN_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const RECOGNIZER = join(PLUGIN_ROOT, 'scripts', 'domain_recognize.py')
const META_DIR = join(PLUGIN_ROOT, 'vault', 'meta')

function pythonBin(): string {
  return process.platform === 'win32' ? 'python' : 'python3'
}

function runRecognizer(args: string[]): unknown {
  const stdout = execFileSync(pythonBin(), [RECOGNIZER, ...args], {
    encoding: 'utf8',
    maxBuffer: 1024 * 1024,
  })
  return JSON.parse(stdout)
}

/** 调用 Python 领域识别器，返回稳定 JSON 结果（含专家团/缺口分支）。 */
export function recognizeDomain(text: string): { ok: boolean; result?: unknown; error?: string } {
  try {
    const result = runRecognizer(['--text', text, '--json'])
    return { ok: true, result }
  } catch (e) {
    return { ok: false, error: String(e) }
  }
}

/** 领域字典（供侧边栏展示预置领域状态）。 */
export function listDomainProfiles(): unknown[] {
  const raw = JSON.parse(readFileSync(join(META_DIR, 'domain-profiles.json'), 'utf8')) as {
    domains?: unknown[]
  }
  return raw.domains || []
}

/** 统一人名专家库（供侧边栏展示专家/缺口状态）。 */
export function listExpertLibrary(): unknown[] {
  const raw = JSON.parse(readFileSync(join(META_DIR, 'EXPERT_LIBRARY.json'), 'utf8')) as {
    experts?: unknown[]
  }
  return raw.experts || []
}

/** 一次拿全侧边栏需要的领域/专家状态数据。 */
export function domainStatusPayload(): Record<string, unknown> {
  return {
    profiles: listDomainProfiles(),
    experts: listExpertLibrary(),
  }
}
