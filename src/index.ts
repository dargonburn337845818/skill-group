/**
 * @dsh-external/dsh-skill-vault — hybrid 形态的 DSH 技能保险库。
 *
 * 提供：
 *   - 运行时 skill 注册：把 vault 中“已启用”的蒸馏 skill 注册到 ctx.skills
 *   - agent 工具：skill_vault_list / enable / disable / add
 *   - Web UI API：/skill-vault/api（配合 src/client 面板）
 *
 * 运维边界（遵循 ~/.dsh/dsh-optimization-consensus.md）：
 *   - 本插件只读写插件数据目录与 vault；不自动 git pull/push。
 *   - 推送由 vault 根目录 scripts/push.sh 手动执行。
 */
import type { Context } from 'cordis'
import z from 'schemastery'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { SkillVaultManager } from './manager.js'
import { registerTools } from './tools.js'
import { registerApi } from './api.js'

type AppContext = Context & {
  skills: { register(skill: unknown): () => void }
  tools: unknown
}

export const name = '@dsh-external/dsh-skill-vault'
export const inject = ['skills', 'tools', 'webServer']

export interface Config {
  /** Vault repo root. Default: <plugin package root>/vault */
  vaultRoot: string
  /** Plugin data dir for enabled.json. Default: <DSH_HOME>/skill-vault */
  dataDir: string
}

export const Config = z.object({
  vaultRoot: z.string().default(''),
  dataDir: z.string().default(''),
})

export function apply(ctx: AppContext, config: Config): void {
  const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
  const dshHome = process.env.DSH_HOME || join(homedir(), '.dsh')
  const vaultRoot = config.vaultRoot ? resolve(config.vaultRoot) : join(pluginRoot, 'vault')
  const dataDir = config.dataDir ? resolve(config.dataDir) : join(dshHome, 'skill-vault')

  const log = (msg: string): void => {
    ctx.logger?.info?.('[skill-vault] ' + msg)
  }

  const manager = new SkillVaultManager(ctx, vaultRoot, dataDir, log)
  manager.refresh()

  registerTools(ctx, manager)
  registerApi(ctx, manager)

  ctx.effect(() => () => {
    manager.dispose()
  })

  ctx.logger?.info?.('[skill-vault] 就绪 vault=%s data=%s catalog=%d', vaultRoot, dataDir, manager.list().length)
}
