import pytest
from app import app

@pytest.fixture
def app():
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_product(client):
    response = client.post('/api/products', json={'name': 'Test Product', 'price': 10.99})
    assert response.status_code == 201

def test_get_product(client):
    response = client.get('/api/products/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Product'
