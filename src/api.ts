/**
 * Web API for the skill-vault UI panel.
 *
 * Endpoints (mounted under /skill-vault/api):
 *   GET  /list                          — catalog + effective switch state
 *   POST /enable   { target, scope }    — enable skill/scenario
 *   POST /disable  { target, scope }    — disable skill/scenario
 */
import type { IncomingMessage, ServerResponse } from 'node:http'
import type { Context } from 'cordis'
import type { SkillVaultManager } from './manager.js'
import type { SwitchScope } from './types.js'

export function registerApi(ctx: Context, manager: SkillVaultManager): void {
  const webserver = ctx.get('webServer')
  if (!webserver) return

  const readBody = async (req: IncomingMessage): Promise<string> => {
    const chunks: Buffer[] = []
    for await (const chunk of req) chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)))
    return Buffer.concat(chunks).toString('utf8')
  }

  const send = (res: ServerResponse, code: number, obj: unknown): void => {
    res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' })
    res.end(JSON.stringify(obj))
  }

  ctx.effect(() => webserver.register({
    kind: 'prefix',
    path: '/skill-vault/api',
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      try {
        const pathname = new URL(req.url ?? '/', 'http://localhost').pathname
        const path = pathname.replace(/^\/skill-vault\/api/, '') || '/'
        if (req.method === 'GET' && path === '/list') {
          return send(res, 200, { ok: true, entries: manager.list(), scenarios: manager.scenarios() })
        }
        if ((req.method === 'POST' && (path === '/enable' || path === '/disable')) || (req.method === 'POST' && path === '/toggle')) {
          const body = JSON.parse(await readBody(req)) as { target?: string; scope?: string; enabled?: boolean }
          const target = String(body.target ?? '').trim()
          if (!target) return send(res, 400, { ok: false, error: 'target 必填' })
          const scope: SwitchScope = body.scope === 'session' ? 'session' : 'global'
          const enabled = path === '/enable' ? true : path === '/disable' ? false : !!body.enabled
          const result = manager.set(target, enabled, scope)
          return send(res, result.ok ? 200 : 404, { ok: result.ok, type: result.type, target: result.target, scope })
        }
        return send(res, 404, { ok: false, error: 'not found: ' + path })
      } catch (e) {
        return send(res, 500, { ok: false, error: String(e) })
      }
    },
  }), 'skill-vault: api')
}
