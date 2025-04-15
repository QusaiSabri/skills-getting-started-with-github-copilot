import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test fetching the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Soccer Team" in activities

def test_signup_for_activity():
    """Test signing up for an activity"""
    email = "teststudent@mergington.edu"
    activity_name = "Soccer Team"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Verify the student is added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    """Test signing up for the same activity twice"""
    email = "teststudent@mergington.edu"
    activity_name = "Soccer Team"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # First signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")  # Duplicate signup
    assert response.status_code == 400
    assert response.json()["detail"] == "Already signed up for this activity"

def test_unregister_from_activity():
    """Test unregistering from an activity"""
    email = "teststudent@mergington.edu"
    activity_name = "Soccer Team"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Ensure student is signed up
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    # Verify the student is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up():
    """Test unregistering a student who is not signed up"""
    email = "notregistered@mergington.edu"
    activity_name = "Soccer Team"
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"

def test_activity_not_found():
    """Test accessing a non-existent activity"""
    email = "teststudent@mergington.edu"
    activity_name = "NonExistentActivity"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
