# Day17: Cloud Build CI/CD実践 - 学習記録ログ

**実施日**: 2025年6月13日  
**所要時間**: 約3時間  
**目標**: GitHub → 自動テスト → Cloud Run デプロイの完全自動化

---

## 🎯 達成目標

- **GitHub連携**: コードpushで自動CI/CD実行
- **自動テスト**: pytest による品質保証
- **自動デプロイ**: Cloud Runへの無停止デプロイ
- **本番環境**: インターネット公開とAPIドキュメント

---

## ✅ 完了した作業

### 1. 環境確認・設定
- プロジェクト設定: `gcp-handson-30days-30010`
- 認証確認: `shin1yokota@gmail.com` (Active)
- 仮想環境: `(venv)` アクティブ状態
- 作業ディレクトリ: `/home/shin1yokota/fastapi-notes`

### 2. 必要ファイル確認
```bash
ls -la main.py requirements.txt cloudbuild.yaml tests/test_main.py
```
- `main.py` (8,203 bytes) - FastAPI + Firestore + Secret Manager
- `requirements.txt` (161 bytes) - Python依存関係
- `cloudbuild.yaml` (754 bytes) - CI/CDパイプライン設定
- `tests/test_main.py` (1,485 bytes) - 3つのテストケース

### 3. API有効化確認
既に有効化済みを確認：
- ✅ Cloud Build API
- ✅ Cloud Run Admin API  
- ✅ Artifact Registry API

### 4. GitHub連携トリガー作成
- トリガー名: `fastapi-notes-ci-cd`
- イベント: ブランチへのpush (^main$)
- GitHub App インストール完了
- サービスアカウント: Compute Engine default

### 5. Git初期化とGitHub連携
```bash
git init
git config --global user.name "syokota-cyber"
git config --global user.email "shin1yokota@gmail.com"
git remote add origin https://github.com/syokota-cyber/MyGCP-30Days.git
git add main.py requirements.txt cloudbuild.yaml tests/ .gitignore
git commit -m "Day17: FastAPI CI/CD setup with Cloud Build"
```

### 6. マージ競合解決
- `.gitignore`ファイルでマージ競合発生
- 手動編集でPython関連の除外ルールを統合
- マージコミット完了

### 7. CI/CDパイプライン実行・問題解決

---

## ⚠️ 発生したエラーと解決方法

### エラー1: Cloud Build クォータ制限
**症状**: 
```
failed precondition: due to quota restrictions, Cloud Build cannot run builds in this region
```

**原因**: `asia-northeast1`リージョンでのCloud Buildクォータ不足

**解決方法**:
```yaml
# cloudbuild.yamlのリージョン変更
--region=asia-northeast1 → --region=us-central1
```

### エラー2: GitHub連携エラー
**症状**:
```
ERROR: (gcloud.builds.triggers.create.github) INVALID_ARGUMENT: Request contains an invalid argument.
```

**原因**: リージョン変更後のGitHub App接続問題

**解決方法**: CLI経由でのトリガー削除・再作成ではなく、直接ビルド実行に変更

### エラー3: pytest モジュール不存在エラー
**症状**:
```
Step #1: /usr/local/bin/python: No module named pytest
```

**原因**: 異なるコンテナ間での依存関係共有不可

**問題の詳細**:
- Step 0: `pip install` でpytestインストール
- Step 1: 新しいコンテナでpytest実行 → モジュールなし

**解決方法**: cloudbuild.yamlの根本的修正
```yaml
# 修正前（失敗版）
steps:
  - name: 'python:3.11'
    entrypoint: pip
    args: ['install', '-r', 'requirements.txt']
  - name: 'python:3.11'
    entrypoint: python
    args: ['-m', 'pytest', 'tests/', '-v']

# 修正後（成功版）  
steps:
  - name: 'python:3.11'
    entrypoint: bash
    args:
      - -c
      - |
        pip install -r requirements.txt
        python -m pytest tests/ -v
```

**修正のポイント**:
- 同一コンテナ内でインストール→テスト実行
- bashによる複数コマンド連続実行

### エラー4: Cloud Run認証エラー
**症状**:
```
Error: Forbidden
Your client does not have permission to get URL / from this server.
```

**原因**: Cloud Runサービスの認証設定問題

**解決方法**:
```bash
gcloud run services add-iam-policy-binding fastapi-notes \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

---

## 🎉 最終成果

### デプロイ成功
- **サービス名**: fastapi-notes
- **リージョン**: us-central1  
- **URL**: https://fastapi-notes-46f5ifcmda-uc.a.run.app
- **デプロイ時刻**: 2025-06-13T07:11:17
- **実行時間**: 5分33秒

### API動作確認
```bash
curl https://fastapi-notes-46f5ifcmda-uc.a.run.app
```

**レスポンス**:
```json
{
  "message": "FastAPI Notes API with Secret Manager is running",
  "version": "1.1.0", 
  "endpoints": {
    "notes": "/notes",
    "admin_config": "/admin/config",
    "health": "/health"
  }
}
```

### 利用可能エンドポイント
- **API ルート**: `/`
- **ヘルスチェック**: `/health`
- **ノートCRUD**: `/notes`
- **管理設定**: `/admin/config`
- **APIドキュメント**: `/docs` (Swagger UI)

---

## 📚 学んだ技術・概念

### CI/CDパイプライン設計
- **継続的インテグレーション**: 自動テスト実行
- **継続的デプロイメント**: 自動本番環境反映
- **品質ゲート**: テスト失敗時の自動停止

### Cloud Build理解
- **ステップベース実行**: YAML定義による工程管理
- **コンテナ分離**: ステップ間でのデータ共有制限
- **リージョン依存**: クォータ・パフォーマンス考慮

### Google Cloud サービス連携
- **Cloud Build**: CI/CDエンジン
- **Cloud Run**: サーバーレスコンテナ実行
- **Artifact Registry**: コンテナイメージ管理
- **IAM**: アクセス制御管理

### 開発ワークフロー最適化
- **GitHub連携**: Push to Production実現
- **自動化価値**: 手動作業排除・人的ミス防止
- **品質保証**: テスト駆動の安全なデプロイメント

---

## 🔄 CI/CDフロー完成形

```
1. 開発者がコード変更
2. GitHubにpush  
3. Cloud Buildトリガー自動実行
4. 依存関係インストール
5. pytest自動実行 (3テスト)
6. テスト成功 → Cloud Runデプロイ
7. 本番環境自動反映
8. アプリケーションURL生成
```

---

## 💡 今後の発展可能性

### セキュリティ強化
- カスタムサービスアカウント作成
- 最小権限原則の適用
- Secret Manager活用拡張

### 監視・運用改善  
- Cloud Monitoring統合
- ログ分析ダッシュボード
- アラート設定

### 開発効率向上
- ブランチ別環境自動作成
- レビューアプリ機能
- A/Bテスト基盤

---

## 📖 参考資料

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions vs Cloud Build比較](https://cloud.google.com/build/docs/automate-builds)

---

## ✨ 感想・反省

### 良かった点
- **段階的問題解決**: エラーを一つずつ確実に解決
- **根本原因追求**: 表面的修正ではなく構造的理解
- **実務応用性**: 現代的なCI/CDワークフロー習得

### 改善点
- **事前準備**: クォータ制限事前確認の重要性
- **設定理解**: cloudbuild.yamlの仕様理解深化
- **運用考慮**: セキュリティ・モニタリング早期検討

### 次回への活かし方
- エラーログ即座確認習慣
- 公式ドキュメント参照重視
- 段階的検証アプローチ継続

---

**Day17完了**: GitHub連携CI/CDによる完全自動化パイプライン構築成功 🎊