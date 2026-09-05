#!/usr/bin/env bash
# 推送脚本：默认交互确认；可通过 --yes/--message 或 PUSH_CONFIRM/PUSH_MESSAGE 自动化。
# 用途：把 vault 中新蒸馏的 skill、语料、产物提交并推送到远程仓库。
# 安全：只允许公开目录；禁止把内部开发产物（assignments/、evals/）一并推上去。
# 凭据：不硬编码、不提示粘贴密码；自动模式请使用 git credential helper、CI secret 或已经配置好的认证。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

AUTO=0
COMMIT_MSG=""

usage() {
  cat <<'EOF'
用法: bash scripts/push.sh [选项]

选项:
  -y, --yes              跳过交互确认，直接提交并推送
  -m, --message <msg>    指定 commit message（也可用 PUSH_MESSAGE 环境变量）
  -h, --help             显示帮助

环境变量:
  PUSH_CONFIRM=yes       等价于 --yes
  PUSH_MESSAGE=<msg>     等价于 --message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes)
      AUTO=1
      shift
      ;;
    -m|--message)
      if [[ $# -lt 2 ]]; then
        echo "! --message 需要参数" >&2
        exit 2
      fi
      COMMIT_MSG="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "! 未知参数: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "${PUSH_CONFIRM:-}" == "yes" || "${PUSH_CONFIRM:-}" == "1" ]]; then
  AUTO=1
fi
if [[ -z "$COMMIT_MSG" && -n "${PUSH_MESSAGE:-}" ]]; then
  COMMIT_MSG="$PUSH_MESSAGE"
fi

echo "=== dsh-skill-vault 推送 ==="
echo "仓库路径: $ROOT"
echo "远程: $(git remote get-url origin 2>/dev/null || echo '(未配置 remote)')"
echo
echo "接下来会执行："
echo "  git add -A"
echo "  git commit -m '${COMMIT_MSG:-vault: update distilled skills}'"
echo "  git push origin HEAD"
echo

if [[ "$AUTO" != "1" ]]; then
  if [[ -t 0 ]]; then
    read -r -p "确认继续？(yes/no): " CONFIRM
    if [[ "$CONFIRM" != "yes" && "$CONFIRM" != "y" ]]; then
      echo "已取消。你可以手动执行上面的 git 命令。"
      exit 0
    fi
  else
    echo "! 非交互环境：请使用 --yes / PUSH_CONFIRM=yes 以启用自动推送。" >&2
    exit 2
  fi
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

if [[ -z "$COMMIT_MSG" ]]; then
  if [[ "$AUTO" == "1" ]]; then
    COMMIT_MSG="vault: update distilled skills"
  elif [[ -t 0 ]]; then
    read -r -p "查看暂存后，输入 commit message（直接回车用默认）: " MSG
    COMMIT_MSG="${MSG:-vault: update distilled skills}"
  else
    COMMIT_MSG="vault: update distilled skills"
  fi
fi

git commit -m "$COMMIT_MSG"
echo "=== 推送中（凭据由 credential helper / CI secret 提供）==="
git push origin HEAD
echo "=== 推送完成 ==="
