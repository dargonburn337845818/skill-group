#!/usr/bin/env node
// Vault validator: ensures the on-disk contract holds before publishing.
// Usage: node scripts/validate-vault.mjs
import { readdirSync, readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(fileURLToPath(new URL('..', import.meta.url)), 'vault')
const skillsRoot = join(root, 'skills')
const errors = []
let count = 0
const FORBIDDEN_TAGS = new Set(['已蒸馏', '已填充', '挂载', '底座挂载', 'done', 'pending', 'in_progress'])

if (!existsSync(skillsRoot)) {
  console.error('vault/skills missing')
  process.exit(1)
}

for (const scenario of readdirSync(skillsRoot, { withFileTypes: true }).filter((d) => d.isDirectory())) {
  const scenarioDir = join(skillsRoot, scenario.name)
  for (const skill of readdirSync(scenarioDir, { withFileTypes: true }).filter((d) => d.isDirectory())) {
    const dir = join(scenarioDir, skill.name)
    // Skip support directories (tools/reports/examples/benchmarks) that are not skill packages.
    if (!existsSync(join(dir, 'SKILL.md')) && !existsSync(join(dir, 'manifest.json'))) continue
    count++
    if (!existsSync(join(dir, 'SKILL.md'))) errors.push(`${scenario.name}/${skill.name}: missing SKILL.md`)
    const manifest = join(dir, 'manifest.json')
    if (!existsSync(manifest)) {
      errors.push(`${scenario.name}/${skill.name}: missing manifest.json`)
      continue
    }
    try {
      const m = JSON.parse(readFileSync(manifest, 'utf8'))
      if (!m.id) errors.push(`${scenario.name}/${skill.name}: manifest.id required`)
      if (!m.description) errors.push(`${scenario.name}/${skill.name}: manifest.description required`)
      if (!m.scenario) errors.push(`${scenario.name}/${skill.name}: manifest.scenario required`)
      if (m.scenario !== scenario.name) errors.push(`${scenario.name}/${skill.name}: manifest.scenario != directory scenario`)
      if (!Array.isArray(m.tags)) errors.push(`${scenario.name}/${skill.name}: manifest.tags must be an array`)
      else {
        if (m.tags.length > 8) errors.push(`${scenario.name}/${skill.name}: tags > 8 (${m.tags.length})`)
        for (const t of m.tags) {
          if (FORBIDDEN_TAGS.has(t)) errors.push(`${scenario.name}/${skill.name}: forbidden tag "${t}"`)
        }
      }
    } catch (e) {
      errors.push(`${scenario.name}/${skill.name}: invalid manifest.json (${String(e)})`)
    }
  }
}

if (errors.length) {
  console.error(`Invalid: ${errors.length} problem(s)`)
  for (const e of errors) console.error('- ' + e)
  process.exit(1)
}
console.log(`OK: ${count} skill(s) validated in vault/skills`)
