""" Separated tests for Products Groups. """

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_products_group_creation():
    products_group_creation_params = {
        'id': 100,
        'name': 'some group',
        'description': 'hello',
    }

    response = client.post(
        '/products_group/create/',
        json=products_group_creation_params
    )
    assert response.json() == {'status_code': '200'}
