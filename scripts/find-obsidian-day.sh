#!/bin/bash
# Obsidianボルトから前日情報を取得するスクリプト

DAY_NUM=$1

if [ -z "$DAY_NUM" ]; then
  echo "Usage: $0 <day_number>"
  echo "Example: $0 12"
  exit 1
fi

OBSIDIAN_PATH="/Users/syokota_mac/obsidian-vault/gcp-training"

echo "🔍 Searching for Day${DAY_NUM} in Obsidian vault..."

# Day12関連ファイルを探す
find "$OBSIDIAN_PATH" -name "*Day${DAY_NUM}*" -o -name "*PubSub*" -o -name "*Slack*" 2>/dev/null

echo ""
echo "📝 If files found above, please manually copy relevant content to:"
echo "   daily-logs/gcp-Day${DAY_NUM}.md"
echo ""
echo "🔄 After copying, run: ./scripts/create-daily-log.sh $((DAY_NUM + 1))"
