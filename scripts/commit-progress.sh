#!/bin/bash

DAY_NUM=$1
MESSAGE="$2"

if [ -z "$DAY_NUM" ] || [ -z "$MESSAGE" ]; then
  echo "Usage: $0 <day_number> <commit_message>"
  echo "Example: $0 13 'Cloud Scheduler implementation completed'"
  exit 1
fi

# 変更をステージング
git add .

# コミットメッセージ形式統一
git commit -m "Day${DAY_NUM}: ${MESSAGE}

- Updated gcp-Day${DAY_NUM}.md
- Added project files
- Updated error solutions if applicable"

echo "Progress committed for Day${DAY_NUM}"
echo "To push: git push origin main"
