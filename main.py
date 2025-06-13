from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from google.cloud import firestore
from google.cloud import secretmanager
import logging
import os
import uvicorn

app = FastAPI(
    title="FastAPI Notes API with Secret Manager",
    description="メモ管理API（Secret Manager統合版）",
    version="1.1.0"
)

# ログ出力の初期化
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Firestore 初期化処理（例外処理付き）
try:
    db = firestore.Client()
    collection = db.collection("notes")
    logger.info("Firestore client initialized successfully")
except Exception as e:
    logger.exception("Firestore initialization failed")
    raise HTTPException(status_code=500, detail="Firestore initialization error")

# Secret Manager クライアント初期化
try:
    secret_client = secretmanager.SecretManagerServiceClient()
    logger.info("Secret Manager client initialized successfully")
except Exception as e:
    logger.exception("Secret Manager initialization failed")
    raise HTTPException(status_code=500, detail="Secret Manager initialization error")

def get_secret(secret_name: str) -> str:
    """Secret Manager から秘密情報を取得"""
    try:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('GCP_PROJECT')
        if not project_id:
            raise HTTPException(status_code=500, detail="プロジェクトIDが設定されていません")
        
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = secret_client.access_secret_version(request={"name": name})
        logger.info(f"Successfully retrieved secret: {secret_name}")
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Secret取得エラー ({secret_name}): {str(e)}")
        raise HTTPException(status_code=500, detail=f"Secret取得エラー: {str(e)}")

# グローバル例外ハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": "An unexpected error occurred."},
    )

@app.get("/")
def root():
    return {
        "message": "FastAPI Notes API with Secret Manager is running",
        "version": "1.1.0",
        "endpoints": {
            "notes": "/notes",
            "admin_config": "/admin/config",
            "health": "/health"
        }
    }

# 🆕 設定情報取得エンドポイント（管理者用）
@app.get("/admin/config")
async def get_config():
    """アプリケーション設定を表示（デバッグ用）"""
    try:
        config = {
            "service": "FastAPI Notes API with Secret Manager",
            "version": "1.1.0",
            "project_id": os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not set'),
            "environment": get_secret("app-environment"),
            "database_configured": bool(get_secret("database-url")),
            "jwt_configured": bool(get_secret("jwt-secret")),
            "firestore_status": "connected",
            "secret_manager_status": "connected"
        }
        return config
    except Exception as e:
        logger.error(f"Config取得エラー: {str(e)}")
        return {
            "error": str(e), 
            "status": "configuration_error",
            "service": "FastAPI Notes API with Secret Manager"
        }

@app.get("/health")
def health():
    """ヘルスチェック（Secret Manager 接続テスト含む）"""
    try:
        # Secret Manager 接続テスト
        test_secret = get_secret("app-environment")
        
        return {
            "status": "healthy",
            "service": "FastAPI Notes API with Secret Manager",
            "firestore": "connected",
            "secret_manager": "connected",
            "environment": test_secret,
            "timestamp": "2024-06-04T12:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "FastAPI Notes API with Secret Manager",
            "firestore": "connected",
            "secret_manager": "disconnected",
            "error": str(e)
        }

@app.post("/notes")
async def add_note(request: Request):
    try:
        data = await request.json()
        user = request.headers.get("X-User-Id")
        if not user:
            raise HTTPException(status_code=400, detail="X-User-Id header is missing")
        
        doc_ref = collection.add({
            "title": data.get("title"),
            "content": data.get("content"),
            "uid": user,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Note added successfully: {doc_ref[1].id}")
        return {"status": "success", "id": doc_ref[1].id}
    except Exception as e:
        logger.exception("Error while adding note")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/notes")
def get_notes():
    try:
        notes = []
        docs = collection.order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            # created_at を文字列に変換
            if "created_at" in data and data["created_at"]:
                data["created_at"] = str(data["created_at"])
            notes.append(data)
        logger.info(f"Retrieved {len(notes)} notes")
        return notes
    except Exception as e:
        logger.exception("Error while retrieving notes")
        raise HTTPException(status_code=500, detail="Failed to retrieve notes")

@app.get("/notes/{note_id}")
def get_note(note_id: str):
    """指定されたIDのメモを取得"""
    try:
        doc = collection.document(note_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="メモが見つかりません")
        
        data = doc.to_dict()
        data["id"] = doc.id
        if "created_at" in data and data["created_at"]:
            data["created_at"] = str(data["created_at"])
        
        logger.info(f"Retrieved note: {note_id}")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error while retrieving note")
        raise HTTPException(status_code=500, detail="Failed to retrieve note")

@app.put("/notes/{note_id}")
async def update_note(note_id: str, request: Request):
    try:
        data = await request.json()
        doc_ref = collection.document(note_id)
        
        # 存在確認
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="メモが見つかりません")
        
        doc_ref.update({
            "title": data.get("title"),
            "content": data.get("content"),
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Note updated successfully: {note_id}")
        return {"status": "updated", "id": note_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error while updating note")
        raise HTTPException(status_code=500, detail="Failed to update note")

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    try:
        doc_ref = collection.document(note_id)
        
        # 存在確認
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="メモが見つかりません")
        
        doc_ref.delete()
        logger.info(f"Note deleted successfully: {note_id}")
        return {"status": "deleted", "id": note_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error while deleting note")
        raise HTTPException(status_code=500, detail="Failed to delete note")

# 👇 ここが Cloud Run に必須！
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)