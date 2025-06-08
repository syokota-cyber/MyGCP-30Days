#!/bin/bash

# 今日の日付取得
TODAY=$(date +%Y-%m-%d)
DAY_NUM=$1

if [ -z "$DAY_NUM" ]; then
  echo "Usage: $0 <day_number>"
  echo "Example: $0 13"
  exit 1
fi

# テンプレートから日次ログを作成
cp templates/daily-template.md "daily-logs/gcp-Day${DAY_NUM}.md"

# 日付とDay番号を置換
sed -i "s/Day XX/Day ${DAY_NUM}/g" "daily-logs/gcp-Day${DAY_NUM}.md"
sed -i "s/2025-06-XX/${TODAY}/g" "daily-logs/gcp-Day${DAY_NUM}.md"

echo "Created: daily-logs/gcp-Day${DAY_NUM}.md"
echo "Please edit the file to add today's learning content!"
