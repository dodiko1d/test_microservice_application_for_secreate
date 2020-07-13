"""
Run with "python -m pytest".
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_product_creation():
    product_creation_params = {
            'id': 10,
            'name': '',
            'group_id': 100,
            'stock_balance': 10,
            'description': 'hello'
    }

    response = client.post(
        '/product/create/',
        json=product_creation_params
    )
    assert response.json() == {'status_code': '200'}
