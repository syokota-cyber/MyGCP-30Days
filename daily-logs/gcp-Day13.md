# GCP Day 13 - Cloud Scheduler (cron) → Cloud Run

## 📅 基本情報
- **日付**: 2025-06-08
- **学習時間**: 90分
- **対象サービス**: Cloud Scheduler, Pub/Sub, Cloud Run
- **AWS対応**: EventBridge Scheduler

## 🎯 今日のゴール
- [x] Cloud Schedulerの基本概念理解
- [x] 毎日08:00実行の定期ジョブ作成
- [x] 既存Pub/Sub → Slack通知システムとの連携
- [x] 定期実行動作確認完了
- [x] CRON形式の理解

## 📚 昨日までのおさらい
**前日の成果物**: 
- Day12: Pub/Sub → Cloud Run → Slack通知システム
- トピック: `notification-events`
- Cloud Run: `slack-notifier`
- 手動でのメッセージ送信テスト成功済み

**今日への接続ポイント**:
- 手動実行していたPub/Sub処理を、Cloud Schedulerで自動化

## 🛠 実装内容

### Step 1: プロジェクト運用方針の明確化

**課題**: デスクトップとObsidianボルトの2箇所管理による混乱

**解決**: 運用方針の明確化
- **メイン作業環境**: `/Users/syokota_mac/obsidian-vault/gcp-training/`（編集・コミット）
- **同期先・テスト環境**: `/Users/syokota_mac/Desktop/gcp-30days/`（参照・テスト用）
- **Git管理**: Obsidianボルトから一元管理

**作成したシステム**:
- プロジェクト運用プロンプト（PROJECT_PROMPT.md）
- 学習継続性・自動巡回システム
- エラー管理データベース構成

### Step 2: 環境確認（いつものGCP儀式）

```bash
# プロジェクト確認
gcloud config get-value project
# → gcp-handson-30days-30010

# 既存リソース確認
gcloud pubsub topics list
# → notification-events

gcloud functions list
# → Listed 0 items.

gcloud run services list
# → fastapi-notes, slack-notifier
```

**発見事項**:
- Day12は Pub/Sub → Cloud Run の構成で実装済み
- Cloud Functions ではなく Cloud Run での実装

### Step 3: 既存システムの動作確認

```bash
# テストメッセージ送信
gcloud pubsub topics publish notification-events \
  --message='{"type":"test","message":"Hello from Day13!"}'
```

**結果**: Slackに正常に通知が届く ✅

### Step 4: Cloud Scheduler設定（GUI優先）

**API有効化**:
```bash
gcloud services enable cloudscheduler.googleapis.com
```

**GUI設定手順**:
1. GCPコンソール → Cloud Scheduler
2. 「ジョブを作成」をクリック

**基本設定**:
- 名前: `daily-report-job`
- リージョン: `asia-northeast1（東京）`
- 説明: `Daily morning GCP learning notification`
- 頻度: `0 8 * * *`（毎日8時0分）
- タイムゾーン: `日本標準時（JST）`

**実行内容設定**:
- ターゲットタイプ: `Pub/Sub`
- トピック: `projects/gcp-handson-30days-30010/topics/notification-events`
- メッセージ本文:
```json
{"type":"daily_report","message":"📊 おはようございます！GCP学習Day13 - 毎日8時の自動通知システムが稼働中です！","date":"2025-06-08"}
```

**オプション設定**:
- 最大再試行回数: 0
- 最大試行時間: 0s
- デフォルト設定で作成

### Step 5: 動作確認

**強制実行テスト**:
- Cloud Scheduler一覧画面の「強制実行」ボタンを使用
- Slackに正常に通知が届く ✅

**メッセージ内容変更（CLI版）**:
```bash
# 既存ジョブ削除
gcloud scheduler jobs delete daily-report-job --location=asia-northeast1

# より詳細な内容で再作成
gcloud scheduler jobs create pubsub daily-report-job \
  --schedule="0 8 * * *" \
  --topic="notification-events" \
  --message-body='{"type":"daily_report","message":"🌅 おはようございます！\n📊 GCP学習30日チャレンジ進行中\n✅ Day13: Cloud Scheduler実装完了\n🎯 次回: Day14 BigQuery基本学習\n💪 一緒に頑張りましょう！","date":"2025-06-08","progress":"13/30"}' \
  --time-zone="Asia/Tokyo" \
  --location=asia-northeast1 \
  --description="Daily GCP learning progress notification"
```

## 💬 質問と学習内容

### Q1: プロジェクトのプロンプト作成について
**質問**: 今後の運用に関して、毎回参照できるようにプロジェクトにプロンプトを追加したい

**回答**: 
- GCP学習プロジェクト運用プロンプトを作成
- エラー管理、継続性確保、チャット新規開始時の継ぎ目ない再開機能
- 自動巡回システム、週次サマリー生成機能も提案

### Q2: Git運用とディレクトリ管理について
**質問**: 結局、git(GitHub)へのコミットは、デスクトップからなのObsidianからなの？

**回答**:
- **Obsidianボルトをメイン**とする運用方針に決定
- 12日間のCursor実績を活かし、既存環境を継続
- デスクトップは同期先・テスト環境として活用

### Q3: 開発環境の切り分けについて
**質問**: Cursorはプロジェクトの運用と履歴管理、エラーログの管理用。実際の開発はCloud Shellで実行

**明確化**:
- **実際の開発・実行**: Cloud Shell
- **履歴管理・継続性**: Cursor/Obsidian

### Q4: 自動継続システムについて
**質問**: 自動的に定期巡回したり、トークンが長くなって新しいチャットになった時に継ぎ目なく始められる？

**回答**:
- ファイルベースでの履歴確認は完全実現可能
- 新しいチャットでの状況復元システム構築済み
- 週次サマリー自動生成、エラー分析システムも提案

### Q5: GUIとCLIの使い分けについて
**質問**: 毎回お願いしているが、GUIを優先にして煩雑だったり難しい場合はCLI

**対応**: 
- Cloud SchedulerはGUI優先で進行
- メッセージ編集時は「GUIの入力ボックスが狭い」理由でCLIに変更
- 適切な使い分けを実践

### Q6: CRON形式について
**質問**: cron形式について分かりやすく説明して

**学習内容**:
- **基本構造**: `分 時 日 月 曜日`
- **特殊文字**: `*`（すべて）、`/`（間隔）、`-`（範囲）、`,`（複数指定）
- **実用例**: 朝の通知、業務系、システム保守
- **覚え方**: 「分時日月曜」= 「ぶんじにちげつよう」

### Q7: CRON実用例について
**質問**: どういう場合に使われる？どういう設定をする時？

**学習内容**:
- **レポート・通知系**: 日次売上、週次サマリー、月次レポート
- **システム保守**: DBバックアップ、監視、ログ管理
- **課金・請求系**: 利用料金チェック、請求書発行
- **データ分析**: ETL処理、定期分析
- **業界別例**: ECサイト、医療、アプリサービス

## ❌ 発生したエラー

### エラー1: プロジェクト未設定
**症状**: 
```
ERROR: (gcloud.pubsub.topics.list) The required property [project] is not currently set.
```

**原因**: Cloud Shellの新セッションでプロジェクト設定がリセット

**解決方法**:
```bash
gcloud config set project gcp-handson-30days-30010
```

**学習**: GCP開発の「毎度の儀式」として理解。AWS CLIの`aws configure`と同様の必須手順

### エラー2: CRON形式入力エラー
**症状**: GUI画面で「フィールドがありません。時の指定は0〜23で行います。」

**原因**: 不完全なCRON式入力（`8`のみ）

**解決方法**: 完全なCRON式`0 8 * * *`に修正

### エラー3: Cloud Functions API未有効化
**症状**: 
```
API [cloudfunctions.googleapis.com] not enabled
```

**原因**: Cloud Functions APIが無効状態

**解決方法**: API有効化後、実際にはCloud Functionsは使用していないことが判明

## ✅ 学習成果
- [x] Cloud Schedulerによる定期実行システム構築
- [x] 既存Pub/Sub → Cloud Run システムとの連携
- [x] CRON形式の理解と実用例習得
- [x] GUIとCLIの適切な使い分け
- [x] プロジェクト管理・継続性システムの構築
- [x] エラー対応パターンの蓄積

## 🔗 関連リンク
- [Cloud Scheduler公式ドキュメント](https://cloud.google.com/scheduler/docs)
- [CRON式チェッカー](https://crontab.guru/)
- [Day12実装記録](./gcp-Day12.md)
- [AWS EventBridge Scheduler比較](../docs/aws-gcp-comparison.md)

## 📝 明日への引き継ぎ

**完成した機能**:
- 毎日08:00自動実行のSlack通知システム
- Cloud Scheduler + Pub/Sub + Cloud Run の完全連携
- プロジェクト運用・継続性管理システム

**動作確認済み**:
- 手動強制実行：成功 ✅
- Slack通知受信：成功 ✅
- メッセージ内容変更：成功 ✅

**残タスク**:
- 明日朝8時の自動実行結果確認
- 必要に応じて通知内容の継続改善

**明日の予定**:
- **Day14**: BigQuery基本クエリ & 無料枠活用
- データ分析基盤の構築開始
- Cloud Schedulerで作成した通知システムの実運用開始

## 🎯 今日の重要な学び

1. **プロジェクト運用の重要性**: 技術実装だけでなく、継続的な学習のための仕組み作りが重要
2. **既存システムとの連携**: Day12のPub/Sub → Cloud Run システムを活用して効率的に実装
3. **GUIとCLIの使い分け**: 直感的な設定はGUI、細かい編集・自動化はCLI
4. **CRON実用性**: 単なる技術仕様ではなく、実業務での具体的な活用場面の理解
5. **エラーパターンの蓄積**: GCP特有の「儀式」的エラーの理解と対処法の習得

**総評**: Day13は技術実装と運用体制構築の両面で大きな成果を得た充実した学習日となった。