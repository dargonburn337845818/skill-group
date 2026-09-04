/**
 * dsh-skill-vault — 教师模块运行时：回合式讨论会话。
 *
 * 职责：
 *   1. 从领域识别器/domain-profiles 加载“具体人名专家团”；
 *   2. 保存一个或多个回合式讨论会话（独立表态 / 冲突点 / 裁决 / 结论）；
 *   3. 给 agent 工具与 Web API 输出稳定 JSON，供侧边栏过程监视器只读展示。
 *
 * 纪律：
 *   - 只使用 EXPERT_LIBRARY 中 persona_type=public-figure-style-reference 的 ready 专家；
 *   - 无 ready 专家时进入 expert_gap，不静默降级；
 *   - 不伪造专家原话；speaks/conflicts 由调用方按来源与风格推断传入。
 */
import { listDomainProfiles, listExpertLibrary, recognizeDomain } from './domain.js';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const PLUGIN_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const TEACHER_PERSONA_TYPE = 'public-figure-style-reference';
export const TEACHER_GAP_FALLBACK = {
    type: 'ask_user',
    question: '该领域暂无已备好的人名专家：要我蒸馏该领域专家团，还是放弃专家团、直接用大模型解答？',
    options: ['distill_expert', 'use_llm_directly'],
};
function nowIso() {
    return new Date().toISOString();
}
/** 读取专家包（vault/expert-packs/<id>/POSITION.md），用作讨论时的蒸馏支撑。 */
function loadExpertPosition(expertId) {
    try {
        const p = join(PLUGIN_ROOT, 'vault', 'expert-packs', expertId, 'POSITION.md');
        if (!existsSync(p))
            return undefined;
        const text = readFileSync(p, 'utf8');
        return text.length > 6000 ? text.slice(0, 6000) + '\n...（截断）' : text;
    }
    catch {
        return undefined;
    }
}
function normalizeExpert(raw) {
    const id = String(raw?.id ?? '');
    return {
        id,
        name: String(raw?.name ?? ''),
        displayName: String(raw?.displayName ?? raw?.name ?? raw?.id ?? ''),
        role: raw?.role ? String(raw.role) : undefined,
        persona_type: String(raw?.persona_type ?? TEACHER_PERSONA_TYPE),
        style: raw?.style ? String(raw.style) : undefined,
        position: loadExpertPosition(id),
        displayNameZh: raw?.displayNameZh ? String(raw.displayNameZh) : undefined,
        fame: raw?.fame ? String(raw.fame) : undefined,
        sourceRefs: Array.isArray(raw?.sourceRefs) ? raw.sourceRefs.map(String) : [],
        status: String(raw?.status ?? ''),
    };
}
function isReadyExpert(expert) {
    return expert?.status === 'ready'
        && expert?.persona_type === TEACHER_PERSONA_TYPE
        && Array.isArray(expert?.sourceRefs)
        && expert.sourceRefs.length > 0;
}
function filterExpertIds(experts, ids) {
    if (!ids || ids.length === 0)
        return experts;
    const set = new Set(ids.map(String));
    const picked = experts.filter((e) => set.has(e.id) || set.has(e.name));
    return picked.length > 0 ? picked : experts;
}
/** 按领域从 EXPERT_LIBRARY 取 ready 专家（供主领域/邻近领域复用）。 */
function readyExpertsForDomain(domainId, profiles, library) {
    const profile = profiles.find((d) => d?.id === domainId);
    if (!profile)
        return [];
    const refs = Array.isArray(profile?.expert_ids) ? profile.expert_ids : [];
    return refs
        .map((id) => library.find((e) => e?.id === id))
        .filter(Boolean)
        .filter(isReadyExpert)
        .map(normalizeExpert);
}
/** 引入邻近领域 ready 专家（跨领域只取邻近，不拉全库）。 */
function adjacentExpertsForDomain(domainId, profiles, library) {
    const profile = profiles.find((d) => d?.id === domainId);
    const adjacent = Array.isArray(profile?.adjacent) ? profile.adjacent : [];
    const out = [];
    const seen = new Set();
    for (const adjId of adjacent) {
        for (const e of readyExpertsForDomain(String(adjId), profiles, library)) {
            if (!seen.has(e.id)) {
                seen.add(e.id);
                out.push(e);
            }
        }
    }
    return out;
}
export class TeacherDiscussionStore {
    sessions = new Map();
    latestId = null;
    /** 从用户自然语言识别领域并创建讨论会话。 */
    startFromText(text, expertIds, opts) {
        const out = recognizeDomain(text);
        if (!out.ok)
            throw new Error(out.error || '领域识别失败');
        const r = out.result;
        const domain = r?.domain
            ? {
                id: String(r.domain.id),
                name: String(r.domain.name),
                confidence: r.domain.confidence ? String(r.domain.confidence) : undefined,
                status: r.domain.status ? String(r.domain.status) : undefined,
            }
            : null;
        let experts = (Array.isArray(r?.experts) ? r.experts : []).map(normalizeExpert);
        const fallback = r?.fallback && typeof r.fallback === 'object' ? r.fallback : null;
        if (opts?.adjacent && domain) {
            const profiles = listDomainProfiles();
            const library = listExpertLibrary();
            const seen = new Set(experts.map((e) => e.id));
            for (const e of adjacentExpertsForDomain(domain.id, profiles, library)) {
                if (!seen.has(e.id)) {
                    seen.add(e.id);
                    experts.push(e);
                }
            }
        }
        return this.create({ domain, experts: filterExpertIds(experts, expertIds), gapFallback: fallback });
    }
    /** 直接指定领域创建讨论会话。 */
    startFromDomain(domainId, expertIds, opts) {
        const profiles = listDomainProfiles();
        const profile = profiles.find((d) => d?.id === domainId);
        if (!profile)
            throw new Error(`domain not found: ${domainId}`);
        const library = listExpertLibrary();
        const candidates = readyExpertsForDomain(domainId, profiles, library);
        const combined = opts?.adjacent ? [...candidates, ...adjacentExpertsForDomain(domainId, profiles, library)] : candidates;
        const domain = {
            id: String(profile.id),
            name: String(profile.name || profile.id),
            confidence: 'high',
            status: String(profile.status || 'unknown'),
        };
        return this.create({
            domain,
            experts: filterExpertIds(combined, expertIds),
            gapFallback: candidates.length > 0 ? null : { ...TEACHER_GAP_FALLBACK },
        });
    }
    /** 手工创建（测试/未来 UI 用）。 */
    create(input) {
        const id = input.session_id || `teacher_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        const session = {
            mode: 'teacher',
            session_id: id,
            domain: input.domain,
            experts: input.experts || [],
            discussion: {
                status: input.gapFallback ? 'expert_gap' : 'active',
                current_round: 0,
                rounds: [],
                gap_fallback: input.gapFallback || null,
            },
            created_at: nowIso(),
            updated_at: nowIso(),
        };
        this.sessions.set(id, session);
        this.latestId = id;
        return session;
    }
    /** 选择/替换当前会话的 ready 专家子集。 */
    selectExperts(sessionId, expertIds) {
        const session = this.mustGet(sessionId);
        if (!session.domain)
            throw new Error('session.domain missing; cannot select experts');
        const profile = listDomainProfiles().find((d) => d?.id === session.domain?.id);
        if (!profile)
            throw new Error(`domain profile not found: ${session.domain.id}`);
        const library = listExpertLibrary();
        const refs = Array.isArray(profile?.expert_ids) ? profile.expert_ids : [];
        const all = refs
            .map((id) => library.find((e) => e?.id === id))
            .filter(Boolean)
            .filter(isReadyExpert)
            .map(normalizeExpert);
        session.experts = filterExpertIds(all, expertIds);
        session.updated_at = nowIso();
        return session;
    }
    /** 追加一轮完整讨论。 */
    addRound(sessionId, input) {
        const session = this.mustGet(sessionId);
        if (session.discussion.status === 'expert_gap') {
            throw new Error('session is expert_gap; 请先选择蒸馏专家团或放弃专家团');
        }
        if (session.discussion.status === 'finished') {
            throw new Error('session already finished');
        }
        const roundNo = session.discussion.current_round + 1;
        const hasDecision = Boolean(input.adjudications?.length) || Boolean(input.conclusions?.length);
        const round = {
            round: roundNo,
            topic: input.topic,
            status: hasDecision ? 'adjudicated' : 'collecting',
            speaks: input.speaks || [],
            conflicts: input.conflicts || [],
            adjudications: input.adjudications || [],
            conclusions: input.conclusions || [],
        };
        session.discussion.rounds.push(round);
        session.discussion.current_round = roundNo;
        session.discussion.status = 'active';
        session.updated_at = nowIso();
        return session;
    }
    /** 结束会话。 */
    finish(sessionId) {
        const session = this.mustGet(sessionId);
        session.discussion.status = 'finished';
        session.updated_at = nowIso();
        return session;
    }
    get(sessionId) {
        const id = sessionId || this.latestId || undefined;
        if (!id)
            return undefined;
        return this.sessions.get(id);
    }
    list() {
        return [...this.sessions.values()];
    }
    /** 侧边栏/API 读取用：返回当前会话 + 全量会话列表。 */
    payload(sessionId) {
        const current = this.get(sessionId) || null;
        return { sessions: this.list(), current };
    }
    has(sessionId) {
        return this.sessions.has(sessionId);
    }
    mustGet(sessionId) {
        const session = this.sessions.get(sessionId);
        if (!session)
            throw new Error(`teacher session not found: ${sessionId}`);
        return session;
    }
}
/** 单例：进程内共享当前教师讨论状态。 */
export const teacherStore = new TeacherDiscussionStore();
//# sourceMappingURL=teacher.js.map