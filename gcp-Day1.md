

# Day01-02 GCP Hands-On ログ

## ✅ Day01：GCP プロジェクト作成 & 請求アラート

### 🎯 目的
GCP 環境の起動と、費用発生前に通知を受けるための安全対策を整備

### 📋 実施内容

- Cloud Shell 起動 & `gcloud init` 実行
- プロジェクト作成：`gcp-handson-30days-30010`
- 予算アラート作成
  - 名前：`Training Budget`
  - 金額：¥0
  - 通知：Gmail 宛

### 🧠 学び
- GCP はプロジェクト単位で課金・管理される
- GUI 上に新規プロジェクトが即時反映されない場合あり（IAM 等が契機になる）

---

## ✅ Day02：IAM カスタムロール & 割当

### 🎯 目的
最小権限設計による安全なアクセス制御の理解と実装

### 📋 実施内容

1. Cloud Shell でカスタムロール JSON 作成：

```json
{
  "title": "Custom Viewer",
  "description": "Minimum view-only access",
  "stage": "GA",
  "includedPermissions": [
    "compute.instances.list",
    "storage.buckets.list"
  ]
}

	2.	ロール登録（CLI）：

gcloud iam roles create custom_viewer \
  --project=gcp-handson-30days-30010 \
  --file=viewer-role.json

	3.	ユーザー割当：

gcloud projects add-iam-policy-binding gcp-handson-30days-30010 \
  --member="user:jac.syokota@gmail.com" \
  --role="projects/gcp-handson-30days-30010/roles/custom_viewer"

	4.	IAM コンソール上で表示確認

🧠 学び
	•	resourcemanager.projects.list はプロジェクトレベルでは無効 → 組織ロール用
	•	GUI と CLI を併用することで、理解と効率の両立が図れる

⸻

📝 所感
	•	プロジェクト表示に詰まったが、IAM 設定により解消
	•	単なるコマンド実行でなく、「GUI ではどこに相当するか」を意識することで理解が深まる

---
