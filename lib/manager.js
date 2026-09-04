import { cpSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { readCatalog, scenarioExists } from './catalog.js';
import { clonePersistedState, emptySessionState, loadPersistedState, savePersistedState, } from './state.js';
export class SkillVaultManager {
    vaultRoot;
    dataDir;
    ctx;
    skills;
    catalog;
    persistent;
    session = emptySessionState();
    disposers = new Map();
    log;
    constructor(ctx, vaultRoot, dataDir, log) {
        this.ctx = ctx;
        this.skills = ctx.skills;
        this.vaultRoot = vaultRoot;
        this.dataDir = dataDir;
        this.persistent = loadPersistedState(dataDir);
        this.catalog = readCatalog(vaultRoot);
        this.log = log || (() => undefined);
    }
    list() {
        return this.catalog.map((entry) => {
            const sessionEnabled = this.effectiveFor(entry);
            const { persistentEnabled, sessionEnabled: sessionOnly } = this.splitEnabled(entry);
            return {
                id: entry.id,
                name: entry.name,
                title: entry.title,
                description: entry.description,
                whenToUse: entry.whenToUse,
                boundary: entry.boundary,
                notWhenToUse: entry.notWhenToUse,
                scenario: entry.scenario,
                scenarioTitle: entry.scenarioTitle,
                routing: entry.routing,
                qualityCriteria: entry.qualityCriteria,
                tags: entry.tags,
                experts: entry.experts,
                sourceRefs: entry.sourceRefs,
                activation: entry.activation,
                hidden: entry.hidden,
                version: entry.version,
                enabled: sessionEnabled,
                persistentEnabled,
                sessionEnabled: sessionOnly,
            };
        });
    }
    scenarios() {
        const rows = this.list();
        const byScenario = new Map();
        for (const row of rows) {
            const list = byScenario.get(row.scenario) || [];
            list.push(row);
            byScenario.set(row.scenario, list);
        }
        return [...byScenario.entries()].map(([id, entries]) => ({
            id,
            title: entries[0]?.scenarioTitle || id,
            skillCount: entries.length,
            enabledCount: entries.filter((e) => e.enabled).length,
        }));
    }
    /** Enable/disable a skill id or a scenario id. */
    set(target, enabled, scope) {
        const skill = this.catalog.find((e) => e.id === target || e.name === target);
        if (skill) {
            if (scope === 'session') {
                this.session.skills.set(skill.id, enabled);
            }
            else {
                this.persistent = clonePersistedState(this.persistent);
                this.persistent.skills[skill.id] = enabled;
                savePersistedState(this.dataDir, this.persistent);
            }
            this.refresh();
            return { ok: true, type: 'skill', target: skill.id };
        }
        const scenario = this.catalog.find((e) => e.scenario === target)?.scenario;
        if (scenario && scenarioExists(this.vaultRoot, scenario)) {
            if (scope === 'session') {
                this.session.scenarios.set(scenario, enabled);
            }
            else {
                this.persistent = clonePersistedState(this.persistent);
                this.persistent.scenarios[scenario] = enabled;
                savePersistedState(this.dataDir, this.persistent);
            }
            this.refresh();
            return { ok: true, type: 'scenario', target: scenario };
        }
        return { ok: false, type: 'skill', target };
    }
    /** Re-register all skills according to the effective state. */
    refresh() {
        for (const disposer of this.disposers.values()) {
            try {
                disposer();
            }
            catch { /* unregister is best-effort */ }
        }
        this.disposers.clear();
        for (const entry of this.catalog) {
            if (!this.effectiveFor(entry))
                continue;
            try {
                const disposer = this.skills.register({
                    name: entry.name,
                    description: entry.description,
                    whenToUse: entry.whenToUse,
                    content: entry.content,
                    source: 'runtime',
                    invocation: { modelInvocable: true, userInvocable: true },
                    provider: 'skill-vault',
                    resourceBase: { kind: 'directory', path: entry.dir },
                });
                this.disposers.set(entry.id, disposer);
                this.log(`registered ${entry.name} (${entry.id})`);
            }
            catch (e) {
                this.log('register failed ' + entry.id + ': ' + String(e));
            }
        }
    }
    dispose() {
        for (const disposer of this.disposers.values()) {
            try {
                disposer();
            }
            catch { /* ignore */ }
        }
        this.disposers.clear();
    }
    /** Batch enable/disable in one refresh; used by the skill-router workflow switch. */
    setMany(actions) {
        const results = [];
        for (const action of actions) {
            results.push(this.set(action.target, action.enabled, action.scope));
        }
        return results;
    }
    /** Reset persistent switches so only the given base ids stay enabled. */
    resetToBase(baseIds) {
        this.persistent = clonePersistedState(this.persistent);
        this.persistent.scenarios = {};
        this.persistent.skills = {};
        for (const id of baseIds) {
            this.persistent.skills[id] = true;
        }
        savePersistedState(this.dataDir, this.persistent);
        this.session = emptySessionState();
        this.refresh();
    }
    /** Base skill ids: entries marked routing=base or activation=always-on. */
    baseIds() {
        return this.catalog.filter((e) => e.routing === 'base' || e.activation === 'always-on').map((e) => e.id);
    }
    /** Add a new skill package by copying an existing distilled skill directory. */
    addSkill(opts) {
        if (!scenarioExists(this.vaultRoot, opts.scenario)) {
            return { ok: false, error: `scenario not found: ${opts.scenario}` };
        }
        const source = opts.sourcePath;
        if (!existsSync(source))
            return { ok: false, error: `source not found: ${source}` };
        if (!existsSync(join(source, 'SKILL.md')))
            return { ok: false, error: 'source must contain SKILL.md' };
        const id = opts.id || source.split(/[\\/]/).filter(Boolean).pop() || 'new-skill';
        const dest = join(this.vaultRoot, 'skills', opts.scenario, id);
        if (existsSync(dest))
            return { ok: false, error: `destination already exists: ${dest}` };
        // Minimal copy: skip heavy/generated dirs by default.
        mkdirSync(dest, { recursive: true });
        cpSync(source, dest, { recursive: true, filter: (p) => !/node_modules|\.git|__pycache__|lib\/|dist\//.test(p) });
        const manifestPath = join(dest, 'manifest.json');
        if (!existsSync(manifestPath)) {
            writeFileSync(manifestPath, JSON.stringify({
                id,
                name: id,
                title: opts.title || id,
                description: opts.description || `蒸馏 skill：${id}`,
                scenario: opts.scenario,
                tags: opts.tags || [],
                experts: opts.experts || [],
                sourceRefs: opts.sourceRefs || [],
                version: '0.0.1',
                license: 'MIT',
            }, null, 2) + '\n', 'utf8');
        }
        // Re-read catalog so the new entry is immediately visible.
        this.catalog = readCatalog(this.vaultRoot);
        this.refresh();
        const entry = this.list().find((e) => e.id === id);
        return { ok: true, entry };
    }
    effectiveFor(entry) {
        const sessionSkill = this.session.skills.get(entry.id);
        if (sessionSkill !== undefined)
            return sessionSkill;
        const persistentSkill = this.persistent.skills[entry.id];
        if (persistentSkill !== undefined)
            return persistentSkill;
        const sessionScenario = this.session.scenarios.get(entry.scenario);
        if (sessionScenario !== undefined)
            return sessionScenario;
        const persistentScenario = this.persistent.scenarios[entry.scenario];
        if (persistentScenario !== undefined)
            return persistentScenario;
        return false;
    }
    splitEnabled(entry) {
        const persistentSkill = this.persistent.skills[entry.id];
        const persistentScenario = this.persistent.scenarios[entry.scenario];
        const persistentEnabled = persistentSkill !== undefined ? persistentSkill : persistentScenario !== undefined ? persistentScenario : false;
        const sessionSkill = this.session.skills.get(entry.id);
        const sessionScenario = this.session.scenarios.get(entry.scenario);
        const sessionEnabled = sessionSkill !== undefined ? sessionSkill : sessionScenario !== undefined ? sessionScenario : persistentEnabled;
        return { persistentEnabled, sessionEnabled: sessionEnabled !== persistentEnabled };
    }
}
//# sourceMappingURL=manager.js.map