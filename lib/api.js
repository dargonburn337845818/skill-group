import { domainStatusPayload, recognizeDomain } from './domain.js';
import { teacherStore } from './teacher.js';
export function registerApi(ctx, manager) {
    const webserver = ctx.get('webServer');
    if (!webserver)
        return;
    const readBody = async (req) => {
        const chunks = [];
        for await (const chunk of req)
            chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)));
        return Buffer.concat(chunks).toString('utf8');
    };
    const send = (res, code, obj) => {
        res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(obj));
    };
    ctx.effect(() => webserver.register({
        kind: 'prefix',
        path: '/skill-vault/api',
        handler: async (req, res) => {
            try {
                const pathname = new URL(req.url ?? '/', 'http://localhost').pathname;
                const path = pathname.replace(/^\/skill-vault\/api/, '') || '/';
                if (req.method === 'GET' && path === '/list') {
                    return send(res, 200, { ok: true, entries: manager.list(), scenarios: manager.scenarios() });
                }
                if ((req.method === 'POST' && (path === '/enable' || path === '/disable')) || (req.method === 'POST' && path === '/toggle')) {
                    const body = JSON.parse(await readBody(req));
                    const target = String(body.target ?? '').trim();
                    if (!target)
                        return send(res, 400, { ok: false, error: 'target 必填' });
                    const scope = body.scope === 'session' ? 'session' : 'global';
                    const enabled = path === '/enable' ? true : path === '/disable' ? false : !!body.enabled;
                    const result = manager.set(target, enabled, scope);
                    return send(res, result.ok ? 200 : 404, { ok: result.ok, type: result.type, target: result.target, scope });
                }
                if (req.method === 'POST' && path === '/route') {
                    const body = JSON.parse(await readBody(req));
                    const scope = body.scope === 'global' ? 'global' : 'session';
                    const enable = Array.isArray(body.enable) ? body.enable.map(String) : [];
                    const disable = Array.isArray(body.disable) ? body.disable.map(String) : [];
                    const actions = [
                        ...enable.map((target) => ({ target, enabled: true, scope })),
                        ...disable.map((target) => ({ target, enabled: false, scope })),
                    ];
                    const results = manager.setMany(actions);
                    const failed = results.filter((r) => !r.ok);
                    return send(res, failed.length ? 404 : 200, { ok: failed.length === 0, results, failed });
                }
                if (req.method === 'POST' && path === '/reset-base') {
                    const body = JSON.parse(await readBody(req));
                    const baseIds = Array.isArray(body.baseIds) && body.baseIds.length ? body.baseIds.map(String) : manager.baseIds();
                    manager.resetToBase(baseIds);
                    return send(res, 200, { ok: true, baseIds, entries: manager.list(), scenarios: manager.scenarios() });
                }
                if (req.method === 'GET' && path === '/domain') {
                    const url = new URL(req.url ?? '/', 'http://localhost');
                    const text = url.searchParams.get('text') || '';
                    if (!text.trim())
                        return send(res, 400, { ok: false, error: 'text 必填' });
                    const out = recognizeDomain(text);
                    if (!out.ok)
                        return send(res, 500, { ok: false, error: out.error });
                    return send(res, 200, { ok: true, ...out.result });
                }
                if (req.method === 'GET' && path === '/domain/status') {
                    return send(res, 200, { ok: true, ...domainStatusPayload() });
                }
                if (req.method === 'GET' && (path === '/teacher/status' || path === '/expert-team/status')) {
                    const url = new URL(req.url ?? '/', 'http://localhost');
                    const sessionId = url.searchParams.get('session_id') || undefined;
                    const payload = teacherStore.payload(sessionId);
                    return send(res, 200, { ok: true, ...payload });
                }
                if (req.method === 'POST' && (path === '/teacher/start' || path === '/expert-team/start')) {
                    const body = JSON.parse(await readBody(req));
                    const expertIds = Array.isArray(body.expert_ids) ? body.expert_ids.map(String) : undefined;
                    const opts = { adjacent: Boolean(body.adjacent) };
                    let session;
                    if (body.text && String(body.text).trim()) {
                        session = teacherStore.startFromText(String(body.text), expertIds, opts);
                    }
                    else if (body.domain_id && String(body.domain_id).trim()) {
                        session = teacherStore.startFromDomain(String(body.domain_id), expertIds, opts);
                    }
                    else {
                        return send(res, 400, { ok: false, error: 'text 或 domain_id 必填' });
                    }
                    return send(res, 200, { ok: true, session });
                }
                if (req.method === 'POST' && (path === '/teacher/round' || path === '/expert-team/round')) {
                    const body = JSON.parse(await readBody(req));
                    const session = teacherStore.addRound(String(body.session_id), body);
                    return send(res, 200, { ok: true, session });
                }
                if (req.method === 'POST' && (path === '/teacher/select' || path === '/expert-team/select')) {
                    const body = JSON.parse(await readBody(req));
                    if (!body.session_id)
                        return send(res, 400, { ok: false, error: 'session_id 必填' });
                    const session = teacherStore.selectExperts(String(body.session_id), Array.isArray(body.expert_ids) ? body.expert_ids.map(String) : []);
                    return send(res, 200, { ok: true, session });
                }
                if (req.method === 'POST' && (path === '/teacher/finish' || path === '/expert-team/finish')) {
                    const body = JSON.parse(await readBody(req));
                    if (!body.session_id)
                        return send(res, 400, { ok: false, error: 'session_id 必填' });
                    const session = teacherStore.finish(String(body.session_id));
                    return send(res, 200, { ok: true, session });
                }
                return send(res, 404, { ok: false, error: 'not found: ' + path });
            }
            catch (e) {
                return send(res, 500, { ok: false, error: String(e) });
            }
        },
    }), 'skill-vault: api');
}
//# sourceMappingURL=api.js.map