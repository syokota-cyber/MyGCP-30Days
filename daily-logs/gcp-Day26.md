# Day24: Vertex AI (Generative) 入門 - Gemini でブログ下書き生成 API

## 🎯 本日の目標

**Vertex AI の Gemini を使って、さまざまなブログ記事の下書きを自動生成するAPI を構築し、Cloud Run にデプロイする**

これまでの fastapi-notes プロジェクトの知識を活用して、実用的なコンテンツ生成システムを作成します。

---

## 📋 前提条件

- Day08までの知識（FastAPI、Cloud Run、Firestore）
- GCPプロジェクト: `gcp-handson-30days-30010`
- 基本的なPython知識

---

## 🧠 Vertex AI Generative AI とは？

| **項目** | **内容** | **AWS対応** |
|----------|----------|-------------|
| **Vertex AI** | GCPのML/AI統合プラットフォーム | Amazon SageMaker |
| **Gemini** | Googleの最新LLM（GPT-4相当） | Claude 3 (Bedrock) |
| **Generative AI** | テキスト・画像・コード生成AI | Amazon Bedrock |
| **主な用途** | コンテンツ生成、要約、翻訳、コード生成 | 同様 |

---

## 🚀 Step 1: 環境準備とAPI有効化

### 1.1 必要なAPIを有効化

```bash
# Vertex AI API を有効化
gcloud services enable aiplatform.googleapis.com

# 確認
gcloud services list --enabled | grep aiplatform
```

### 1.2 プロジェクト設定確認

```bash
# 現在のプロジェクト確認
gcloud config get-value project

# 必要に応じて設定
gcloud config set project gcp-handson-30days-30010
```

---

## 💻 Step 2: プロジェクト構成作成

### 2.1 ディレクトリ構造

```
vertex-ai-blog-api/
├── main.py              # FastAPI アプリ
├── requirements.txt     # 依存関係
├── blog_generator.py    # Gemini呼び出しロジック
├── templates.py         # プロンプトテンプレート
└── README.md
```

### 2.2 requirements.txt

```txt
fastapi==0.104.1
uvicorn==0.24.0
google-cloud-aiplatform==1.38.0
pydantic==2.5.0
python-multipart==0.0.6
```

---

## 🎨 Step 3: ブログ生成ロジック実装

### 3.1 blog_generator.py - Gemini API呼び出し

```python
import vertexai
from vertexai.generative_models import GenerativeModel
from typing import Dict, Any
import os

class BlogGenerator:
    def __init__(self, project_id: str, location: str = "us-central1"):
        """Vertex AI Gemini を初期化"""
        self.project_id = project_id
        self.location = location
        
        # Vertex AI初期化
        vertexai.init(project=project_id, location=location)
        
        # Gemini Pro モデル初期化
        self.model = GenerativeModel("gemini-1.5-pro")
    
    def generate_blog_draft(self, 
                           topic: str, 
                           category: str = "tech", 
                           tone: str = "professional",
                           length: str = "medium") -> Dict[str, Any]:
        """
        ブログ下書きを生成
        
        Args:
            topic: ブログのトピック
            category: カテゴリ（tech, travel, lifestyle等）
            tone: トーン（professional, casual, friendly）
            length: 長さ（short, medium, long）
        """
        
        # プロンプト生成
        prompt = self._build_prompt(topic, category, tone, length)
        
        try:
            # Gemini API呼び出し
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            
            # レスポンス解析
            content = response.text
            
            return {
                "success": True,
                "content": content,
                "topic": topic,
                "category": category,
                "tone": tone,
                "length": length,
                "word_count": len(content.split())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "topic": topic
            }
    
    def _build_prompt(self, topic: str, category: str, tone: str, length: str) -> str:
        """プロンプトを構築"""
        
        length_guide = {
            "short": "400-600文字",
            "medium": "800-1200文字", 
            "long": "1500-2000文字"
        }
        
        tone_guide = {
            "professional": "専門的で信頼感のある",
            "casual": "親しみやすくカジュアルな",
            "friendly": "温かみがあり読者に寄り添う"
        }
        
        category_context = {
            "tech": "技術解説やプログラミング関連の",
            "travel": "旅行体験や観光情報の",
            "lifestyle": "日常生活や趣味に関する",
            "business": "ビジネスや起業に関する"
        }
        
        prompt = f"""
あなたは経験豊富なブログライターです。以下の条件に従って、魅力的なブログ記事の下書きを作成してください。

## 記事条件
- **トピック**: {topic}
- **カテゴリ**: {category_context.get(category, "一般的な")}記事
- **トーン**: {tone_guide.get(tone, "バランスの取れた")}文体
- **文字数**: {length_guide.get(length, "800-1200文字")}程度

## 記事構成
1. **魅力的なタイトル** (SEOを意識した)
2. **導入部** (読者の関心を引く)
3. **本文** (具体例や体験談を含む)
4. **まとめ** (行動喚起を含む)

## 重要なポイント
- 読者にとって実用的で価値のある内容にする
- 具体的な例やエピソードを含める
- SEOキーワードを自然に織り込む
- 読みやすい構成と適切な見出しを使用

それでは、ブログ記事の下書きを作成してください：
"""
        
        return prompt
```

### 3.2 templates.py - プロンプトテンプレート管理

```python
from typing import Dict

class PromptTemplates:
    """プロンプトテンプレートの管理クラス"""
    
    @staticmethod
    def get_specialized_template(category: str) -> str:
        """カテゴリ別の特化プロンプト"""
        
        templates = {
            "tech_tutorial": """
あなたは技術ブログの専門ライターです。初心者にも理解しやすい技術チュートリアル記事を作成してください。

## 記事の要件
- コードサンプルを含める
- ステップバイステップの説明
- 想定読者：プログラミング学習者
- 実際に動作する内容
- トラブルシューティングのヒント含む

トピック: {topic}
""",
            
            "product_review": """
あなたは信頼できるプロダクトレビュアーです。公平で詳細なレビュー記事を作成してください。

## レビューの要件
- メリット・デメリット両方を記載
- 実際の使用感を詳しく
- どんな人におすすめかを明記
- 競合製品との比較
- 評価点数（5点満点）

レビュー対象: {topic}
""",
            
            "experience_story": """
あなたは体験談の名手です。読者が共感できるリアルな体験記事を作成してください。

## 体験記の要件
- 時系列での体験の流れ
- 感じた emotions を詳しく
- 学んだことや気づき
- 読者へのアドバイス
- 写真があると想定した記述

体験内容: {topic}
"""
        }
        
        return templates.get(category, "")
```

---

## 🛠 Step 4: FastAPI アプリケーション実装

### 4.1 main.py - メインアプリケーション

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
from blog_generator import BlogGenerator

app = FastAPI(
    title="Vertex AI Blog Generator API",
    description="Gemini を使ったブログ下書き生成API",
    version="1.0.0"
)

# ブログ生成器初期化
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "gcp-handson-30days-30010")
blog_gen = BlogGenerator(PROJECT_ID)

class BlogRequest(BaseModel):
    topic: str
    category: Optional[str] = "tech"
    tone: Optional[str] = "professional"
    length: Optional[str] = "medium"

class BlogResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    topic: str
    category: str
    tone: str
    length: str
    word_count: Optional[int] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """APIの基本情報"""
    return {
        "message": "Vertex AI Blog Generator API",
        "version": "1.0.0",
        "endpoints": [
            "/generate - ブログ下書き生成",
            "/categories - 利用可能カテゴリ一覧",
            "/examples - 生成例"
        ]
    }

@app.post("/generate", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    """ブログ下書きを生成"""
    
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="トピックが指定されていません")
    
    try:
        result = blog_gen.generate_blog_draft(
            topic=request.topic,
            category=request.category,
            tone=request.tone,
            length=request.length
        )
        
        return BlogResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成エラー: {str(e)}")

@app.get("/categories")
async def get_categories():
    """利用可能なカテゴリ一覧"""
    return {
        "categories": [
            {"id": "tech", "name": "技術・プログラミング"},
            {"id": "travel", "name": "旅行・観光"},
            {"id": "lifestyle", "name": "ライフスタイル"},
            {"id": "business", "name": "ビジネス"},
            {"id": "review", "name": "レビュー・評価"}
        ],
        "tones": [
            {"id": "professional", "name": "プロフェッショナル"},
            {"id": "casual", "name": "カジュアル"},
            {"id": "friendly", "name": "フレンドリー"}
        ],
        "lengths": [
            {"id": "short", "name": "短め (400-600文字)"},
            {"id": "medium", "name": "中程度 (800-1200文字)"},
            {"id": "long", "name": "長め (1500-2000文字)"}
        ]
    }

@app.get("/examples")
async def get_examples():
    """生成例の紹介"""
    return {
        "examples": [
            {
                "topic": "FastAPIとFirestoreでメモアプリを作る",
                "category": "tech",
                "description": "技術チュートリアル記事"
            },
            {
                "topic": "初心者がGCPを30日間学んでみた体験記",
                "category": "tech",
                "description": "学習体験記"
            },
            {
                "topic": "東京の隠れた名所巡り",
                "category": "travel",
                "description": "旅行ガイド記事"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## 🚀 Step 5: Cloud Run デプロイ

### 5.1 ローカルテスト

```bash
# 依存関係インストール
pip install -r requirements.txt

# ローカル起動
python main.py

# 別ターミナルでテスト
curl -X POST "http://localhost:8080/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "FastAPIでAPIを作る方法",
    "category": "tech",
    "tone": "friendly",
    "length": "medium"
  }'
```

### 5.2 Cloud Run デプロイ

```bash
# デプロイ
gcloud run deploy vertex-ai-blog-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

---

## 📝 Step 6: 実際の生成例（具体的事例）

### 例1: 技術チュートリアル

**入力:**
```json
{
  "topic": "FirebaseとReactでリアルタイムチャットアプリを作る",
  "category": "tech",
  "tone": "friendly",
  "length": "long"
}
```

**生成結果例:**
```
# 【初心者向け】FirebaseとReactでリアルタイムチャットアプリを30分で作ってみよう！

## はじめに
「リアルタイムでメッセージがやり取りできるチャットアプリを作ってみたい！」
そんな方に向けて、今回はFirebaseとReactを使って実際に動くチャットアプリを
一緒に作っていきましょう。

プログラミング初心者の方でも大丈夫です。
ステップバイステップで進めていけば、きっと素敵なアプリができあがりますよ♪

## 今回作るアプリの機能
- リアルタイムメッセージ送受信
- ユーザー名の設定
- 投稿時間の表示
- シンプルで使いやすいUI

## 必要な事前準備
1. Node.jsのインストール
2. Firebaseアカウントの作成
3. 基本的なHTML/CSSの知識
4. Reactの基礎知識（useState、useEffectが分かればOK）

[... 続きのコンテンツ]
```

### 例2: 体験記・レビュー

**入力:**
```json
{
  "topic": "GCPを30日間独学してみた正直な感想",
  "category": "tech",
  "tone": "casual",
  "length": "medium"
}
```

**生成結果例:**
```
# 【正直レビュー】GCPを30日間独学してみた！挫折ポイントと乗り越え方

## なぜGCPを学び始めたの？
正直に言うと、AWSの学習に少し疲れていたんです（笑）
「何か新しいクラウドサービスを触ってみたい」そんな軽い気持ちで
GCPの学習をスタートしました。

結果から言うと...めちゃくちゃハマりました！
でも、正直しんどい時期もあったので、リアルな体験談をお伝えします。

## 1週目：「なにこれ、AWS と全然違う...」
最初の印象は「UIが違いすぎる！」でした。
AWSのマネジメントコンソールに慣れていたので、
GCPのコンソール画面を見た時は少し戸惑いました。

特に困ったのが：
- サービス名が違う（EC2→Compute Engine、S3→Cloud Storage）
- IAMの設定方法
- 課金設定の場所

[... 続きのコンテンツ]
```

### 例3: 旅行・ライフスタイル

**入力:**
```json
{
  "topic": "テレワークが捗るカフェの選び方",
  "category": "lifestyle",
  "tone": "professional",
  "length": "medium"
}
```

**生成結果例:**
```
# テレワーク効率化の秘訣：生産性が上がるカフェの選び方完全ガイド

## 自宅以外での作業環境の重要性
テレワークが一般化した現在、自宅だけでなく外部の作業スペースを
効果的に活用することが、生産性向上の鍵となっています。

特にカフェでの作業は、適度な雑音と変化に富んだ環境により、
集中力の向上や創造性の刺激といった効果が期待できます。

## 生産性を高めるカフェの5つの条件

### 1. 安定したWi-Fi環境
テレワークにおいて最も重要な要素です。
- 回線速度: 上り下り共に10Mbps以上が理想
- 接続の安定性: 途切れないこと
- 接続台数制限の確認

[... 続きのコンテンツ]
```

---

## 🔧 Step 7: エラー対処とトラブルシューティング

### よくあるエラーと解決方法

```python
# エラーログ記録機能を追加
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlogGeneratorWithErrorHandling(BlogGenerator):
    def generate_blog_draft(self, **kwargs):
        """エラーハンドリング強化版"""
        
        try:
            # 生成前ログ
            logger.info(f"ブログ生成開始: {kwargs.get('topic', 'Unknown')}")
            
            result = super().generate_blog_draft(**kwargs)
            
            # 成功ログ
            if result.get('success'):
                logger.info(f"ブログ生成成功: {result.get('word_count', 0)}文字")
            
            return result
            
        except Exception as e:
            error_msg = f"生成エラー: {str(e)}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat(),
                "topic": kwargs.get('topic', 'Unknown')
            }
```

### 主要エラーパターン

| **エラー** | **原因** | **解決方法** |
|------------|----------|-------------|
| `API not enabled` | Vertex AI APIが未有効化 | `gcloud services enable aiplatform.googleapis.com` |
| `Permission denied` | 認証情報不正 | Service Account設定確認 |
| `Quota exceeded` | API呼び出し制限 | 制限緩和申請またはリトライ実装 |
| `Model not found` | モデル名間違い | gemini-1.5-pro を確認 |

---

## 📊 AWS Bedrock / OpenAI との比較

| **項目** | **Vertex AI (Gemini)** | **AWS Bedrock (Claude)** | **OpenAI GPT-4** |
|----------|------------------------|---------------------------|-------------------|
| **料金** | トークン単価（入力: $0.00025/1K）| トークン単価（入力: $0.003/1K） | トークン単価（入力: $0.01/1K） |
| **日本語対応** | 優秀 | 良好 | 良好 |
| **インフラ統合** | GCP完全統合 | AWS完全統合 | 別途API連携必要 |
| **セキュリティ** | Google Cloud 基盤 | AWS 基盤 | OpenAI基盤 |
| **カスタマイズ** | ファインチューニング可 | Limited | ファインチューニング可 |

---

## 🔄 Step 8: 実用的な改善案

### 8.1 バッチ生成機能

```python
@app.post("/generate-batch")
async def generate_batch_blogs(topics: List[str], category: str = "tech"):
    """複数トピックの一括生成"""
    results = []
    
    for topic in topics:
        result = blog_gen.generate_blog_draft(
            topic=topic,
            category=category
        )
        results.append(result)
    
    return {"results": results, "total": len(results)}
```

### 8.2 生成履歴の保存（Firestore連携）

```python
from google.cloud import firestore

db = firestore.Client()

def save_generation_history(result: dict):
    """生成履歴をFirestoreに保存"""
    doc_ref = db.collection('blog_generations').document()
    doc_ref.set({
        **result,
        'created_at': firestore.SERVER_TIMESTAMP
    })
```

---

## 🎯 Next Steps: Day25への準備

### Day25予告: Vertex AI ゲートウェイ + Cloud Run
明日は今日作ったブログ生成APIをさらに発展させて：
- **APIゲートウェイによる認証・レート制限**
- **キャッシュ機能による高速化**
- **複数モデルの切り替え機能**
- **コスト最適化**

---

## 🧪 実際に試してみよう！具体的な操作手順

### 実践1: 技術ブログ生成テスト

```bash
# 1. API有効化
gcloud services enable aiplatform.googleapis.com

# 2. プロジェクト作成とデプロイ
mkdir vertex-ai-blog-api
cd vertex-ai-blog-api

# 3. コードファイルを作成（上記のコードをコピー）
# main.py, blog_generator.py, requirements.txt

# 4. Cloud Runにデプロイ
gcloud run deploy vertex-ai-blog-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 実践2: 実際のブログ生成テスト

```bash
# デプロイされたAPIのURLを取得
export API_URL=$(gcloud run services describe vertex-ai-blog-api \
  --region=us-central1 --format="value(status.url)")

# テスト1: 技術記事生成
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Cloud RunとFirestoreでサーバーレスAPI開発",
    "category": "tech",
    "tone": "friendly",
    "length": "medium"
  }' | jq .

# テスト2: 体験記生成
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "プログラミング初心者がGCPを1ヶ月学んでみた",
    "category": "tech", 
    "tone": "casual",
    "length": "long"
  }' | jq .

# テスト3: 旅行記事生成
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "一人旅で行きたい日本の温泉地TOP5",
    "category": "travel",
    "tone": "professional",
    "length": "medium"
  }' | jq .
```

---

## 💡 実用的な活用例

### 活用例1: 個人ブログ運営者

```python
# ブログネタ切れ解消ツール
topics = [
    "在宅ワークで集中力を保つ方法",
    "プログラミング学習で挫折しないコツ", 
    "効率的な情報収集の方法",
    "副業でWebサイト制作を始める手順"
]

for topic in topics:
    blog_draft = generate_blog_draft(topic, category="lifestyle")
    print(f"=== {topic} ===")
    print(blog_draft['content'][:200] + "...")
```

### 活用例2: コンテンツマーケティング

```python
# 商品・サービス紹介記事の下書き生成
product_topics = [
    "新機能リリース：リアルタイム通知機能の使い方",
    "お客様事例：中小企業のDX化成功事例",
    "比較記事：当社サービス vs 競合他社",
    "導入ガイド：5分で始められるセットアップ手順"
]
```

### 活用例3: 技術ドキュメント生成

```python
# API仕様書の説明文生成
api_endpoints = [
    "POST /api/users - ユーザー作成エンドポイント",
    "GET /api/posts - 投稿一覧取得エンドポイント",
    "PUT /api/posts/{id} - 投稿更新エンドポイント",
    "DELETE /api/users/{id} - ユーザー削除エンドポイント"
]
```

---

## 🔍 高度なプロンプトエンジニアリング例

### プロンプト改良版: SEO特化

```python
def build_seo_optimized_prompt(topic: str, target_keyword: str, search_intent: str) -> str:
    return f"""
あなたはSEOライティングの専門家です。以下の条件で検索上位を狙える記事を作成してください。

## SEO要件
- **ターゲットキーワード**: {target_keyword}
- **検索意図**: {search_intent}
- **競合分析**: 上位記事より詳しく実用的な内容
- **E-A-T**: 専門性・権威性・信頼性を意識

## 記事構成（SEO最適化）
1. **タイトル**: ターゲットキーワードを含む32文字以内
2. **メタディスクリプション**: 120文字以内の魅力的な要約
3. **見出し構造**: H2, H3を適切に使用
4. **内部リンク提案**: 関連記事への言及
5. **FAQ要素**: よくある質問への回答

## コンテンツ要件
- 検索ユーザーの問題を解決する具体的な内容
- 実体験やデータに基づく信頼性の高い情報
- 読みやすい文章構成（1文は60文字以内）
- ユーザーの行動を促すCTA（Call to Action）

記事テーマ: {topic}
"""
```

### プロンプト改良版: ペルソナ特化

```python
def build_persona_prompt(topic: str, persona: dict) -> str:
    return f"""
以下のペルソナ（想定読者）に向けた記事を作成してください。

## ターゲットペルソナ
- **年齢**: {persona.get('age', '20-30代')}
- **職業**: {persona.get('job', 'IT関連')}
- **スキルレベル**: {persona.get('skill_level', '初級者')}
- **悩み**: {persona.get('pain_points', '時間不足')}
- **目標**: {persona.get('goals', 'スキルアップ')}

## ペルソナに合わせた記事作成ポイント
- 専門用語は{persona.get('skill_level', '初級者')}レベルに合わせて説明
- {persona.get('pain_points', '時間不足')}を解決する実用的な内容
- {persona.get('goals', 'スキルアップ')}につながる具体的なアクション提示
- 忙しい{persona.get('job', 'IT関連')}でも実践できる内容

記事テーマ: {topic}
"""
```

---

## 📈 パフォーマンス最適化

### 非同期処理対応

```python
import asyncio
from typing import List
from concurrent.futures import ThreadPoolExecutor

class AsyncBlogGenerator(BlogGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def generate_multiple_blogs(self, requests: List[dict]) -> List[dict]:
        """複数ブログの非同期生成"""
        loop = asyncio.get_event_loop()
        
        tasks = []
        for req in requests:
            task = loop.run_in_executor(
                self.executor,
                self.generate_blog_draft,
                req['topic'],
                req.get('category', 'tech'),
                req.get('tone', 'professional'),
                req.get('length', 'medium')
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results

# FastAPIでの非同期エンドポイント
@app.post("/generate-async")
async def generate_blogs_async(requests: List[BlogRequest]):
    """非同期でブログ生成"""
    async_generator = AsyncBlogGenerator(PROJECT_ID)
    
    request_dicts = [req.dict() for req in requests]
    results = await async_generator.generate_multiple_blogs(request_dicts)
    
    return {"results": results, "total": len(results)}
```

### キャッシュ機能追加

```python
from functools import lru_cache
import hashlib
import json

class CachedBlogGenerator(BlogGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}
    
    def _get_cache_key(self, **kwargs) -> str:
        """キャッシュキー生成"""
        cache_data = json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def generate_blog_draft(self, **kwargs):
        """キャッシュ機能付きブログ生成"""
        cache_key = self._get_cache_key(**kwargs)
        
        # キャッシュチェック
        if cache_key in self._cache:
            cached_result = self._cache[cache_key].copy()
            cached_result['from_cache'] = True
            return cached_result
        
        # 新規生成
        result = super().generate_blog_draft(**kwargs)
        
        # 成功時のみキャッシュ
        if result.get('success'):
            self._cache[cache_key] = result.copy()
        
        result['from_cache'] = False
        return result
```

---

## 🛡️ セキュリティとコスト管理

### レート制限機能

```python
from collections import defaultdict
from datetime import datetime, timedelta
import time

class RateLimitedBlogGenerator(BlogGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_counts = defaultdict(list)
        self.rate_limit = 10  # 1時間あたり10リクエスト
    
    def check_rate_limit(self, user_id: str) -> bool:
        """レート制限チェック"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        # 1時間以内のリクエストのみ保持
        self.request_counts[user_id] = [
            req_time for req_time in self.request_counts[user_id]
            if req_time > hour_ago
        ]
        
        return len(self.request_counts[user_id]) < self.rate_limit
    
    def generate_blog_draft(self, user_id: str = "anonymous", **kwargs):
        """レート制限付きブログ生成"""
        if not self.check_rate_limit(user_id):
            return {
                "success": False,
                "error": "レート制限に達しました。1時間後に再試行してください。",
                "rate_limit_exceeded": True
            }
        
        # リクエスト記録
        self.request_counts[user_id].append(datetime.now())
        
        return super().generate_blog_draft(**kwargs)

# FastAPIでのレート制限適用
@app.post("/generate-limited")
async def generate_blog_with_rate_limit(
    request: BlogRequest, 
    user_id: str = "anonymous"
):
    """レート制限付きブログ生成"""
    limited_generator = RateLimitedBlogGenerator(PROJECT_ID)
    
    result = limited_generator.generate_blog_draft(
        user_id=user_id,
        **request.dict()
    )
    
    if result.get('rate_limit_exceeded'):
        raise HTTPException(status_code=429, detail=result['error'])
    
    return result
```

### コスト監視機能

```python
class CostAwareBlogGenerator(BlogGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_tokens = 0
        self.estimated_cost = 0.0
        self.cost_per_1k_tokens = 0.00025  # Gemini Pro の料金
    
    def generate_blog_draft(self, **kwargs):
        """コスト計算付きブログ生成"""
        result = super().generate_blog_draft(**kwargs)
        
        if result.get('success'):
            # トークン数推定（文字数 ÷ 3 の概算）
            estimated_tokens = len(result['content']) // 3
            self.total_tokens += estimated_tokens
            
            # コスト計算
            cost = (estimated_tokens / 1000) * self.cost_per_1k_tokens
            self.estimated_cost += cost
            
            result.update({
                'estimated_tokens': estimated_tokens,
                'estimated_cost_usd': round(cost, 6),
                'total_cost_usd': round(self.estimated_cost, 6)
            })
        
        return result
    
    def get_cost_summary(self):
        """コスト概要取得"""
        return {
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.estimated_cost, 6),
            'total_cost_jpy': round(self.estimated_cost * 150, 2)  # 1USD=150円想定
        }
```

---

## 🎯 まとめ：Day24で実現できたこと

### ✅ 今日達成したこと

1. **Vertex AI Gemini の基本理解**
   - GCPのGenerative AI サービスの全体像
   - AWS Bedrock との比較理解

2. **実用的なブログ生成API の構築**
   - FastAPI + Vertex AI の統合
   - 多様なカテゴリ・トーン・長さへの対応
   - エラーハンドリングの実装

3. **Cloud Run でのデプロイ**
   - サーバーレス環境での AI API 運用
   - スケーラブルな構成の実現

4. **実際の生成例とユースケース**
   - 技術記事、体験記、ライフスタイル記事
   - SEO対応、ペルソナ特化の応用

5. **本格運用への拡張機能**
   - 非同期処理、キャッシュ、レート制限
   - コスト監視、セキュリティ対策

### 🚀 実用価値

- **個人ブロガー**: ネタ切れ解消、下書き生成の効率化
- **コンテンツマーケター**: 大量記事の下書き生成
- **技術ライター**: 技術解説記事のたたき台作成
- **学習者**: 文章構成やSEOライティングの学習

### 📊 コスト効率

```
従来の記事外注: 1記事 3,000-10,000円
今回のAPI: 1記事 約0.3-1円（トークン使用料）
効率化: 約99%のコスト削減
```

---

## 🔄 Day25 への橋渡し

明日は今日のブログ生成APIをさらに実用的にする予定です：

### Day25 予定内容
1. **API Gateway 追加**による認証・認可
2. **複数モデル対応**（Gemini Pro/Flash切り替え）
3. **レスポンスキャッシュ**による高速化
4. **使用量ダッシュボード**の構築
5. **Webhook連携**（Slack/Discord通知）

これにより、**企業レベルで運用可能なAI API プラットフォーム**が完成する予定です✨

---

## 📝 本日の学習記録テンプレート

```markdown
# Day24 学習記録

## 完了項目
- [ ] Vertex AI API有効化
- [ ] ブログ生成ロジック実装
- [ ] FastAPI統合
- [ ] Cloud Runデプロイ
- [ ] 生成テスト（3パターン以上）

## 生成したブログサンプル
1. **技術記事**: [トピック名] - [文字数]
2. **体験記**: [トピック名] - [文字数]  
3. **ライフスタイル**: [トピック名] - [文字数]

## 今日の気づき
- Geminiの日本語品質: [評価]
- プロンプトエンジニアリングのコツ: [学び]
- Cloud Runでの運用感: [印象]

## 明日への準備
- [ ] 生成したAPIのURL保存
- [ ] コスト確認
- [ ] 改善したい機能のリストアップ
```

お疲れ様でした！Day24のVertex AI Gemini活用、いかがでしたでしょうか？