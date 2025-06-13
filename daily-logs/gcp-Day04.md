

✅ Day06_Firebase_Hosting_Log.md（完全記録版）

# Day06 Firebase Hosting ハンズオンログ（完全記録）

## 🗓 日付
2025-05-26

## 🎯 本日の目標
- Firebase CLI による Hosting 構築とデプロイ
- GCP プロジェクトと Firebase の連携を理解・実践
- 失敗と原因分析から確実なデプロイ技術を習得

---

## ✅ 実施内容の流れ

### 1. Firebase CLI セットアップ & ログイン

```bash
firebase --version  # → 13.28.0
firebase login --no-localhost

	•	Cloud Shell 上でローカルホストが使えないため、--no-localhost で手動認証
	•	ブラウザと CLI の連携をコードで確認・入力
	•	✔ Success! Logged in as shin1yokota@gmail.com 確認

⸻

2. ❌ Firebase に GCP プロジェクトを追加できないトラブル発生

試したプロジェクト：
	•	planar-lacing-460705-m6
	•	gcp-handson-30days-30010

現象：
	•	Firebase Console からプロジェクトを追加しようとすると「不明なエラー」
	•	CLI から firebase init hosting --project プロジェクトID を実行すると：

Error: Failed to get Firebase project xxx

✅ 原因：

カテゴリ	詳細
API未有効	Firebase Hosting API, Firebase Management API が未有効（解決済）
IAM権限	shin1yokota@gmail.com にオーナー権限あり（問題なし）
Firebase連携未完了	GCPプロジェクトはFirebaseに「追加」されていなかった

🎯 本来あるべき理想の流れ：
	1.	GCP Console でプロジェクト作成
	2.	Firebase Console にて「既存の GCP プロジェクトを追加」から明示的に登録
	3.	Firebase CLI が自動認識 → firebase init hosting 成功

⸻

3. ✅ 代替策：Firebase 側から新規プロジェクト作成

実行手順：
	•	Firebase Console で「新しいプロジェクト」を作成
	•	名前：my-firebase-site
	•	プロジェクト ID：my-firebase-site-2a796
	•	Google Analytics は「無効」に設定

✅ 完全に Firebase に連携された状態で作成成功

⸻

4. Firebase Hosting の初期化とデプロイ

firebase init hosting --project my-firebase-site-2a796
firebase deploy

回答例：

質問	回答
public ディレクトリ	public（デフォルト）
SPA（Single Page App）対応	Yes
GitHub 連携	No

✅ firebase.json, .firebaserc, public/index.html 作成
✅ Hosting URL 発行完了 → 公開成功 🎉

⸻

🌐 公開URL

https://my-firebase-site-2a796.web.app

⸻

🔍 詰まりポイントとその対応

トラブル内容	原因	回避・解決策
Firebase コンソールで GCP プロジェクトが表示されない	Firebase にプロジェクトが追加されていない	新しいプロジェクトを Firebase 側で作成し直す
CLI が Firebase プロジェクトを取得できない	--project 指定先が Firebase に存在しない	Firebase Console 側で新規プロジェクト作成し、その ID を指定
ローカルホストでの認証不可	Cloud Shell では localhost 使えない	--no-localhost オプションで手動認証を通す


⸻

📘 学びの要点まとめ
	•	Firebase プロジェクトは「Firebase Console 側から追加」しないと CLI で使えない
	•	Firebase CLI は API が有効化されていれば直にデプロイできる
	•	Firebase Hosting は SPA 含む静的サイトの即時公開に非常に向いている

⸻

📌 次に進むときは
	•	public/index.html をカスタムにして再デプロイ
	•	firebase deploy で変更を即反映可能
	•	firebase init hosting → GitHub Actions 連携を組み込んで自動化へ

---

ご主人様、上記内容にて `.md` ファイル形式で保存・記録も可能でございます。  
Notion に `/log` 登録、GitHub にアップロードしたい場合はお申し付けくださいませ✨