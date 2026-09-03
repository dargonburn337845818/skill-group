#!/usr/bin/env bash
# 把 dsh-skill-vault 装入指定 DSH profile（默认 web）。
# 用法：
#   bash scripts/install-web-profile.sh [profile]
#
# 注意：
# - 涉及 ~/.dsh 的修改，先确认没有运行中的 agent 会话。
# - 安装后需要重启 dsh web 才能加载插件。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_NAME="@dsh-external/dsh-skill-vault"
PROFILE="${1:-web}"
DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
PROFILE_DIR="$DSH_HOME/profiles/$PROFILE"
PKG="$PROFILE_DIR/package.json"

if [ ! -f "$PKG" ]; then
  echo "错误：找不到 profile $PROFILE 的 $PKG" >&2
  exit 1
fi

echo "=== dsh-skill-vault 安装到 profile: $PROFILE ==="
echo "插件目录: $ROOT"
echo "Profile : $PROFILE_DIR"
echo

# 备份
BACKUP="$PKG.bak.$(date +%s)"
cp "$PKG" "$BACKUP"
echo "已备份: $BACKUP"

# 写入 dependencies + dsh.profile.bundles
node - "$PKG" "$PLUGIN_NAME" "$ROOT" <<'NODE'
const fs = require('fs')
const [file, name, root] = process.argv.slice(2)
const pkg = JSON.parse(fs.readFileSync(file, 'utf8'))
const link = `link:${root}`
pkg.dependencies = pkg.dependencies || {}
pkg.dependencies[name] = link
const bundles = pkg.dsh?.profile?.bundles || (pkg.dsh = pkg.dsh || {}, pkg.dsh.profile = pkg.dsh.profile || {}, pkg.dsh.profile.bundles = [])
if (!bundles.includes(name)) bundles.push(name)
fs.writeFileSync(file, JSON.stringify(pkg, null, 2) + '\n')
NODE

cd "$PROFILE_DIR"
echo "=== 运行 pnpm install ==="
pnpm install --no-frozen-lockfile

echo
echo "安装完成。请重启 dsh web："
echo "  dsh --profile $PROFILE"
echo "或"
echo "  dsh web"
