import fs from 'node:fs';
const out = fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8');
if (!out.includes('NO_LLM_NEEDED')) { process.stdout.write('FAIL missing NO_LLM_NEEDED\n'); process.exit(1); }
process.stdout.write('PASS\n');
process.exit(0);
