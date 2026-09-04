#!/usr/bin/env bash
# 手动推送脚本（必须人工执行，因为需要输入 git HTTPS 凭据）。
# 用途：把 vault 中新蒸馏的 skill、语料、产物提交并推送到远程仓库。
# 安全：只允许公开目录；禁止把内部开发产物（assignments/、evals/）一并推上去。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== dsh-skill-vault 手动推送 ==="
echo "仓库路径: $ROOT"
echo "远程: $(git remote get-url origin 2>/dev/null || echo '(未配置 remote)')"
echo
echo "接下来会执行："
echo "  git add -A"
echo "  git commit -m 'vault: update distilled skills'"
echo "  git push origin HEAD"
echo
read -r -p "确认继续？(yes/no): " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
  echo "已取消。你可以手动执行上面的 git 命令。"
  exit 0
fi

git add -A

# 安全护栏：内部开发产物不应进入公开仓库。
STAGED_INTERNAL="$(git diff --cached --name-only | grep -E '^(assignments|evals)/' || true)"
if [ -n "$STAGED_INTERNAL" ]; then
  echo "! 检测到内部开发产物被暂存，已中止。请检查 .gitignore 或手动移除：" >&2
  echo "$STAGED_INTERNAL" >&2
  git reset >/dev/null 2>&1 || true
  exit 1
fi

git diff --cached --stat || true
read -r -p "查看暂存后，输入 commit message（直接回车用默认）: " MSG
COMMIT_MSG="${MSG:-vault: update distilled skills}"

git commit -m "$COMMIT_MSG"
echo "=== 推送中（可能提示输入密码/密钥）==="
git push origin HEAD
echo "=== 推送完成 ==="
