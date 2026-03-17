from app import app
import pytest

def test_():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200

def test_dynamic_route():
    client = app.test_client()
    response = client.get("/shay")

    assert response.status_code == 200