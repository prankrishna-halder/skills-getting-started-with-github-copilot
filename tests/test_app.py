import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg.status_code == 200
    assert f"Unregistered {email}" in response_unreg.json()["message"]
    # Try unregister again
    response_unreg2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code == 400


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=nouser@mergington.edu")
    assert response.status_code == 404


def test_unreg_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=nouser@mergington.edu")
    assert response.status_code == 404
