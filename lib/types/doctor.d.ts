export interface DoctorIssue {
    skill: string;
    ok: boolean;
    issues: string[];
    warnings: string[];
}
/** Run doctor across the public catalog under vaultRoot/skills. */
export declare function runDoctor(vaultRoot: string): DoctorIssue[];
