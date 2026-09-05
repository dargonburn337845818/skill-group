/**
 * Skill doctor — health check for the public skill catalog.
 *
 * Checks the same discipline as `scripts/skill_doctor.py` but from the plugin,
 * so an agent/user can run it without a Python path. It only checks public
 * (registered) skill packages, not internal subskills.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { readCatalog } from './catalog.js';
const EXT = /\.(md|yml|yaml|ts|js|py|json|txt)$/;
function frontmatterName(text) {
    if (!text.startsWith('---'))
        return '';
    const end = text.indexOf('\n---', 3);
    if (end < 0)
        return '';
    for (const line of text.slice(3, end).split('\n')) {
        const m = /^name:\s*(.+)$/.exec(line.trim());
        if (m)
            return m[1].trim().replace(/^["']|["']$/g, '');
    }
    return '';
}
function checkSkill(dir, id) {
    const issues = [];
    const warnings = [];
    const skillPath = join(dir, 'SKILL.md');
    const manifestPath = join(dir, 'manifest.json');
    const changelogPath = join(dir, 'CHANGELOG.md');
    if (!existsSync(skillPath))
        issues.push('missing SKILL.md');
    else {
        const text = readFileSync(skillPath, 'utf8');
        const name = frontmatterName(text);
        if (name && name !== id)
            issues.push(`frontmatter name '${name}' != dir '${id}'`);
        const lower = text.toLowerCase();
        const hasTrigger = /触发|when to use|trigger/.test(lower);
        const hasAction = /动作|workflow|action|步骤/.test(lower);
        const hasBoundary = /边界|反例|boundary|not when|失效/.test(lower);
        if (!(hasTrigger && hasAction && hasBoundary)) {
            issues.push(`body discipline incomplete: trigger=${hasTrigger} action=${hasAction} boundary=${hasBoundary}`);
        }
    }
    if (!existsSync(manifestPath))
        issues.push('missing manifest.json');
    else {
        try {
            const m = JSON.parse(readFileSync(manifestPath, 'utf8'));
            if (m.id !== id)
                issues.push(`manifest.id '${m.id}' != dir '${id}'`);
            if (!Array.isArray(m.sourceRefs) || m.sourceRefs.length === 0)
                warnings.push('manifest.sourceRefs missing/empty');
            const tags = Array.isArray(m.tags) ? m.tags : [];
            if (tags.length > 8)
                warnings.push(`tags > 8 (${tags.length})`);
        }
        catch {
            issues.push('manifest.json invalid JSON');
        }
    }
    if (!existsSync(changelogPath))
        warnings.push('no CHANGELOG.md');
    // references: warn if referenced local files do not exist (markdown links only)
    const refsDir = join(dir, 'references');
    if (existsSync(refsDir)) {
        const refNames = readdirSync(refsDir).filter((f) => existsSync(join(refsDir, f)));
        for (const ref of refNames) {
            if (!/\.(md|json|txt|yaml|yml|ts|js)$/.test(ref))
                continue;
            // Only warn if the SKILL.md never mentions it at all.
            const skillText = existsSync(skillPath) ? readFileSync(skillPath, 'utf8') : '';
            if (!skillText.includes(ref))
                warnings.push(`references/${ref} not referenced by SKILL.md`);
        }
    }
    return { skill: id, ok: issues.length === 0, issues, warnings };
}
/** Run doctor across the public catalog under vaultRoot/skills. */
export function runDoctor(vaultRoot) {
    const entries = readCatalog(vaultRoot);
    return entries.map((e) => checkSkill(e.dir, e.id));
}
//# sourceMappingURL=doctor.js.map