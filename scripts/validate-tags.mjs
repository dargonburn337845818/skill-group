#!/usr/bin/env node
// Tag taxonomy validator for dsh-skill-vault.
// Usage: node scripts/validate-tags.mjs
// Rules (vault/TAG_TAXONOMY.md):
//   - tags must be an array of non-empty strings
//   - tags <= 8
//   - status/lifecycle words are forbidden
import { readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(fileURLToPath(new URL('..', import.meta.url)), 'vault', 'skills')

const FORBIDDEN = new Set(['已蒸馏', '已填充', '挂载', '底座挂载', 'done', 'pending', 'in_progress'])

function walk(dir) {
  const out = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name)
    if (entry.isDirectory()) out.push(...walk(p))
    else if (entry.name === 'manifest.json') out.push(p)
  }
  return out
}

const manifests = walk(root)
const errors = []
let count = 0

for (const file of manifests) {
  let m
  try {
    m = JSON.parse(readFileSync(file, 'utf8'))
  } catch (e) {
    errors.push(`${file}: invalid JSON (${String(e)})`)
    continue
  }
  if (!Array.isArray(m.tags)) {
    errors.push(`${file}: tags must be an array`)
    continue
  }
  count++
  if (m.tags.length > 8) {
    errors.push(`${file}: ${m.id || '?'} has ${m.tags.length} tags (max 8)`)
  }
  for (const t of m.tags) {
    if (typeof t !== 'string' || !t.trim()) {
      errors.push(`${file}: empty/non-string tag ${JSON.stringify(t)}`)
    } else if (FORBIDDEN.has(t.trim())) {
      errors.push(`${file}: forbidden status tag "${t.trim()}"`)
    }
  }
}

if (errors.length) {
  console.error(`Tag validation FAILED: ${errors.length} problem(s)`)
  for (const e of errors) console.error('- ' + e)
  process.exit(1)
}
console.log(`OK: ${count} manifest(s) tag-validated`)
