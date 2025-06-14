# Day03 - Cloud Storage バケット & 静的サイト公開

## 🎯 今日の目的
- GCS バケットを作成し、`index.html` を HTTPS 経由で公開する
- 静的コンテンツ（HTML・画像）の公開権限を適切に設定する

---

## ✅ 実施内容ログ

- Cloud Storage バケット `my-first-bucket-syokota` を作成
- `index.html` をアップロードし、HTTPS 経由でのページ表示確認に成功
- 画像（hero.jpg）の公開設定にて以下の問題に直面：

### 🔍 詰まりポイント

- バケットに **Uniform bucket-level access が有効** → ACL 操作が使用不可
- `gsutil acl ch` での公開がブロックされ、403 `AccessDenied` が発生
- 対処法として IAM に `allUsers:objectViewer` 付与を試行

### 🧭 得られた学び

- GCS バケットのアクセス制御方式（Uniform vs Fine-Grained）の実践理解
- 公開可能なオブジェクトの条件と、Cloud Storage 公開設定の流れ
- `gsutil` / `gcloud` による IAM 操作の実務スキル向上

---

## 📌 本日の成果

- `https://storage.googleapis.com/my-first-bucket-syokota/index.html` でページ表示確認 ✅
- 画像公開は時間の都合で中断。Day04 のドメイン設定と合わせて再検討予定

---

## 💬 感想・次回へのメモ

- 表示されるようになったときの達成感はあるが、画像の公開が難航
- Day04 で独自ドメイン対応後、Cloud CDN 経由で画像も含めた運用を再試行予定