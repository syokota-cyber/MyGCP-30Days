#!/bin/bash
# エラー自動記録スクリプト

# 使用方法: ./scripts/log-error.sh "error-type" "error-title" "error-description"
# 例: ./scripts/log-error.sh "api" "Cloud Functions API未有効化" "gcloud services enable cloudfunctions.googleapis.com"

ERROR_TYPE=$1
ERROR_TITLE=$2
ERROR_DESC=$3
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y-%m-%d')

if [ -z "$ERROR_TYPE" ] || [ -z "$ERROR_TITLE" ]; then
    echo "Usage: $0 <error-type> <error-title> [error-description]"
    echo "Error types: api, auth, scheduler, pubsub, cloudrun, general"
    exit 1
fi

# エラータイプに応じてファイルを決定
case $ERROR_TYPE in
    "api")
        ERROR_FILE="error-solutions/gcp-api-errors.md"
        ;;
    "auth")
        ERROR_FILE="error-solutions/auth-permission-errors.md"
        ;;
    "scheduler")
        ERROR_FILE="error-solutions/cloud-scheduler-errors.md"
        ;;
    "pubsub")
        ERROR_FILE="error-solutions/pub-sub-errors.md"
        ;;
    "cloudrun")
        ERROR_FILE="error-solutions/cloud-run-errors.md"
        ;;
    *)
        ERROR_FILE="error-solutions/general-gcp-errors.md"
        ;;
esac

# ディレクトリが存在しない場合は作成
mkdir -p error-solutions

# エラーファイルが存在しない場合は初期化
if [ ! -f "$ERROR_FILE" ]; then
    echo "# $(basename $ERROR_FILE .md | tr '-' ' ' | tr '[:lower:]' '[:upper:]') エラー解決集" > "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "このファイルには関連エラーと解決方法を記録します。" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
fi

# エラー記録を追加
cat >> "$ERROR_FILE" << EOF

## 🚨 ${ERROR_TITLE}

**発生日時**: ${TIMESTAMP}
**発生日**: Day$(date +%d)

### 症状
${ERROR_DESC}

### エラーメッセージ
\`\`\`
[エラーメッセージをここに貼り付け]
\`\`\`

### 解決方法
\`\`\`bash
[解決コマンドをここに記入]
\`\`\`

### 原因
[エラーの根本原因]

### 予防策
- [今後同じエラーを防ぐ方法]

### 関連リンク
- [参考ドキュメントURL]

---

EOF

echo "✅ エラーログ記録完了: $ERROR_FILE"
echo "📝 詳細情報を追記してください"
echo "🔄 完了後: ./scripts/commit-errors.sh で自動コミット"
