import pytest
from fastapi.testclient import TestClient
from urls import app


@pytest.fixture
def client():
    return TestClient(app)


def test_forecast_200(client):
    resp = client.get('/forecast/1')
    assert resp.status_code == 200
    assert resp.text == '["Moscow","St. Petersburg"]'


def test_forecast_404(client):
    resp = client.get('/forecast/999999')
    assert resp.status_code == 404
    assert resp.text == '{"detail":"Cities not found."}'
