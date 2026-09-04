import test from 'node:test'
import assert from 'node:assert/strict'
import { TeacherDiscussionStore } from '../lib/teacher.js'

test('startFromText loads ready algorithm expert team', () => {
  const store = new TeacherDiscussionStore()
  const s = store.startFromText('这道算法竞赛题 dp 怎么写')
  assert.equal(s.mode, 'teacher')
  assert.equal(s.discussion.status, 'active')
  assert.ok(s.experts.length >= 2)
  assert.ok(s.experts.some((e) => e.id === 'tourist'))
  assert.ok(s.experts.every((e) => e.persona_type === 'public-figure-style-reference'))
})

test('startFromDomain loads ready frontend team', () => {
  const store = new TeacherDiscussionStore()
  const s = store.startFromDomain('frontend')
  assert.equal(s.discussion.status, 'active')
  assert.ok(s.experts.some((e) => e.id === 'evan-you'))
  assert.ok(s.experts.every((e) => e.persona_type === 'public-figure-style-reference'))
})

test('create with gapFallback returns expert_gap', () => {
  const store = new TeacherDiscussionStore()
  const s = store.create({
    domain: { id: 'empty-domain', name: '空领域' },
    experts: [],
    gapFallback: { type: 'ask_user', question: '没有专家', options: ['distill_expert', 'use_llm_directly'] },
  })
  assert.equal(s.discussion.status, 'expert_gap')
  assert.equal(s.experts.length, 0)
  assert.ok(s.discussion.gap_fallback)
})

test('addRound appends speaks/conflicts/adjudications/conclusions', () => {
  const store = new TeacherDiscussionStore()
  const s = store.startFromDomain('algorithm')
  const out = store.addRound(s.session_id, {
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
    adjudications: [{ conflict_id: 'c1', adjudicator: 'user', decision: 'merge', reason: '合并' }],
    conclusions: [
      { conclusion_id: 'concl_1', round: 1, expert_id: 'tourist', expert_name: 'Tourist', persona_type: 'public-figure-style-reference', text: '先写基线', sourceRefs: [] },
    ],
  })
  assert.equal(out.discussion.rounds.length, 1)
  assert.equal(out.discussion.current_round, 1)
  assert.equal(out.discussion.rounds[0].speaks.length, 2)
  assert.equal(out.discussion.rounds[0].conclusions[0].expert_id, 'tourist')
})

test('selectExperts filters the ready team', () => {
  const store = new TeacherDiscussionStore()
  const s = store.startFromDomain('algorithm')
  const out = store.selectExperts(s.session_id, ['tourist'])
  assert.equal(out.experts.length, 1)
  assert.equal(out.experts[0].id, 'tourist')
})

test('finish marks session finished', () => {
  const store = new TeacherDiscussionStore()
  const s = store.startFromDomain('algorithm')
  const out = store.finish(s.session_id)
  assert.equal(out.discussion.status, 'finished')
})
