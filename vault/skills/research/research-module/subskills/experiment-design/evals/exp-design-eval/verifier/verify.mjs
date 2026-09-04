import fs from 'node:fs';
const raw = fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8'); const out = raw.toLowerCase();
const required = ["假设", "统计检验", "样本量", "可复现", "EXP_OK"];
const missing = required.map(s=>s.toLowerCase()).filter(s => !out.includes(s));
if (missing.length) { process.stdout.write('FAIL missing: ' + missing.join(',') + '\n'); process.exit(1); }
process.stdout.write('PASS\n'); process.exit(0);
