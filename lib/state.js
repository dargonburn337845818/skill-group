/**
 * Persisted + session switch state.
 *
 * Persistent state lives outside the public Git vault
 * (default: <DSH_HOME>/skill-vault/enabled.json) so personal switches are not
 * published. Session state lives only in memory for this process.
 */
import { mkdirSync, readFileSync, writeFileSync, existsSync, renameSync } from 'node:fs';
import { dirname, join } from 'node:path';
export function emptyPersistedState() {
    return { scenarios: {}, skills: {} };
}
export function emptySessionState() {
    return { scenarios: new Map(), skills: new Map() };
}
export function loadPersistedState(dataDir) {
    const file = join(dataDir, 'enabled.json');
    if (!existsSync(file))
        return emptyPersistedState();
    try {
        const raw = JSON.parse(readFileSync(file, 'utf8'));
        return {
            scenarios: isRecord(raw.scenarios) ? { ...raw.scenarios } : {},
            skills: isRecord(raw.skills) ? { ...raw.skills } : {},
        };
    }
    catch {
        return emptyPersistedState();
    }
}
export function savePersistedState(dataDir, state) {
    const file = join(dataDir, 'enabled.json');
    mkdirSync(dirname(file), { recursive: true });
    const tmp = file + '.tmp';
    const payload = { version: 1, scenarios: state.scenarios, skills: state.skills };
    writeFileSync(tmp, JSON.stringify(payload, null, 2) + '\n', 'utf8');
    renameSync(tmp, file);
}
export function clonePersistedState(state) {
    return {
        scenarios: { ...state.scenarios },
        skills: { ...state.skills },
    };
}
function isRecord(v) {
    return !!v && typeof v === 'object' && !Array.isArray(v);
}
//# sourceMappingURL=state.js.map