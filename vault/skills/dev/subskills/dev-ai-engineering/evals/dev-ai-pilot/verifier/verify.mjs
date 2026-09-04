import fs from 'node:fs';
const out = fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8');
const required = ['上下文预算', 'RAG', '评测', '降级', 'CHECKLIST_OK'];
const missing = required.filter(s => !out.includes(s));
if (missing.length) {
  process.stdout.write('FAIL missing: ' + missing.join(',') + '\n');
  process.exit(1);
}
process.stdout.write('PASS\n');
process.exit(0);
