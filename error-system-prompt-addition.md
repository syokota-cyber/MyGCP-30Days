# PROJECT_PROMPT.mdへの追記内容

## 🚨 エラー自動記録システム（追記部分）

### エラー発生時の対応フロー
1. **AI支援でエラー分析・解決方法提案**
2. **自動記録スクリプト実行**: `./scripts/log-error.sh [type] [title] [description]`
3. **詳細情報をファイルに追記**（AI提案内容）
4. **自動コミット**: `./scripts/commit-errors.sh`

### エラータイプ分類
- `api`: API有効化・設定エラー
- `auth`: 認証・権限・プロジェクト設定エラー
- `scheduler`: Cloud Scheduler関連エラー
- `pubsub`: Pub/Sub関連エラー
- `cloudrun`: Cloud Run関連エラー
- `general`: その他のGCPエラー

### AI支援の指針
- エラー発生時は即座に分類・解決方法を提案
- 記録用のコマンド例を具体的に提示
- 予防策・関連情報も含めて支援

### 自動化可能な項目
- ✅ エラー分析・解決方法提案
- ✅ 記録フォーマット生成
- ✅ ファイル作成・編集（filesystem使用）
- ❌ Git操作（手動実行必要）

### 定期メンテナンス
- 週次: `python3 scripts/generate-error-summary.py`
- 月次: エラーパターンの見直し・改善提案