#!/usr/bin/env bash
# cron-setup.sh — 安装定时任务
#
# 用法: ./scripts/cron-setup.sh
# 查看: crontab -l
# 卸载: crontab -r (删除所有 cron 任务)

set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Setting up cron jobs for Obsidian Brain..."
echo "Vault directory: $VAULT_DIR"

CRON_ENTRIES="
# Obsidian Brain — 每日凌晨 2:07 consolidate
7 2 * * * cd $VAULT_DIR && claude -p '/project:wiki/consolidate' >> $VAULT_DIR/data/cron.log 2>&1

# Obsidian Brain — 每周日晚 20:13 lint + review
13 20 * * 0 cd $VAULT_DIR && claude -p '/project:wiki/lint' >> $VAULT_DIR/data/cron.log 2>&1 && claude -p '/project:wiki/review weekly' >> $VAULT_DIR/data/cron.log 2>&1

# Obsidian Brain — 每月 1 号凌晨 3:17 深度 consolidate
17 3 1 * * cd $VAULT_DIR && claude -p '/project:wiki/consolidate --deep' >> $VAULT_DIR/data/cron.log 2>&1
"

if crontab -l 2>/dev/null | grep -q "Obsidian Brain"; then
  echo "Cron jobs already installed. Replacing..."
  crontab -l 2>/dev/null | grep -v "Obsidian Brain" | grep -v "wiki/consolidate" | grep -v "wiki/lint" | grep -v "wiki/review" > /tmp/crontab_clean
  echo "$CRON_ENTRIES" >> /tmp/crontab_clean
  crontab /tmp/crontab_clean
  rm /tmp/crontab_clean
else
  echo "Installing new cron jobs..."
  (crontab -l 2>/dev/null; echo "$CRON_ENTRIES") | crontab -
fi

echo ""
echo "Installed cron jobs:"
crontab -l | grep "Obsidian Brain" -A1
echo ""
echo "Done. Logs will be written to $VAULT_DIR/data/cron.log"

mkdir -p "$VAULT_DIR/data"
