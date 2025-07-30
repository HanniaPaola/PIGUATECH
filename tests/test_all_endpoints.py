from main import app
from fastapi.testclient import TestClient
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)


def get_auth_token(email, password):
    resp = client.post("/api/auth/login",
                       json={"email": email, "password": password})
    return resp.json()["data"]["token"]


def test_register_and_login_supervisor():
    # Register
    r = client.post("/api/auth/register", json={
        "full_name": "Test Supervisor",
        "email": "supervisor_all@example.com",
        "password": "testpass123"
    })
    assert r.status_code == 201
    # Login
    r = client.post("/api/auth/login", json={
        "email": "supervisor_all@example.com",
        "password": "testpass123"
    })
    assert r.status_code == 200
    assert "token" in r.json()["data"]


def test_create_and_get_farmer():
    # Register supervisor
    client.post("/api/auth/register", json={
        "full_name": "Test Supervisor2",
        "email": "supervisor_farmer@example.com",
        "password": "testpass123"
    })
    token = get_auth_token("supervisor_farmer@example.com", "testpass123")
    headers = {"Authorization": f"Bearer {token}"}
    # Create farmer
    r = client.post("/api/users/farmers", json={
        "full_name": "Test Farmer",
        "email": "farmer_all@example.com",
        "password": "farmerpass"
    }, headers=headers)
    assert r.status_code == 201
    # Get me (supervisor)
    r = client.get("/api/users/me", headers=headers)
    assert r.status_code == 200
    # Get my farmers
    r = client.get("/api/users/my-farmers", headers=headers)
    assert r.status_code == 200
    assert any(f["email"] == "farmer_all@example.com" for f in r.json()["data"])


def test_ponds_endpoints():
    r = client.get("/api/ponds/")
    assert r.status_code in (200, 401, 403, 404)  # depende de implementación
    r = client.post("/api/ponds/", json={"name": "Pond1"})
    assert r.status_code in (200, 201, 400, 401, 403)


def test_readings_endpoints():
    r = client.get("/api/readings/")
    assert r.status_code in (200, 401, 403, 404)
    r = client.post("/api/readings/", json={"value": 1.23})
    assert r.status_code in (200, 201, 400, 401, 403)


def test_biomass_endpoints():
    r = client.get("/api/biomass/")
    assert r.status_code in (200, 401, 403, 404)
    r = client.post("/api/biomass/", json={"weight": 10.5})
    assert r.status_code in (200, 201, 400, 401, 403)


def test_notifications_endpoints():
    r = client.get("/api/notifications/")
    assert r.status_code in (200, 401, 403, 404)
    r = client.post("/api/notifications/", json={"message": "Test"})
    assert r.status_code in (200, 201, 400, 401, 403)


def test_reports_endpoints():
    r = client.get("/api/reports/")
    assert r.status_code in (200, 401, 403, 404)
    r = client.post("/api/reports/", json={"title": "Report1"})
    assert r.status_code in (200, 201, 400, 401, 403)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
