import test from 'node:test'
import assert from 'node:assert/strict'
import { registerApi } from '../lib/api.js'

function makeHandler() {
  let captured
  const webserver = {
    register(opts) {
      captured = opts
      return () => undefined
    },
  }
  const ctx = {
    effect(fn) {
      fn()
      return () => undefined
    },
    get(key) {
      return key === 'webServer' ? webserver : undefined
    },
  }
  registerApi(ctx, {})
  return captured.handler
}

async function call(handler, method, path, body) {
  const chunks = body ? [Buffer.from(JSON.stringify(body))] : []
  const req = {
    method,
    url: path,
    [Symbol.asyncIterator]: async function* () {
      for (const c of chunks) yield c
    },
  }
  let statusCode = 0
  let payload
  const res = {
    writeHead(code) {
      statusCode = code
    },
    end(text) {
      payload = JSON.parse(text)
    },
  }
  await handler(req, res)
  return { statusCode, payload }
}

test('teacher/status returns empty payload before any session', async () => {
  const handler = makeHandler()
  const { payload } = await call(handler, 'GET', '/teacher/status')
  assert.equal(payload.ok, true)
  assert.deepEqual(payload.sessions, [])
  assert.equal(payload.current, null)
})

test('teacher/start + round + status form a usable discussion session', async () => {
  const handler = makeHandler()
  const started = await call(handler, 'POST', '/teacher/start', { domain_id: 'algorithm' })
  assert.equal(started.statusCode, 200)
  const session = started.payload.session
  assert.ok(session.experts.length >= 2)
  assert.equal(session.discussion.status, 'active')

  const round = await call(handler, 'POST', '/teacher/round', {
    session_id: session.session_id,
    topic: '先暴力还是先建模',
    speaks: [
      { expert_id: 'tourist', expert_name: 'Tourist', persona_type: 'public-figure-style-reference', stance: '先写基线' },
      { expert_id: 'um-nik', expert_name: 'Um_nik', persona_type: 'public-figure-style-reference', stance: '先重述模型' },
    ],
    conflicts: [
      {
        conflict_id: 'c1',
        topic: '先暴力还是先建模',
        claim_a: { expert_id: 'tourist', expert_name: 'Tourist', stance: '先写基线' },
        claim_b: { expert_id: 'um-nik', expert_name: 'Um_nik', stance: '先重述模型' },
      },
    ],
    adjudications: [{ conflict_id: 'c1', adjudicator: 'user', decision: 'merge' }],
    conclusions: [
      {
        conclusion_id: 'concl_1',
        round: 1,
        expert_id: 'tourist',
        expert_name: 'Tourist',
        persona_type: 'public-figure-style-reference',
        text: '先写基线',
        sourceRefs: [],
      },
    ],
  })
  assert.equal(round.statusCode, 200)
  assert.equal(round.payload.session.discussion.rounds.length, 1)

  const status = await call(handler, 'GET', `/teacher/status?session_id=${session.session_id}`)
  assert.equal(status.statusCode, 200)
  assert.equal(status.payload.current.session_id, session.session_id)
  assert.equal(status.payload.current.discussion.rounds[0].speaks.length, 2)
})

test('teacher/start loads ready frontend team', async () => {
  const handler = makeHandler()
  const { payload } = await call(handler, 'POST', '/teacher/start', { domain_id: 'frontend' })
  assert.equal(payload.session.discussion.status, 'active')
  assert.ok(payload.session.experts.some((e) => e.id === 'evan-you'))
})
