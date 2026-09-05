import test from 'node:test'
import assert from 'node:assert/strict'
import { buildGovernanceReport } from '../lib/governance.js'

function cat(id, enabled = false, scenario = 'base') {
  return { id, enabled, scenario }
}

test('no runtime data yields no_data and never enables blindly', () => {
  const report = buildGovernanceReport({
    catalog: [cat('alpha', true), cat('beta', false)],
    effects: [],
    doctorResults: [],
    openChanges: [],
  })
  const alpha = report.rows.find((r) => r.skill === 'alpha')
  const beta = report.rows.find((r) => r.skill === 'beta')
  assert.ok(alpha.actions.some((a) => a.action === 'no_data'))
  assert.ok(beta.actions.some((a) => a.action === 'no_data'))
  assert.ok(!beta.actions.some((a) => a.action === 'enable'))
  assert.equal(report.enabledCount, 1)
})

test('positive evidence on disabled skill suggests enable', () => {
  const effects = [
    { at: '2026-01-01T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
    { at: '2026-01-02T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
    { at: '2026-01-03T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
  ]
  const report = buildGovernanceReport({
    catalog: [cat('beta', false)],
    effects,
    doctorResults: [],
    openChanges: [],
  })
  const row = report.rows[0]
  assert.ok(row.actions.some((a) => a.action === 'enable'))
})

test('poor effect on enabled skill suggests disable_or_demote', () => {
  const effects = [
    { at: '2026-01-01T00:00:00Z', skill: 'alpha', task: 't', triggered: true, used: false, outcome: 'neg', note: '' },
    { at: '2026-01-02T00:00:00Z', skill: 'alpha', task: 't', triggered: true, used: false, outcome: 'neg', note: '' },
    { at: '2026-01-03T00:00:00Z', skill: 'alpha', task: 't', triggered: true, used: false, outcome: 'neg', note: '' },
  ]
  const report = buildGovernanceReport({
    catalog: [cat('alpha', true)],
    effects,
    doctorResults: [],
    openChanges: [],
  })
  const row = report.rows[0]
  assert.ok(row.actions.some((a) => a.action === 'disable_or_demote'))
  assert.ok(row.misuseRate > 0.3)
})

test('open change suppresses actionable suggestions', () => {
  const effects = [
    { at: '2026-01-01T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
    { at: '2026-01-02T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
    { at: '2026-01-03T00:00:00Z', skill: 'beta', task: 't', triggered: true, used: true, outcome: 'pos', note: '' },
  ]
  const report = buildGovernanceReport({
    catalog: [cat('beta', false)],
    effects,
    doctorResults: [],
    openChanges: ['beta'],
  })
  const row = report.rows[0]
  assert.deepEqual(row.actions.map((a) => a.action), ['flow_control'])
})

test('doctor issues produce fix action', () => {
  const report = buildGovernanceReport({
    catalog: [cat('gamma', true)],
    effects: [],
    doctorResults: [{ skill: 'gamma', ok: false, issues: ['missing SKILL.md'], warnings: [] }],
    openChanges: [],
  })
  const row = report.rows[0]
  assert.ok(row.actions.some((a) => a.action === 'fix'))
})
