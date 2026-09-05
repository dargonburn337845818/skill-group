import type { EffectEntry } from './effects.js';
import type { DoctorIssue } from './doctor.js';
import type { CatalogRow } from './types.js';
export interface GovernanceAction {
    action: 'keep' | 'enable' | 'disable_or_demote' | 'reduce_trigger' | 'fix' | 'no_data' | 'merge_candidate' | 'flow_control';
    reason: string;
}
export interface SkillGovernanceRow {
    skill: string;
    scenario: string;
    enabled: boolean;
    total: number;
    triggered: number;
    used: number;
    pos: number;
    neu: number;
    neg: number;
    effectRate: number;
    misuseRate: number;
    lastAt: string | null;
    doctorOk: boolean;
    doctorIssues: string[];
    doctorWarnings: string[];
    openChange: boolean;
    actions: GovernanceAction[];
}
export interface GovernanceReport {
    at: string;
    enabledCount: number;
    catalogCount: number;
    totalEntries: number;
    effectLogPath: string;
    doctor: {
        ok: boolean;
        pass: number;
        total: number;
    };
    openChanges: string[];
    rows: SkillGovernanceRow[];
    summary: string;
}
export interface OpenChangesFile {
    version?: number;
    open?: string[];
    changes?: Array<{
        skill: string;
        branch?: string;
        pr?: string;
        openedAt?: string;
    }>;
}
export declare function loadOpenChanges(file?: string): string[];
export declare function rowDefault(skill: string, enabled: boolean, scenario: string): SkillGovernanceRow;
export declare function buildGovernanceReport(args: {
    catalog: CatalogRow[];
    effects?: EffectEntry[];
    doctorResults?: DoctorIssue[];
    openChanges?: string[];
    effectPath?: string;
    openChangesFile?: string;
}): GovernanceReport;
