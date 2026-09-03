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
import type { Context } from 'cordis';
import z from 'schemastery';
type AppContext = Context & {
    skills: {
        register(skill: unknown): () => void;
    };
    tools: unknown;
};
export declare const name = "@dsh-external/dsh-skill-vault";
export declare const inject: string[];
export interface Config {
    /** Vault repo root. Default: <plugin package root>/vault */
    vaultRoot: string;
    /** Plugin data dir for enabled.json. Default: <DSH_HOME>/skill-vault */
    dataDir: string;
}
export declare const Config: z<Schemastery.ObjectS<{
    vaultRoot: z<string, string>;
    dataDir: z<string, string>;
}>, Schemastery.ObjectT<{
    vaultRoot: z<string, string>;
    dataDir: z<string, string>;
}>>;
export declare function apply(ctx: AppContext, config: Config): void;
export {};
