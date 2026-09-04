/**
 * dsh-skill-vault — shared types.
 *
 * This module defines the immutable catalog entry and the persisted/session
 * switch state shapes. The vault's on-disk manifest is the source of truth for
 * metadata; this file only mirrors it in memory.
 */
export interface QualityCriteria {
    high?: string[];
    reject?: string[];
    minIndependentSources?: number;
    notes?: string;
}
export interface SkillManifest {
    id: string;
    name?: string;
    title?: string;
    description: string;
    whenToUse?: string;
    boundary?: string;
    notWhenToUse?: string;
    scenario: string;
    scenarios?: string[];
    routing?: 'base' | 'core' | 'domain';
    qualityCriteria?: QualityCriteria;
    tags?: string[];
    experts?: string[];
    sourceRefs?: string[];
    activation?: 'catalog' | 'always-on' | 'internal';
    hidden?: boolean;
    version?: string;
    license?: string;
}
export interface SkillEntry {
    id: string;
    name: string;
    title: string;
    description: string;
    whenToUse?: string;
    boundary?: string;
    notWhenToUse?: string;
    scenario: string;
    scenarioTitle: string;
    routing: 'base' | 'core' | 'domain';
    qualityCriteria?: QualityCriteria;
    tags: string[];
    experts: string[];
    sourceRefs: string[];
    activation: 'catalog' | 'always-on' | 'internal';
    hidden: boolean;
    version: string;
    license?: string;
    /** Absolute directory of the skill package. */
    dir: string;
    /** Absolute path to SKILL.md. Empty until loaded. */
    skillPath: string;
    /** Markdown body, loaded lazily for registration. */
    content: string;
}
export interface SwitchState {
    scenarios: Record<string, boolean>;
    skills: Record<string, boolean>;
}
export interface PersistedStateFile {
    version: 1;
    scenarios?: Record<string, boolean>;
    skills?: Record<string, boolean>;
}
export interface SessionSwitchState {
    scenarios: Map<string, boolean>;
    skills: Map<string, boolean>;
}
export type SwitchScope = 'global' | 'session';
export interface CatalogRow {
    id: string;
    name: string;
    title: string;
    description: string;
    whenToUse?: string;
    boundary?: string;
    notWhenToUse?: string;
    scenario: string;
    scenarioTitle: string;
    routing: string;
    qualityCriteria?: QualityCriteria;
    tags: string[];
    experts: string[];
    sourceRefs: string[];
    activation: string;
    hidden: boolean;
    version: string;
    enabled: boolean;
    persistentEnabled: boolean;
    sessionEnabled: boolean;
}
