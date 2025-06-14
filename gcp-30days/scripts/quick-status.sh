#!/bin/bash
echo "🚀 Cloud Shell GCP状況確認"
echo "=========================="
echo "プロジェクト: $(gcloud config get-value project)"
echo "アカウント: $(gcloud config get-value account)"
echo ""

echo "📊 デプロイ済みサービス:"
echo "Cloud Run: $(gcloud run services list --format='value(metadata.name)' | wc -l) services"
echo "Functions: $(gcloud functions list --format='value(name)' | wc -l) functions"
echo "Pub/Sub: $(gcloud pubsub topics list --format='value(name)' | wc -l) topics"
echo "Scheduler: $(gcloud scheduler jobs list --format='value(name)' | wc -l) jobs"
echo "Artifact Registry: $(gcloud artifacts repositories list --format='value(name)' | wc -l) repositories"
