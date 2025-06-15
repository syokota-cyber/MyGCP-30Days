# Day19 学習ログ - Artifact Registry + Docker

**日付**: 2025年6月15日  
**学習時間**: 約90分  
**技術テーマ**: プライベートDockerレジストリの構築・運用

---

## 🎯 **今日の目標**

**「Artifact Registry + Docker：ビルドしたイメージをプライベート格納」**

| **項目** | **GCP** | **AWS対応** |
|----------|---------|-------------|
| **サービス名** | **Artifact Registry** | **ECR (Elastic Container Registry)** |
| **用途** | Dockerイメージのプライベート格納・管理 | 同様 |
| **特徴** | 複数形式対応（Docker, npm, Maven, Python等） | Docker特化 |

---

## 🔍 **開始時の環境確認**

### **問題発生: プロジェクト設定未完了**

```bash
gcloud config list
# [core]セクションにprojectの設定なし

gcloud services list --enabled
# ERROR: The required property [project] is not currently set.
```

**原因**: Cloud Shellセッション後に設定がリセット

### **解決方法: Configuration管理の導入**

```bash
# 専用configuration作成・有効化
gcloud config configurations create gcp-handson
gcloud config configurations activate gcp-handson
gcloud config set project gcp-handson-30days-30010
```

### **質問: 「毎回こうならないためにはどうしたらいいのか？」**

**提案した予防策**:
1. **Configuration管理**: 複数プロファイル対応
2. **setup.sh**: 一括設定スクリプト
3. **.bashrc自動化**: 起動時自動チェック
4. **エイリアス**: 短縮コマンド

**実装結果**: 全ての予防策を導入、プロンプトにプロジェクト名表示

---

## 🏗️ **Artifact Registry リポジトリ確認・作成**

### **既存状況確認**

**発見したリポジトリ**:
- `cloud-run-source-deploy` (Day17-18のCI/CD作業で自動作成)
- `production-images` (過去の作業)
- `slack-notifier` (Day12のPub/Sub → Slack通知)

### **新規リポジトリ作成（GUI操作）**

**設定内容**:
- **名前**: `day19-docker-repo`
- **形式**: `Docker`
- **ロケーション**: `asia-northeast1`
- **説明**: `Day19 Docker learning repository`

---

## 🔧 **Docker認証設定**

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

**結果**: 全世界のArtifact Registryリージョンに対応する認証ヘルパーが設定

### **質問: 「これは何をやってるの？」**

**説明内容**:
- **認証自動化**: `docker push`時にGCP認証を自動使用
- **全リージョン対応**: 世界中のArtifact Registryで利用可能
- **パスワード不要**: 手動ログインの必要がない

---

## 📝 **サンプルアプリケーション作成**

### **ファイル配置場所の課題**

**質問: 「public傘下だけど問題ない？」**

実際の場所: `/home/shin1yokota/fastapi-notes/my-firebase-auth-app/public/day19-app`

**結論**: 技術的には問題なし、現状のまま進行

### **作成ファイル**

**app.py** (Python Flask):
```python
from flask import Flask
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Day19 Artifact Registry成功！</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; }}
            .container {{ background: rgba(255,255,255,0.1); 
                         padding: 30px; border-radius: 10px; }}
            h1 {{ color: #ffdd59; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Day19 Artifact Registry成功！</h1>
            <p><strong>Container ID:</strong> {os.uname().nodename}</p>
            <p><strong>デプロイ元:</strong> プライベートArtifact Registry</p>
            <p><strong>作成者:</strong> ご主人様</p>
            <p><strong>デプロイ時刻:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>リポジトリ:</strong> day19-docker-repo</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

**requirements.txt**:
```
Flask==2.3.3
```

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
```

---

## 🐳 **Docker Build & Push**

### **ディレクトリ確認の改善**

**質問: 「これって、ツリー上とかもっと見やすくできないのかな？」**

**提案解決策**:
```bash
# treeコマンドインストール
sudo apt install tree -y

# 美しいディレクトリ表示
tree ~/fastapi-notes/my-firebase-auth-app/public/day19-app
```

### **Docker操作**

```bash
# イメージビルド
docker build -t asia-northeast1-docker.pkg.dev/gcp-handson-30days-30010/day19-docker-repo/my-flask-app:v1 .

# ビルド確認
docker images | grep my-flask-app
# 結果: 604cde0928fd   18 seconds ago   146MB

# Artifact Registryにプッシュ
docker push asia-northeast1-docker.pkg.dev/gcp-handson-30days-30010/day19-docker-repo/my-flask-app:v1
```

**成功結果**:
```
v1: digest: sha256:e1497742fca2d6449a3286a2e5b0b808859c9efd66afc173db7b7334def80bcb size: 1990
```

### **質問: 「これは何をやっていたの？Fluxで、フロントエンドのアプリか何かだよね?」**

**回答**:
- **技術**: Python Flask（バックエンド）、React/Vue（フロントエンド）ではない
- **役割**: サーバーサイドでHTMLを生成する「サーバーサイドレンダリング」
- **実現内容**: プライベートDockerレジストリにWebアプリを保管

---

## 🚀 **Cloud Run デプロイ**

### **コンテナ選択時の疑問**

**質問: 「たくさんコンテナがあるんだけれど、これはどういうことなの？」**

**説明内容**:
| **リポジトリ名** | **用途** | **作成経緯** |
|-----------------|----------|-------------|
| `cloud-run-source-deploy` | Cloud Buildの自動ビルド用 | Day17-18のCI/CD作業 |
| `slack-notifier` | Pub/Sub → Slack通知 | Day12の作業 |
| **`day19-docker-repo`** | **今日の学習用** | **今回手動作成** |
| `production-images` | 本番用イメージ | 過去の作業 |

**選択したイメージ**: `day19-docker-repo/my-flask-app:v1` (7分前)

### **デプロイ設定**

| **項目** | **設定値** |
|----------|------------|
| **コンテナURL** | `day19-docker-repo/my-flask-app:v1` |
| **サービス名** | `day19-flask-app` |
| **リージョン** | `asia-northeast1 (東京)` |
| **認証** | `Allow unauthenticated invocations` |
| **課金** | `リクエストベース` |

---

## ✅ **最終成果**

### **公開URL**
```
https://day19-flask-app-231551961281.asia-northeast1.run.app
```

### **表示内容**
- **タイトル**: Day19 Artifact Registry成功！
- **Container ID**: localhost
- **デプロイ元**: プライベートArtifact Registry
- **作成者**: ご主人様
- **デプロイ時刻**: 2025-06-15 02:04:38
- **リポジトリ**: day19-docker-repo

### **質問: 「でもこれって何使うの？」**

**実用例**:

**企業での活用**:
- 社内アプリ開発（機密コード管理）
- マイクロサービス構築
- CI/CDパイプライン
- チーム開発での統一環境

**個人開発での活用**:
- ポートフォリオ作成
- プロトタイプ開発
- 学習・実験環境
- 副業・フリーランス向けアプリ

---

## 📊 **技術スタック全体像**

```
Python Flask App 
    ↓ (Dockerize)
Artifact Registry (プライベート保管)
    ↓ (Deploy)
Cloud Run (サーバーレス実行)
    ↓ (結果)
世界中からアクセス可能なWebアプリ
```

**習得スキル**: **コンテナ化 → レジストリ管理 → クラウドデプロイ**

---

## 🛠️ **導入した運用改善**

### **設定管理の自動化**

1. **gcloud configurations**: 複数プロジェクト対応
2. **setup.sh**: 環境一括設定
3. **.bashrc自動化**: 起動時プロジェクト確認
4. **プロンプト改造**: 常時プロジェクト名表示
5. **便利エイリアス**: `gcp`, `day19`, `gcphelp`

### **ディレクトリ管理の改善**

- **treeコマンド**: 階層構造の可視化
- **findコマンド**: ファイル位置の効率的特定

---

## 🎯 **学習成果まとめ**

### **技術的達成項目**

✅ **Artifact Registry リポジトリ作成・管理**  
✅ **Docker認証設定・自動化**  
✅ **Flask Webアプリのコンテナ化**  
✅ **プライベートレジストリへのpush**  
✅ **Cloud Runでの本格デプロイ**  

### **運用スキル向上**

✅ **gcloud設定の永続化・自動化**  
✅ **GUI + CLI のハイブリッド操作**  
✅ **ディレクトリ構造の効率的管理**  
✅ **エラー予防策の実装**  

### **理解深化項目**

✅ **AWS ECR vs GCP Artifact Registry 比較理解**  
✅ **プライベートレジストリの実用性理解**  
✅ **モダンWebアプリ開発フローの習得**  
✅ **サーバーサイドレンダリング vs フロントエンド技術の区別**  

---

## 📝 **次回への発展可能性**

1. **CI/CDパイプライン**: GitHub連携での自動デプロイ
2. **データベース連携**: Cloud SQLやFirestoreと接続
3. **認証機能**: Firebase Authでログイン機能追加
4. **監視・ログ**: Cloud Monitoringで運用監視

---

## 💡 **今日の重要な気づき**

**「個人でも企業レベルのインフラ構築ができる」**

Day19で習得した**プライベートDockerレジストリシステム**は、現代のWebアプリ開発における核心技術であり、実際のプロダクション環境でも使用される本格的なスキルである。

---

**学習完了時刻**: 2025年6月15日 02:04  
**次回学習予定**: Day20 - Firebase Storage (画像アップロード)

 **Day19 完全成功！おめでとうございます！** ✨

## **🔍 「これって何に使うの？」への回答**

### **📦 今回実現したこと**

**プライベートDockerレジストリシステム**を構築しました！

## **🎯 実際の用途・活用例**

### **🏢 1. 企業での実用例**

| **シチュエーション** | **使い方** |
|---------------------|------------|
| **社内アプリ開発** | 機密コードを含むアプリをプライベートレジストリで管理 |
| **マイクロサービス** | 複数の小さなAPIを個別にコンテナ化・管理 |
| **CI/CD パイプライン** | GitHub → ビルド → プライベートレジストリ → 本番デプロイ |
| **チーム開発** | 開発者全員が同じコンテナイメージを使用 |

### **🚀 2. 個人開発での活用**

| **用途** | **具体例** |
|----------|------------|
| **ポートフォリオ** | 自作Webアプリを安全にデプロイ・公開 |
| **プロトタイプ** | アイデアを素早く形にして検証 |
| **学習・実験** | 新しい技術を試すサンドボックス環境 |
| **副業・フリーランス** | クライアント向けアプリの開発・納品 |

---

## **💡 AWS ECRとの比較で理解**

| **項目** | **今回構築したもの** | **AWS ECR** |
|----------|---------------------|-------------|
| **技術** | GCP Artifact Registry | AWS ECR |
| **用途** | プライベートDockerイメージ管理 | 同様 |
| **メリット** | Google Cloud他サービスとの連携 | AWS他サービスとの連携 |

---

## **🔥 今回の技術スタックの価値**

```
Python Flask App 
    ↓ (Dockerize)
Artifact Registry (プライベート保管)
    ↓ (Deploy)
Cloud Run (サーバーレス実行)
    ↓ (結果)
世界中からアクセス可能なWebアプリ
```

**これは現代の主流な開発手法**：**コンテナ化 → レジストリ管理 → クラウドデプロイ**

---

## **🎯 次に発展させるなら**

1. **CI/CDパイプライン**: GitHub連携で自動デプロイ
2. **データベース連携**: Cloud SQLやFirestoreと接続
3. **認証機能**: Firebase Authでログイン機能追加
4. **監視・ログ**: Cloud Monitoringで運用監視

---

**Day19で習得したスキルは、モダンなWebアプリ開発の核心技術です！** 

これで**「個人でも企業レベルのインフラ構築ができる」**ようになりました 🚀✨

**次はDay20に進みますか？** それとも今日の成果をさらに発展させてみますか？