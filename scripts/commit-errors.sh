#!/bin/bash
# エラーログ自動コミットスクリプト

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DAY_NUM=$(date +%d)

# error-solutionsディレクトリの変更確認
if [ -n "$(git status --porcelain error-solutions/)" ]; then
    echo "🔄 エラーログの変更を検出しました"
    
    # エラーファイルのみコミット
    git add error-solutions/
    
    # コミットメッセージ生成
    COMMIT_MSG="Day${DAY_NUM}: Error logs updated

- Updated error solutions database
- New error patterns and solutions added
- Timestamp: ${TIMESTAMP}"

    git commit -m "$COMMIT_MSG"
    
    echo "✅ エラーログをコミットしました"
    echo "🚀 プッシュ: git push origin main"
    
    # 自動プッシュ（オプション - 有効にする場合はコメント解除）
    # git push origin main
    # echo "🎯 GitHubにプッシュ完了"
else
    echo "📝 エラーログに変更はありません"
fi
