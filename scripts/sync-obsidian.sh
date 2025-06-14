#!/bin/bash
# Obsidian ⇄ Desktop 同期スクリプト

OBSIDIAN_PATH="/Users/syokota_mac/obsidian-vault/gcp-training"
DESKTOP_PATH="/Users/syokota_mac/Desktop/gcp-30days"

echo "🔄 Obsidian ⇄ Desktop 同期開始..."

if [ ! -d "$OBSIDIAN_PATH" ]; then
  echo "❌ Obsidian vault not found: $OBSIDIAN_PATH"
  exit 1
fi

# Obsidian → Desktop (エラー情報取得)
if [ -d "$OBSIDIAN_PATH/エラー解決集" ]; then
  mkdir -p "$DESKTOP_PATH/error-solutions/from-obsidian"
  rsync -av "$OBSIDIAN_PATH/エラー解決集/" "$DESKTOP_PATH/error-solutions/from-obsidian/"
  echo "✅ Error solutions synced from Obsidian"
fi

# Desktop → Obsidian (新しい学習ログ送信)
if [ -d "$DESKTOP_PATH/daily-logs" ]; then
  mkdir -p "$OBSIDIAN_PATH/作業ログ"
  rsync -av "$DESKTOP_PATH/daily-logs/" "$OBSIDIAN_PATH/作業ログ/"
  echo "✅ Daily logs synced to Obsidian"
fi

echo "🎯 同期完了"
echo "💡 Obsidianで確認: $OBSIDIAN_PATH/作業ログ"
