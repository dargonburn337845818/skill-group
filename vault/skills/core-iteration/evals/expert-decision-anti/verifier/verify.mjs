// Deterministic anti-trigger verifier: a simple factual question must NOT trigger the full decision loop.
import fs from 'node:fs';
const out = fs.existsSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt') ? fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8') : '';
const forbidden = ['0 Brief', '1 Evidence', '3 Conflict', '4 Adjudicate', 'decision_log_entry'];
const triggered = forbidden.filter((m) => out.includes(m));
if (triggered.length) {
  process.stdout.write(`FAIL unexpected decision-loop markers: ${triggered.join(', ')}\n`);
  process.exit(1);
}
if (!/2\s*(?:\n|$)/.test(out)) {
  process.stdout.write('FAIL expected simple numeric answer 2\n');
  process.exit(1);
}
process.stdout.write('PASS\n');
process.exit(0);
