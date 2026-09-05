// Reference solution used by oracle gate.
import fs from 'node:fs';
const render = `# Network troubleshoot report

## DIAGNOSIS
- nslookup registry.npmjs.org
- dig @8.8.8.8 registry.npmjs.org
- cat /etc/resolv.conf

## RESOLUTION
- 临时切换 DNS 到 8.8.8.8，记录原配置
- 刷新 DNS 缓存

## VERIFY
- npm ping
- npm install
`;
fs.writeFileSync('report.md', render);
fs.writeFileSync('output.txt', 'done');
