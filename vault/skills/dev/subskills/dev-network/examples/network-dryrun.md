# dev-network 干跑样例

> 三个真实网络错误样本，按六步流程走一遍。用来证明“症状分类→诊断→根因→可逆修复→验证”闭环，不是完整 A/B。

## 样例 1：npm install 报 `ENOTFOUND`

1. **Collect**：`npm install` 报 `ENOTFOUND registry.npmjs.org`；目标为 npm registry；环境 Ubuntu。
2. **Classify**：DNS 类。
3. **Diagnose**：
   ```bash
   nslookup registry.npmjs.org
   nslookup registry.npmjs.org 8.8.8.8
   cat /etc/resolv.conf
   ```
4. **Analyze**：本机 DNS 解析失败；用 `8.8.8.8` 可解析，说明本机 DNS 服务器/缓存问题。
5. **Resolve**：临时把 DNS 改为 `8.8.8.8`（或 `1.1.1.1`）并 flush；记录原 resolv.conf。
6. **Verify**：`npm ping` 成功；重跑 `npm install` 成功。

## 样例 2：Git push 报 `unable to access`

1. **Collect**：`git push` 报 `fatal: unable to access 'https://github.com/...'`；公司网。
2. **Classify**：代理/Git 配置类。
3. **Diagnose**：
   ```bash
   echo $HTTP_PROXY $HTTPS_PROXY
   git config --global --get http.proxy
   curl -I https://github.com --connect-timeout 5
   ```
4. **Analyze**：直连 GitHub 超时，但 `http_proxy` 指向 `127.0.0.1:7890` 且代理端口未监听 → 代理未运行。
5. **Resolve**：启动代理并确认 `7890` LISTENING；不改 Git 全局配置。
6. **Verify**：`git ls-remote https://github.com/user/repo.git` 成功；`git push` 成功。

## 样例 3：HTTPS 报 `UNABLE_TO_VERIFY_LEAF_SIGNATURE`

1. **Collect**：Node 请求内部 API 报 `UNABLE_TO_VERIFY_LEAF_SIGNATURE`；目标为内部 HTTPS。
2. **Classify**：TLS/证书链类。
3. **Diagnose**：
   ```bash
   echo | openssl s_client -connect <host>:443 -showcerts 2>/dev/null | openssl x509 -noout -subject -issuer -dates
   ```
4. **Analyze**：证书由内部 CA 签发，系统未信任中间 CA；不是服务端证书过期。
5. **Resolve**：把内部 CA（或中间证书）导入系统信任库，或给 Node 指定 `NODE_EXTRA_CA_CERTS`；不永久关闭校验。
6. **Verify**：`curl https://<host>` 通过；Node 请求恢复。

## 反触发说明

- 用户问“帮我写一个 React 组件”时，不进入本技能。
- 用户问“这个算法为什么超时”时，先判断是算法复杂度还是网络；若是纯计算问题，不进入网络排障。
