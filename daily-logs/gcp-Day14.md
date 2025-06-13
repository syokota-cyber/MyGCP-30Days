# Day14: BigQuery基本クエリ & 無料枠活用 - 学習ログ

**日付**: 2025年6月9日  
**学習時間**: 約90分  
**目標**: BigQueryでのデータ分析基礎習得

---

## 📚 BigQueryとは

### 🎯 サービス概要
BigQuery（ビッグクエリ）は、Googleが提供する**サーバーレスデータウェアハウス**です。

### 🔧 主な特徴
- **超高速処理**: ペタバイト級のデータを数秒で分析
- **サーバーレス**: インフラ管理不要、自動スケーリング
- **SQL使用**: 既存のSQL知識で即座に利用可能
- **カラム型ストレージ**: 必要な列のみ処理でコスト効率化
- **無料枠提供**: 月1TBクエリ処理 + 10GBストレージ

### 🆚 AWS対応サービス
| BigQuery | AWS対応 |
|----------|---------|
| BigQuery | Amazon Athena / Redshift Serverless |
| 超高速SQL分析 | 同様の大規模分析機能 |
| カラム型処理 | Parquet形式での最適化 |

---

## 🎯 本日の達成目標

- [x] BigQuery環境構築
- [x] CSVデータの取り込み
- [x] 基本的なSQL分析クエリ実行
- [x] 複数角度からのビジネス分析
- [x] 無料枠内での安全運用

---

## 🛠️ 実施した操作手順

### Phase 1: 環境構築
1. **BigQuery コンソールアクセス**
   - GCPコンソール → BigQuery
   - API自動有効化確認

2. **データセット作成**
   - データセット名: `handson_analytics`
   - リージョン: `asia-northeast1` (東京)
   - ロケーション選択の重要性を学習

### Phase 2: データ準備
1. **サンプルデータ作成**
   - ECサイト売上データ（15件）
   - 8カラム: order_id, customer_id, product_name, category, quantity, unit_price, order_date, region

2. **テーブル作成・データ取り込み**
   - ソース: ローカルCSVファイルアップロード
   - スキーマ: 自動検出使用
   - テーブル名: `sales_data`
   - 取り込み結果: 15行、8カラム正常完了

### Phase 3: データ確認
1. **プレビュー機能**
   - データ正常性確認
   - 日本語商品名の表示確認
   - データ型自動判定結果確認

2. **スキーマ確認**
   ```
   order_id: INTEGER
   customer_id: STRING
   product_name: STRING
   category: STRING
   quantity: INTEGER
   unit_price: INTEGER
   order_date: DATE
   region: STRING
   ```

---

## 📊 実行した分析クエリ

### 1. 基本データ確認
```sql
SELECT * FROM `gcp-handson-30days-30010.handson_analytics.sales_data` LIMIT 1000;
```
**学び**: SELECT文の基本構文、LIMIT句の使用

### 2. カテゴリ別売上分析
```sql
SELECT 
    category,
    COUNT(*) as order_count,
    SUM(quantity * unit_price) as total_revenue,
    AVG(quantity * unit_price) as avg_order_value
FROM `gcp-handson-30days-30010.handson_analytics.sales_data`
GROUP BY category
ORDER BY total_revenue DESC;
```

**結果**:
- Electronics: 5件、￥197,500（最高売上）
- Home: 2件、￥34,000
- Food: 3件、￥27,600

**学び**: GROUP BY、集計関数（COUNT, SUM, AVG）、ORDER BY DESC

### 3. 地域別売上分析
```sql
SELECT 
    region,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(*) as total_orders,
    SUM(quantity * unit_price) as total_revenue,
    ROUND(SUM(quantity * unit_price) / COUNT(DISTINCT customer_id), 0) as revenue_per_customer
FROM `gcp-handson-30days-30010.handson_analytics.sales_data`
GROUP BY region
ORDER BY total_revenue DESC;
```

**結果**:
- Osaka: 3名、￥94,600（総売上1位）
- Fukuoka: 2名、￥91,800（顧客単価￥45,900で最高）
- Tokyo: 3名、￥85,000（注文件数6件で最多）
- Nagoya: 2名、￥26,400

**学び**: COUNT(DISTINCT)、ROUND関数、顧客単価計算

### 4. 顧客別購買パターン分析
```sql
SELECT 
    customer_id,
    COUNT(*) as order_frequency,
    SUM(quantity * unit_price) as total_spent,
    COUNT(DISTINCT category) as category_diversity,
    CASE 
        WHEN SUM(quantity * unit_price) >= 50000 THEN 'VIP'
        WHEN SUM(quantity * unit_price) >= 20000 THEN 'Premium'
        ELSE 'Regular'
    END as customer_tier
FROM `gcp-handson-30days-30010.handson_analytics.sales_data`
GROUP BY customer_id
ORDER BY total_spent DESC;
```

**結果**:
- VIP顧客: C006（￥85,000）、C002（￥70,000）、C001（￥67,500）
- Premium顧客: C004（￥21,000）
- Regular顧客: 6名

**学び**: CASE文、顧客セグメンテーション、条件分岐

---

## 🎯 発見したビジネス洞察

### 📈 商品戦略
1. **Electronics強化**: 全売上の65%を占める主力カテゴリ
2. **Home商品拡充**: 少ない注文で高収益（効率性高）
3. **Food安定供給**: リピート購入見込みカテゴリ

### 🗺️ 地域戦略
1. **Fukuoka重点**: 最高顧客単価（￥45,900）
2. **Osaka維持**: 安定した総売上トップ
3. **Tokyo活性化**: 注文数多いが単価向上余地
4. **Nagoya開拓**: 成長ポテンシャル地域

### 👥 顧客戦略
1. **VIP特別対応**: 3名で￥222,500（全体の76%）
2. **リピート促進**: C001の3回購入パターン活用
3. **高額商品推奨**: C006の一点豪華型購買促進

---

## 🔧 操作で学んだテクニック

### GUI操作
- **データセット作成**: リージョン選択の重要性
- **テーブル作成**: CSVアップロード、スキーマ自動検出
- **クエリエディタ**: 構文ハイライト、実行前データ量表示
- **結果表示**: プレビュー、グラフ化、JSON表示

### SQL構文
- **基本SELECT**: カラム指定、全選択（*）
- **集計関数**: COUNT, SUM, AVG, COUNT(DISTINCT)
- **グループ化**: GROUP BY + 集計
- **並び替え**: ORDER BY ASC/DESC
- **条件分岐**: CASE WHEN THEN ELSE END
- **関数**: ROUND（数値丸め）

### エラー対処
- **構文エラー**: SELECT list must not be empty
- **解決方法**: SELECT * の間にスペース追加
- **デバッグ**: エラーメッセージの読み方

---

## 💰 コスト管理

### 無料枠確認
- **月間クエリ処理**: 1TB（今回使用：約2KB）
- **ストレージ**: 10GB（今回使用：約1MB）
- **処理量表示**: クエリ実行前に処理データ量確認

### コスト最適化技術
- **SELECT * 回避**: 必要カラムのみ指定
- **LIMIT句活用**: 探索的分析時の制限
- **WHERE句**: データ絞り込みで処理量削減

---

## 🔄 複数タブ活用

### タブ管理戦略
1. **基本確認**: データプレビュー用
2. **カテゴリ分析**: 商品戦略立案
3. **地域分析**: マーケティング戦略
4. **顧客分析**: CRM・リテンション戦略

### 横断分析の価値
- **統合洞察**: 複数角度からの検証
- **仮説検証**: 分析結果の相互確認
- **戦略立案**: データドリブンな意思決定

---

## 🌟 重要な学び

### BigQueryの強み
1. **処理速度**: 数秒で15行を瞬時分析
2. **使いやすさ**: SQL知識で即座に利用可能
3. **スケーラビリティ**: 小規模から大規模まで対応
4. **コスト効率**: 無料枠で十分な学習・検証可能

### 実務応用性
- **EC事業**: 商品・顧客・売上分析
- **SaaS**: ユーザー行動・利用パターン分析
- **マーケティング**: キャンペーン効果測定
- **経営**: KPI監視・意思決定支援

### データ分析思考
- **仮説設定**: 何を明らかにしたいか
- **適切な集計**: 目的に応じた指標選択
- **結果解釈**: データから洞察を導出
- **アクション**: 分析結果の実務活用

---

## 🚀 次回への準備

### Day15予定: Looker Studio連携
- BigQueryデータのダッシュボード化
- 視覚的なデータ表現
- インタラクティブな分析環境
- ステークホルダー向けレポート作成

### 継続学習ポイント
- **より複雑なクエリ**: JOIN、サブクエリ、WINDOW関数
- **パフォーマンス最適化**: パーティション、クラスタリング
- **データモデリング**: 正規化、非正規化の使い分け
- **自動化**: スケジュールクエリ、データパイプライン

---

## 📝 感想・反省

### 良かった点
- GUI中心アプローチで直感的に操作習得
- 実際のビジネスデータで実用的な分析体験
- エラー対処を通じてSQLデバッグ能力向上
- 複数タブでの多角的分析手法習得

### 改善点
- クエリ実行前の処理量確認をより意識する
- より複雑な分析パターンへの挑戦
- データビジュアライゼーションとの連携

### 次回目標
- Looker Studioでのダッシュボード作成
- より高度なSQL分析パターンの習得
- 実務レベルでのデータ分析スキル向上

---

**学習完了**: Day14 BigQuery基本クエリ & 無料枠活用 ✅  
**次回**: Day15 BigQuery → Looker Studio で可視化