/**
 * SkillVaultManager — the deep module behind the plugin.
 *
 * Responsibilities:
 *  1. Read the vault catalog.
 *  2. Track persistent (global) and in-memory (session) switch state.
 *  3. Register/unregister enabled skills on ctx.skills.
 *  4. Expose small pure operations used by tools, API, and the UI.
 *
 * The class is intentionally UI- and transport-agnostic.
 */
import type { Context } from 'cordis';
import type { CatalogRow, SwitchScope } from './types.js';
export declare class SkillVaultManager {
    readonly vaultRoot: string;
    readonly dataDir: string;
    private readonly ctx;
    private readonly skills;
    private catalog;
    private persistent;
    private session;
    private disposers;
    private readonly log;
    constructor(ctx: Context, vaultRoot: string, dataDir: string, log?: (msg: string) => void);
    list(): CatalogRow[];
    scenarios(): Array<{
        id: string;
        title: string;
        skillCount: number;
        enabledCount: number;
    }>;
    /** Enable/disable a skill id or a scenario id. */
    set(target: string, enabled: boolean, scope: SwitchScope): {
        ok: boolean;
        type: 'skill' | 'scenario';
        target: string;
    };
    /** Re-register all skills according to the effective state. */
    refresh(): void;
    dispose(): void;
    /** Batch enable/disable in one refresh; used by the skill-router workflow switch. */
    setMany(actions: Array<{
        target: string;
        enabled: boolean;
        scope: SwitchScope;
    }>): Array<{
        ok: boolean;
        type: 'skill' | 'scenario';
        target: string;
    }>;
    /** Reset persistent switches so only the given base ids stay enabled. */
    resetToBase(baseIds: string[]): void;
    /** Base skill ids: entries marked routing=base or activation=always-on. */
    baseIds(): string[];
    /** Add a new skill package by copying an existing distilled skill directory. */
    addSkill(opts: {
        sourcePath: string;
        scenario: string;
        id?: string;
        title?: string;
        description?: string;
        tags?: string[];
        experts?: string[];
        sourceRefs?: string[];
    }): {
        ok: boolean;
        error?: string;
        entry?: CatalogRow;
    };
    private effectiveFor;
    private splitEnabled;
}
