export interface EffectEntry {
    at: string;
    skill: string;
    task: string;
    triggered: boolean;
    used: boolean;
    outcome: 'pos' | 'neu' | 'neg';
    note: string;
}
export interface EffectStatsRow {
    skill: string;
    total: number;
    triggered: number;
    used: number;
    pos: number;
    neu: number;
    neg: number;
}
export declare function effectLogPath(): string;
export declare function loadEffects(file?: string): EffectEntry[];
export declare function saveEffects(entries: EffectEntry[], file?: string): void;
export declare function recordEffect(input: Omit<EffectEntry, 'at'>, file?: string): EffectEntry;
export declare function effectStats(entries: EffectEntry[]): EffectStatsRow[];
