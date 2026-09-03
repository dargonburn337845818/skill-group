import z from 'schemastery';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SkillVaultManager } from './manager.js';
import { registerTools } from './tools.js';
import { registerApi } from './api.js';
export const name = '@dsh-external/dsh-skill-vault';
export const inject = ['skills', 'tools'];
export const Config = z.object({
    vaultRoot: z.string().default(''),
    dataDir: z.string().default(''),
});
export function apply(ctx, config) {
    const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
    const dshHome = process.env.DSH_HOME || join(homedir(), '.dsh');
    const vaultRoot = config.vaultRoot ? resolve(config.vaultRoot) : join(pluginRoot, 'vault');
    const dataDir = config.dataDir ? resolve(config.dataDir) : join(dshHome, 'skill-vault');
    const log = (msg) => {
        ctx.logger?.info?.('[skill-vault] ' + msg);
    };
    const manager = new SkillVaultManager(ctx, vaultRoot, dataDir, log);
    manager.refresh();
    registerTools(ctx, manager);
    registerApi(ctx, manager);
    ctx.effect(() => () => {
        manager.dispose();
    });
    ctx.logger?.info?.('[skill-vault] 就绪 vault=%s data=%s catalog=%d', vaultRoot, dataDir, manager.list().length);
}
//# sourceMappingURL=index.js.map