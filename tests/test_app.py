import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data, "No activities returned"

def test_signup_and_unregister():
    # Use a test email and a known activity
    test_email = "pytestuser@mergington.edu"
    activity_name = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # Try duplicate signup
    dup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert dup_resp.status_code == 400
    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 400
    # Unregister again (should fail)
    unregister_again = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister_again.status_code == 400
