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
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
const SCENARIO_TITLES = {
    teaching: '教学引导 / 拆题',
    distillation: '内容蒸馏 / 知识化',
    research: '科研 / 组会 / 论文',
    'dsh-ops': 'DSH 运维 / 工具',
};
export function readCatalog(vaultRoot) {
    const skillsRoot = join(vaultRoot, 'skills');
    if (!existsSync(skillsRoot))
        return [];
    const entries = [];
    const scenarioDirs = readdirSync(skillsRoot, { withFileTypes: true })
        .filter((d) => d.isDirectory())
        .sort((a, b) => a.name.localeCompare(b.name));
    for (const scenarioDir of scenarioDirs) {
        const scenario = scenarioDir.name;
        const scenarioPath = join(skillsRoot, scenario);
        const skillDirs = readdirSync(scenarioPath, { withFileTypes: true })
            .filter((d) => d.isDirectory())
            .sort((a, b) => a.name.localeCompare(b.name));
        for (const skillDir of skillDirs) {
            const id = skillDir.name;
            const dir = join(scenarioPath, id);
            const skillPath = join(dir, 'SKILL.md');
            const manifestPath = join(dir, 'manifest.json');
            if (!existsSync(skillPath))
                continue;
            const manifest = readManifest(manifestPath, id, scenario);
            const content = readFileSync(skillPath, 'utf8').replace(/^---[\s\S]*?---\s*/, '').trim();
            entries.push({
                id,
                name: manifest.name || id,
                title: manifest.title || manifest.name || id,
                description: manifest.description || `蒸馏 skill：${id}`,
                whenToUse: manifest.whenToUse,
                scenario,
                scenarioTitle: SCENARIO_TITLES[scenario] || scenario,
                tags: manifest.tags || [],
                experts: manifest.experts || [],
                sourceRefs: manifest.sourceRefs || [],
                activation: manifest.activation || 'catalog',
                version: manifest.version || '0.0.0',
                license: manifest.license,
                dir: resolve(dir),
                skillPath: resolve(skillPath),
                content,
            });
        }
    }
    return entries;
}
function readManifest(path, fallbackId, fallbackScenario) {
    if (!existsSync(path)) {
        return {
            id: fallbackId,
            description: '',
            scenario: fallbackScenario,
        };
    }
    try {
        const raw = JSON.parse(readFileSync(path, 'utf8'));
        const description = typeof raw.description === 'string' ? raw.description : '';
        return {
            id: typeof raw.id === 'string' ? raw.id : fallbackId,
            name: typeof raw.name === 'string' ? raw.name : undefined,
            title: typeof raw.title === 'string' ? raw.title : undefined,
            description,
            whenToUse: typeof raw.whenToUse === 'string' ? raw.whenToUse : undefined,
            scenario: typeof raw.scenario === 'string' ? raw.scenario : fallbackScenario,
            scenarios: Array.isArray(raw.scenarios) ? raw.scenarios.map(String) : undefined,
            tags: Array.isArray(raw.tags) ? raw.tags.map(String) : undefined,
            experts: Array.isArray(raw.experts) ? raw.experts.map(String) : undefined,
            sourceRefs: Array.isArray(raw.sourceRefs) ? raw.sourceRefs.map(String) : undefined,
            activation: raw.activation === 'always-on' ? 'always-on' : raw.activation === 'catalog' ? 'catalog' : undefined,
            version: typeof raw.version === 'string' ? raw.version : undefined,
            license: typeof raw.license === 'string' ? raw.license : undefined,
        };
    }
    catch {
        return {
            id: fallbackId,
            description: '',
            scenario: fallbackScenario,
        };
    }
}
export function scenarioExists(vaultRoot, scenario) {
    const p = join(vaultRoot, 'skills', scenario);
    return existsSync(p) && statSync(p).isDirectory();
}
//# sourceMappingURL=catalog.js.map