/**
 * Skill effect log — lightweight runtime sensor.
 *
 * Records whether a skill was triggered, used, and whether it changed the
 * task outcome. Stored in <DSH_HOME>/skill-vault/effect-log.json (not in git).
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';
export function effectLogPath() {
    const dshHome = process.env.DSH_HOME || join(homedir(), '.dsh');
    return join(dshHome, 'skill-vault', 'effect-log.json');
}
export function loadEffects(file = effectLogPath()) {
    if (!existsSync(file))
        return [];
    try {
        const raw = JSON.parse(readFileSync(file, 'utf8'));
        const entries = Array.isArray(raw) ? raw : Array.isArray(raw?.entries) ? raw.entries : [];
        return entries.filter((e) => e && typeof e.skill === 'string');
    }
    catch {
        return [];
    }
}
export function saveEffects(entries, file = effectLogPath()) {
    mkdirSync(dirname(file), { recursive: true });
    const tmp = file + '.tmp';
    writeFileSync(tmp, JSON.stringify({ version: 1, entries }, null, 2) + '\n', 'utf8');
    renameSync(tmp, file);
}
export function recordEffect(input, file = effectLogPath()) {
    const entry = { at: new Date().toISOString(), ...input };
    const entries = loadEffects(file);
    entries.push(entry);
    saveEffects(entries, file);
    return entry;
}
export function effectStats(entries) {
    const map = new Map();
    for (const e of entries) {
        const row = map.get(e.skill) || { skill: e.skill, total: 0, triggered: 0, used: 0, pos: 0, neu: 0, neg: 0 };
        row.total += 1;
        if (e.triggered)
            row.triggered += 1;
        if (e.used)
            row.used += 1;
        if (e.outcome === 'pos')
            row.pos += 1;
        else if (e.outcome === 'neg')
            row.neg += 1;
        else
            row.neu += 1;
        map.set(e.skill, row);
    }
    return [...map.values()].sort((a, b) => a.skill.localeCompare(b.skill));
}
//# sourceMappingURL=effects.js.map