// Deterministic verifier for expert-decision-enforce
import fs from 'node:fs';
const out = fs.existsSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt') ? fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8') : '';
const rep = fs.existsSync('report.md') ? fs.readFileSync('report.md', 'utf8') : '';
const combined = out + '\n' + rep;
const required = [
  '0 Brief',
  '1 Evidence',
  '3 Conflict',
  '4 Adjudicate',
  '7 Verify',
  'decision_log_entry',
];
const missing = required.filter((m) => !combined.includes(m));
if (missing.length) {
  process.stdout.write(`FAIL missing: ${missing.join(', ')}\n`);
  process.exit(1);
}
if (!fs.existsSync('report.md')) {
  process.stdout.write('FAIL missing report.md\n');
  process.exit(1);
}
process.stdout.write('PASS\n');
process.exit(0);
