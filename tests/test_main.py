import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# テスト環境変数を設定
os.environ["TESTING"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project"

# モックを使用してmainをインポート
with patch('google.cloud.firestore.Client'), \
     patch('google.cloud.secretmanager.SecretManagerServiceClient'):
    from main import app

client = TestClient(app)

def test_read_root():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert json_response["version"] == "1.1.0"

def test_health_endpoint():
    """ヘルスチェックエンドポイントのテスト"""
    with patch('main.get_secret', return_value="test"):
        response = client.get("/health")
        assert response.status_code == 200

@patch('main.collection')
def test_get_notes(mock_collection):
    """ノート一覧取得のテスト"""
    # モックの設定
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {
        "title": "テストノート",
        "content": "テスト内容",
        "uid": "test-user"
    }
    mock_doc.id = "test-id"
    
    mock_collection.order_by.return_value.stream.return_value = [mock_doc]
    
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
