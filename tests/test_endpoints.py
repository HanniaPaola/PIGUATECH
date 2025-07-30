
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_supervisor():
    response = client.post("/api/auth/register", json={
        "full_name": "Test Supervisor",
        "email": "supervisor@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "supervisor@example.com"


def test_login_supervisor():
    # Primero registrar
    client.post("/api/auth/register", json={
        "full_name": "Test Supervisor",
        "email": "supervisor2@example.com",
        "password": "testpass123"
    })
    # Luego login
    response = client.post("/api/auth/login", json={
        "email": "supervisor2@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert data["data"]["user"]["email"] == "supervisor2@example.com"


def test_create_farmer():
    # Registrar y loguear supervisor
    client.post("/api/auth/register", json={
        "full_name": "Test Supervisor",
        "email": "supervisor3@example.com",
        "password": "testpass123"
    })
    login = client.post("/api/auth/login", json={
        "email": "supervisor3@example.com",
        "password": "testpass123"
    })
    token = login.json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/users/farmers", json={
        "full_name": "Test Farmer",
        "email": "farmer@example.com",
        "password": "farmerpass"
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "farmer@example.com"
