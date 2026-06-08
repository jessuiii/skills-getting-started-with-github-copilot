import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert all(
        set(activity.keys()) == {"description", "schedule", "max_participants", "participants"}
        for activity in data.values()
    )


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_duplicate_signup_returns_bad_request():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_the_user():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_delete_missing_participant_returns_not_found():
    activity_name = "Chess Club"
    email = "missing@student.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
