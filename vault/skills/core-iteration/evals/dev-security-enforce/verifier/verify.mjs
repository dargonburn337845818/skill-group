import fs from 'node:fs';
const outPath = process.env.SKILLJACK_OUTPUT_FILE || 'output.txt';
const out = fs.existsSync(outPath) ? fs.readFileSync(outPath, 'utf8') : '';
const rep = fs.existsSync('report.md') ? fs.readFileSync('report.md', 'utf8') : '';
const combined = out + '\n' + rep;
const required = ['威胁清单','认证绕过','越权','信任边界','威胁建模','输入校验与输出编码','认证 / 授权 / 会话','依赖与供应链','密钥、配置与日志'];
const missing = required.filter((m) => !combined.includes(m));
if (missing.length) { process.stdout.write(`FAIL missing: ${missing.join(', ')}\n`); process.exit(1); }
const riskCount = (combined.match(/RISK:/g) || []).length;
if (riskCount < 5) { process.stdout.write(`FAIL RISK count ${riskCount} < 5\n`); process.exit(1); }
if (!fs.existsSync('report.md')) { process.stdout.write('FAIL missing report.md\n'); process.exit(1); }
process.stdout.write('PASS\n'); process.exit(0);
