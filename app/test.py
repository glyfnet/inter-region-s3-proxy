from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/", params={'Prefix':'collection02'})
    print(response)
    assert response.status_code == 200