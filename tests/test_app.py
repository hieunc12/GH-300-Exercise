from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    # No special setup needed for this endpoint.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@example.edu"

    # Make sure the email is not already present before the test.
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    participants = initial_data[activity_name]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated_response = client.get("/activities")
    updated_data = updated_response.json()
    assert email in updated_data[activity_name]["participants"]

    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_signup_rejects_duplicate_email():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@example.edu"

    # Ensure the email is not already registered.
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    if email in initial_data[activity_name]["participants"]:
        client.delete(f"/activities/{activity_name}/unregister?email={email}")

    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={email}")
