# Day18: セキュリティ強化 + 最適化版
FROM python:3.11-slim as builder

# パッケージリスト更新 + 必要最小限
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 実行ステージ
FROM python:3.11-slim

# セキュリティ: 非rootユーザー
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 最小限のランタイム依存関係
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# ビルド済み依存関係コピー
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=appuser:appuser . .

# 環境変数
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

USER appuser
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
