from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(
    title="FastAPI Notes - Security Enhanced",
    description="Day18: セキュリティ強化 + SBOM対応版",
    version="2.1.0"
)

@app.get("/")
async def root():
    return {
        "message": "FastAPI Notes Security Enhanced v2.1.0",
        "features": ["SBOM対応", "脆弱性スキャン済み", "非rootユーザー"],
        "size": "最適化済み"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.1.0"}

@app.get("/security")
async def security_info():
    return {
        "user": "appuser (非root)",
        "scanned": True,
        "sbom": "生成済み",
        "base_image": "python:3.11-slim"
    }
