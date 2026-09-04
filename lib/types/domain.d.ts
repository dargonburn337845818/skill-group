/** 调用 Python 领域识别器，返回稳定 JSON 结果（含专家团/缺口分支）。 */
export declare function recognizeDomain(text: string): {
    ok: boolean;
    result?: unknown;
    error?: string;
};
/** 领域字典（供侧边栏展示预置领域状态）。 */
export declare function listDomainProfiles(): unknown[];
/** 统一人名专家库（供侧边栏展示专家/缺口状态）。 */
export declare function listExpertLibrary(): unknown[];
/** 一次拿全侧边栏需要的领域/专家状态数据。 */
export declare function domainStatusPayload(): Record<string, unknown>;
