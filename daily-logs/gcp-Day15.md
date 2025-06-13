# Day15: BigQuery → Looker Studio 可視化 完全レポート

## 📘 Day15の目標と成果

### 🎯 当初の目標
**「BigQueryにあるデータを、見やすいグラフにする」**

### ✅ 実際に達成したこと
- BigQuery の sales_data テーブルをLooker Studioに接続
- カテゴリ別・商品別・地域別の多角的分析ダッシュボード作成
- リアルタイム更新対応の可視化環境構築
- ビジネス洞察の抽出

---

## 🚨 発生した技術的課題と解決

### 認証エラーとの格闘

#### 問題1: Cloud Shell認証の不安定性
```bash
ERROR: (bq) You do not currently have an active account selected.
```

**解決方法:**
```bash
# Cloud Shell特有の認証方法
gcloud auth application-default login
gcloud config set account shin1yokota@gmail.com
gcloud config set project gcp-handson-30days-30010
```

#### 問題2: BigQuery API未有効化
```bash
ERROR: API [cloudresourcemanager.googleapis.com] not enabled
```

**解決方法:**
- 段階的なAPI有効化
- Cloud Resource Manager API → BigQuery API の順序

### 学習ポイント
- **Cloud Shellの認証は時々リフレッシュが必要**
- **GUI操作の方がCLIより安定**
- **API有効化には順序と時間が必要**

---

## 📊 作成したダッシュボードの詳細

### データ構造（BigQuery: sales_data）
```sql
-- テーブル構造
CREATE TABLE handson_analytics.sales_data (
  order_id INT64,
  customer_id STRING,
  product_name STRING,
  category STRING,
  quantity INT64,
  unit_price FLOAT64,
  region STRING,
  order_date DATE
);
```

### 可視化結果

#### 1. カテゴリ別売上分析（円グラフ）
- **Electronics（33.3%）** - 最大の売上カテゴリ
- **Food（20%）**, **Sports（20%）** - 同率で第2位
- **Home（13.3%）**, **Books（6.7%）**, **Fashion（6.7%）**

#### 2. 商品別売上分析（円グラフ）
- **コーヒー豆（20.8%）** - 最も売れている商品
- **ビジネス書（12.5%）**
- **プロテイン（8.3%）**, **ワイヤレスイヤホン（8.3%）**

#### 3. 地域別売上分析（積み上げ棒グラフ）
- **東京（Tokyo）** - 圧倒的な売上（約7件）
- **名古屋（Nagoya）** - 第2位（約6件）
- **大阪（Osaka）** - 第3位（約4件）
- **福岡（Fukuoka）** - 第4位（約2件）

---

## 💡 重要な質問と回答

### Q1: BigQueryや Looker Studioはどんな人たちがどんな用途で使うの？

#### 職種別利用例

| **職種** | **BigQuery用途** | **Looker Studio用途** | **年収目安** |
|---------|-----------------|---------------------|-------------|
| **データアナリスト** | 深堀り分析・仮説検証 | ダッシュボード作成・レポーティング | 400-800万円 |
| **マーケティング担当** | 施策効果測定・ROI分析 | キャンペーン監視・A/Bテスト結果 | 450-750万円 |
| **経営陣** | KPI監視・意思決定支援 | 経営ダッシュボード・月次レポート | 1000万円〜 |
| **データエンジニア** | データ基盤構築・パイプライン | 運用監視・データ品質チェック | 600-1200万円 |

#### 業界別活用例

**🎮 ゲーム業界:**
- BigQuery: プレイヤー行動ログ・課金データ分析
- Looker Studio: 運営ダッシュボード・KPI監視

**🛒 EC・小売:**
- BigQuery: 売上・在庫・顧客データ統合
- Looker Studio: 商品ランキング・地域別分析

**🏥 ヘルスケア:**
- BigQuery: 匿名化された医療データ分析
- Looker Studio: 疾患別統計・治療成功率

### Q2: ExcelのピボットテーブルやGoogleスプレッドシートとは何が違うの？

#### 比較表

| **機能** | **Excel ピボット** | **Googleスプレッドシート** | **BigQuery + Looker Studio** |
|---------|-------------------|-------------------------|---------------------------|
| **データ容量** | 100万行程度が限界 | 数万行程度 | **数十億行も処理可能** |
| **処理速度** | 大量データで重い | 中程度のデータで重い | **数秒で巨大データを集計** |
| **リアルタイム更新** | 手動更新が必要 | 手動更新が必要 | **自動リアルタイム更新** |
| **共有・コラボ** | ファイル送信が必要 | リアルタイム共有 | **URL共有で即座にアクセス** |
| **複数データ統合** | 手動でコピペ必要 | 限定的 | **自動でデータ統合** |
| **学習コスト** | 低い | 低い | **中程度（SQL必要）** |

#### 使い分けの判断基準

| **データ規模** | **推奨ツール** | **理由** |
|---------------|---------------|----------|
| **〜1万行** | Googleスプレッドシート | 手軽、学習コスト低 |
| **1万〜10万行** | どちらでも可 | 用途・スキルによる |
| **10万行〜** | **BigQuery + Looker Studio** | 処理速度・安定性が必要 |

### Q3: GCPのWebアプリ開発との連携は？

#### 典型的な連携フロー
```
ユーザーアクション → Cloud Run Webアプリ → Firestore → BigQuery → Looker Studio
```

#### 具体的なコード例
```javascript
// ECサイトでの購入処理
app.post('/api/purchase', async (req, res) => {
  // 1. Firestoreに注文データ保存
  await db.collection('orders').add({
    userId: req.body.userId,
    productId: req.body.productId,
    amount: req.body.amount,
    timestamp: new Date()
  });
  
  // 2. BigQueryにリアルタイム分析データ送信
  await bigquery.dataset('analytics').table('purchases').insert([{
    user_id: req.body.userId,
    product_id: req.body.productId,
    amount: req.body.amount,
    timestamp: new Date().toISOString()
  }]);
  
  // 3. Looker Studioで即座に売上が反映される
});
```

#### 業界別連携例

**🍕 フードデリバリー:**
```
注文アプリ → Cloud Run → Firestore → BigQuery → Looker Studio
                            ↓           ↓
                        注文処理    需要予測・配達最適化
```

**🎮 ゲーム:**
```
ゲームアプリ → Firebase → Cloud Functions → BigQuery → Looker Studio
                              ↓              ↓
                         課金処理      プレイヤー行動分析
```

### Q4: こういうのをやってる人の職業は？

#### 主要職種と年収

| **職種** | **主な業務** | **年収目安** | **必要スキル** |
|---------|-------------|-------------|---------------|
| **データアナリスト** | SQL分析・ダッシュボード作成 | 400-800万円 | SQL, 統計, BI ツール |
| **データエンジニア** | データパイプライン構築 | 600-1200万円 | Python, GCP, SQL最適化 |
| **フルスタックエンジニア** | アプリ開発＋分析連携 | 500-1000万円 | JavaScript, Python, 基本的な分析 |
| **データサイエンティスト** | 機械学習・予測モデル | 700-1500万円 | Python, 統計, ML, ビジネス理解 |

#### 企業規模別の役割分担

**🚀 スタートアップ（〜50名）:**
- 1人で全部: アプリ開発 + データ分析 + ダッシュボード

**🏬 中規模企業（50-500名）:**
- データエンジニア: データ基盤
- データアナリスト: 分析・可視化
- バックエンドエンジニア: アプリ開発

**🏭 大企業（500名〜）:**
- 高度な専門分化
- MLエンジニア、データアーキテクトなど

---

## 🛠 技術的な学び

### Looker Studio操作のコツ

#### グラフ設定変更方法
1. **グラフをクリック** → **右側「設定」タブ**
2. **ディメンション（分類軸）の変更:**
   - customer_id → category（カテゴリ別）
   - customer_id → product_name（商品別）
   - customer_id → region（地域別）
3. **指標（数値軸）の変更:**
   - Record Count（件数）
   - quantity (SUM)（数量合計）
   - unit_price (SUM)（金額合計）

#### よくある問題と対処
- **勝手にグラフが変わる:** Looker Studioの自動フィルタリング機能
- **解決方法:** 空白部分をクリックしてフィルタクリア

### BigQuery接続の流れ
1. **Looker Studio** → **「作成」** → **「レポート」**
2. **「データを追加」** → **「BigQuery」コネクタ選択**
3. **接続設定:**
   - プロジェクト: `gcp-handson-30days-30010`
   - データセット: `handson_analytics`
   - テーブル: `sales_data`

---

## 📈 ビジネス洞察

### 発見した重要な情報

#### 🎯 市場分析
1. **主力カテゴリ:** Electronicsが売上の1/3を占める
2. **成長機会:** Fashion・Booksは市場拡大の余地あり
3. **地域特性:** 首都圏（東京）の売上が圧倒的
4. **人気商品:** Food分野のコーヒー豆が最も売れている

#### 💼 事業戦略への示唆
- **商品戦略:** Electronics分野への更なる投資検討
- **マーケティング:** 地方都市（大阪・福岡）への販促強化
- **在庫管理:** コーヒー豆の安定供給体制確保
- **新規開拓:** Fashion・Books分野の商品ラインナップ拡充

---

## 🚀 今後の発展アイデア

### 短期的改善（1-3ヶ月）
1. **時系列分析:** 日付フィルタで売上推移を追加
2. **顧客分析:** リピート率・購入頻度の可視化
3. **収益分析:** unit_priceを使った金額ベース分析

### 中期的発展（3-6ヶ月）
1. **リアルタイム連携:** WebアプリからBigQueryへの自動送信
2. **予測分析:** BigQuery MLによる需要予測
3. **アラート設定:** 売上目標達成度の自動通知

### 長期的展望（6ヶ月〜）
1. **機械学習:** 顧客離脱予測・推薦システム
2. **高度な分析:** コホート分析・RFM分析
3. **全社展開:** 部門別ダッシュボードの標準化

---

## 📚 学習リソースと次のステップ

### 推奨学習パス

#### データアナリスト志向
1. **SQL深化** - 複雑なJOIN、ウィンドウ関数
2. **統計学基礎** - A/Bテスト、因果推論
3. **ビジネス理解** - KPI設計、仮説構築

#### データエンジニア志向
1. **Python学習** - pandas, numpy, データ処理
2. **GCPサービス深化** - Cloud Functions, Dataflow
3. **パフォーマンス最適化** - BigQueryコスト削減

#### フルスタック志向
1. **フロントエンド** - React/Vue でのダッシュボード組み込み
2. **リアルタイム処理** - Pub/Sub, WebSocket
3. **DevOps** - CI/CD, 監視・アラート

### 参考リンク
- [BigQuery 公式ドキュメント](https://cloud.google.com/bigquery/docs)
- [Looker Studio ヘルプ](https://support.google.com/looker-studio)
- [GCP データ分析チュートリアル](https://cloud.google.com/bigquery/docs/tutorials)

---

## 🎯 Day15 総括

### ✅ 技術的達成
- **BigQuery SQL分析** の基礎習得
- **Looker Studio可視化** の実践経験
- **GCP認証・権限管理** の理解
- **リアルタイムダッシュボード** の構築

### ✅ ビジネス理解
- **データドリブン意思決定** の重要性
- **KPI設計・監視** の実践
- **ステークホルダー向けレポーティング** の経験

### ✅ キャリア視点
- **データ分析職種** の理解
- **市場価値・年収水準** の把握
- **学習ロードマップ** の明確化

**Day15「BigQuery → Looker Studio可視化」完全達成！**

実際のビジネスデータを使った本格的な分析ダッシュボードが完成し、データ分析の全工程を体験することができました。この経験は、データアナリスト・データエンジニアの実務に直結する貴重なスキルとなります。

**次回Day16では「Cloud Logging & Monitoring」で、作成したシステムの監視・アラート設定を学ぶ予定です。**