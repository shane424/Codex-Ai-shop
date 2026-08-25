import os
os.environ['DATABASE_URL']='sqlite://'
from fastapi.testclient import TestClient
from backend.main import app

def test_health():
    with TestClient(app) as client: assert client.get('/health').json()=={'status':'ok'}
def test_unknown_product_is_safe():
    with TestClient(app) as client:
        response=client.get('/api/products/no-such-product'); assert response.status_code==404; assert response.json()['detail']=='Product not found'
