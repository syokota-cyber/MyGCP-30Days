# Day11: Secret Manager 基本操作 - 学習ログ

## 📋 学習概要
- **日付**: 2025-06-04
- **学習時間**: 約3時間
- **テーマ**: GCP Secret Manager でAPIキーを安全に管理
- **技術スタック**: FastAPI + Secret Manager + Cloud Run + Firestore

## 🎯 学習目標
**Secret Manager の基本操作をマスターし、実用的なAPI統合システムを構築**

## ✅ 達成内容

### 1. Secret Manager 基本設定
- **Secret Manager API 有効化**: `gcloud services enable secretmanager.googleapis.com`
- **GUI操作でSecret作成**: 3つの重要な設定値を安全に保存
  - `database-url`: `postgres://user:password123@localhost:5432/mydb`
  - `jwt-secret`: `my-super-secret-jwt-key-2024`
  - `app-environment`: `production`
- **CLI確認**: `gcloud secrets list` および `gcloud secrets versions access`

### 2. Cloud Run 権限設定
- **Compute Engine API 有効化**: デフォルトサービスアカウント作成
- **IAM権限付与**: Cloud Run サービスアカウントに `roles/secretmanager.secretAccessor` 権限
- **権限確認**: IAMポリシーで権限付与を検証

### 3. FastAPI + Secret Manager 統合
- **dependencies 追加**: `google-cloud-secret-manager==2.18.1`
- **Secret Manager クライアント統合**: SecretManagerServiceClient 初期化
- **get_secret() 関数実装**: 安全なSecret取得機能
- **新エンドポイント追加**:
  - `/admin/config`: Secret Manager統合状況確認
  - `/health`: Secret Manager接続テスト
- **uvicorn設定修正**: gunicorn→uvicorn でASGI対応

### 4. Firestore 統合
- **Firestore API 有効化**: GUIで有効化
- **データベース初期化**: Firestore（ネイティブモード）作成
- **完全統合確認**: Secret Manager + Firestore 連携動作

## 🛠 技術的詳細

### Secret Manager 統合コード例
```python
from google.cloud import secretmanager

# Secret Manager クライアント初期化
secret_client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_name: str) -> str:
    """Secret Manager から安全に秘密情報を取得"""
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# 使用例
environment = get_secret("app-environment")  # → "production"
```

### デプロイ設定
```bash
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
google-cloud-firestore==2.13.1
google-cloud-secret-manager==2.18.1

# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🎉 動作確認結果

### 成功したエンドポイント
1. **ルート**: `GET /`
   ```json
   {
     "message": "FastAPI Notes API with Secret Manager is running",
     "version": "1.1.0",
     "endpoints": {"notes": "/notes", "admin_config": "/admin/config", "health": "/health"}
   }
   ```

2. **管理設定**: `GET /admin/config`
   ```json
   {
     "service": "FastAPI Notes API with Secret Manager",
     "environment": "production",
     "database_configured": true,
     "jwt_configured": true,
     "secret_manager_status": "connected"
   }
   ```

3. **CRUD操作**: `POST /notes`, `GET /notes`
   ```json
   // POST 成功
   {"status": "success", "id": "so0bFuYqe4GORfhDd6yW"}
   
   // GET 結果
   [{
     "id": "so0bFuYqe4GORfhDd6yW",
     "title": "🎉 Day11 完全達成",
     "content": "Secret Manager + Firestore 統合APIが完璧に動作しています！",
     "uid": "testuser",
     "created_at": "2025-06-04 08:17:34.610000+00:00"
   }]
   ```

## 🔍 トラブルシューティング記録

### 問題1: プロジェクト間でのSecret作成ミス
- **症状**: CLI で `Listed 0 items` 
- **原因**: GUI作業時に異なるプロジェクト選択
- **解決**: 正しいプロジェクトで Secret 再作成

### 問題2: Cloud Run デプロイでgunicornエラー
- **症状**: `TypeError: FastAPI.__call__() missing 1 required positional argument: 'send'`
- **原因**: gunicorn の同期ワーカーがASGI未対応
- **解決**: uvicorn 明示 + Procfile 作成

### 問題3: Firestore 404エラー
- **症状**: `The database (default) does not exist`
- **原因**: Firestore API有効化のみでDB未作成
- **解決**: GUIでFirestore データベース初期化

## 🏆 学習成果

### 習得したスキル
- ✅ **Secret Manager の概念**と企業レベルセキュリティの理解
- ✅ **GUI + CLI 操作**での Secret 管理
- ✅ **IAM権限設計**（最小権限の原則）
- ✅ **FastAPI セキュア開発**（機密情報をコードから分離）
- ✅ **Cloud Run 運用**（ASGI + 環境変数設定）
- ✅ **統合システム構築**（Secret Manager + Firestore + Cloud Run）

### 実用的な価値
- **従来**: コードに機密情報を直書き → セキュリティリスク
- **現在**: Secret Manager で暗号化管理 → 企業レベルのセキュリティ
- **利点**: 
  - 環境別設定の自動切り替え
  - リアルタイム設定更新（サーバー再起動不要）
  - 完全な監査ログとアクセス制御

## 🚀 次回学習予定
- **Day12**: 実際の外部サービス連携（SendGrid メール送信）
- **高度なSecret Manager活用**：ローテーション、バージョン管理
- **本格的なAPIキー管理**：複数環境での運用

## 🔗 関連リソース
- **Service URL**: https://fastapi-notes-46f5ifcmda-an.a.run.app
- **プロジェクト**: gcp-handson-30days-30010
- **Secret Manager コンソール**: https://console.cloud.google.com/security/secret-manager
- **Cloud Run コンソール**: https://console.cloud.google.com/run

---
*本ログは GCP 30日学習プログラム Day11 の記録です。*