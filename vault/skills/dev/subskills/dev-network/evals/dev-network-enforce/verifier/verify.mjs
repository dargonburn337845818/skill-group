// Deterministic verifier for dev-network-enforce.
import fs from 'node:fs';

const outPath = process.env.SKILLJACK_OUTPUT_FILE || 'output.txt';
const out = fs.existsSync(outPath) ? fs.readFileSync(outPath, 'utf8') : '';
const rep = fs.existsSync('report.md') ? fs.readFileSync('report.md', 'utf8') : '';
const combined = out + '\n' + rep;

const required = ['DIAGNOSIS', 'RESOLUTION', 'VERIFY'];
const missing = required.filter((m) => !combined.includes(m));
if (missing.length) {
  process.stdout.write(`FAIL missing: ${missing.join(', ')}\n`);
  process.exit(1);
}
const diagCount = (combined.match(/dig|nslookup|curl|resolv\.conf|hosts/g) || []).length;
if (diagCount < 3) {
  process.stdout.write(`FAIL diagnostic command count ${diagCount} < 3\n`);
  process.exit(1);
}
if (!fs.existsSync('report.md')) {
  process.stdout.write('FAIL missing report.md\n');
  process.exit(1);
}
process.stdout.write('PASS\n');
process.exit(0);
