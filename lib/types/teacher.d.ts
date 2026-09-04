export declare const TEACHER_PERSONA_TYPE = "public-figure-style-reference";
export declare const TEACHER_GAP_FALLBACK: {
    type: string;
    question: string;
    options: string[];
};
export interface TeacherDomain {
    id: string;
    name: string;
    confidence?: string;
    status?: string;
}
export interface TeacherExpert {
    id: string;
    name: string;
    displayName: string;
    role?: string;
    persona_type: string;
    style?: string;
    position?: string;
    displayNameZh?: string;
    fame?: string;
    sourceRefs: string[];
    status: string;
}
export interface TeacherSpeak {
    expert_id: string;
    expert_name: string;
    persona_type: string;
    stance: string;
    claims?: string[];
    style_inference?: boolean;
    sourceRefs?: string[];
}
export interface TeacherClaimSide {
    expert_id: string;
    expert_name: string;
    stance: string;
    reason?: string;
}
export interface TeacherConflict {
    conflict_id: string;
    topic: string;
    claim_a: TeacherClaimSide;
    claim_b: TeacherClaimSide;
    aligned_expert_ids?: string[];
    aligned_expert_names?: string[];
    sources?: string[];
    resolution?: TeacherAdjudication | null;
}
export interface TeacherAdjudication {
    conflict_id: string;
    adjudicator: string;
    decision: 'adopt_a' | 'adopt_b' | 'merge' | 'reject' | 'defer';
    reason?: string;
    adjudicated_at?: string;
}
export interface TeacherConclusion {
    conclusion_id: string;
    round: number;
    expert_id: string;
    expert_name: string;
    persona_type: string;
    text: string;
    sourceRefs: string[];
    decision?: string;
    adjudicated_by?: string;
}
export interface TeacherRound {
    round: number;
    topic: string;
    status: 'collecting' | 'adjudicated';
    speaks: TeacherSpeak[];
    conflicts: TeacherConflict[];
    adjudications: TeacherAdjudication[];
    conclusions: TeacherConclusion[];
}
export interface TeacherDiscussionState {
    status: 'active' | 'finished' | 'expert_gap';
    current_round: number;
    rounds: TeacherRound[];
    gap_fallback: Record<string, unknown> | null;
}
export interface TeacherSession {
    mode: 'teacher';
    session_id: string;
    domain: TeacherDomain | null;
    experts: TeacherExpert[];
    discussion: TeacherDiscussionState;
    created_at: string;
    updated_at: string;
}
export interface TeacherRoundInput {
    topic: string;
    speaks?: TeacherSpeak[];
    conflicts?: TeacherConflict[];
    adjudications?: TeacherAdjudication[];
    conclusions?: TeacherConclusion[];
}
export declare class TeacherDiscussionStore {
    private readonly sessions;
    private latestId;
    /** 从用户自然语言识别领域并创建讨论会话。 */
    startFromText(text: string, expertIds?: string[], opts?: {
        adjacent?: boolean;
    }): TeacherSession;
    /** 直接指定领域创建讨论会话。 */
    startFromDomain(domainId: string, expertIds?: string[], opts?: {
        adjacent?: boolean;
    }): TeacherSession;
    /** 手工创建（测试/未来 UI 用）。 */
    create(input: {
        session_id?: string;
        domain: TeacherDomain | null;
        experts?: TeacherExpert[];
        gapFallback?: Record<string, unknown> | null;
    }): TeacherSession;
    /** 选择/替换当前会话的 ready 专家子集。 */
    selectExperts(sessionId: string, expertIds: string[]): TeacherSession;
    /** 追加一轮完整讨论。 */
    addRound(sessionId: string, input: TeacherRoundInput): TeacherSession;
    /** 结束会话。 */
    finish(sessionId: string): TeacherSession;
    get(sessionId?: string): TeacherSession | undefined;
    list(): TeacherSession[];
    /** 侧边栏/API 读取用：返回当前会话 + 全量会话列表。 */
    payload(sessionId?: string): {
        sessions: TeacherSession[];
        current: TeacherSession | null;
    };
    has(sessionId: string): boolean;
    private mustGet;
}
/** 单例：进程内共享当前教师讨论状态。 */
export declare const teacherStore: TeacherDiscussionStore;
