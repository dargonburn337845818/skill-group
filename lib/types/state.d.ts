import type { SessionSwitchState, SwitchState } from './types.js';
export declare function emptyPersistedState(): SwitchState;
export declare function emptySessionState(): SessionSwitchState;
export declare function loadPersistedState(dataDir: string): SwitchState;
export declare function savePersistedState(dataDir: string, state: SwitchState): void;
export declare function clonePersistedState(state: SwitchState): SwitchState;
