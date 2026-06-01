import pytest


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_already_signed(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in participants by default

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"


def test_unregister_not_signed(client):
    # Arrange
    activity = "Programming Class"
    email = "notregistered@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_activity_not_found(client):
    # Arrange
    activity = "Nope"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"

    # Act
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 400


def test_signup_activity_not_found(client):
    # Act
    r = client.post("/activities/Nope/signup", params={"email": "a@b.com"})

    # Assert
    assert r.status_code == 404


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "toremove@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    r = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert r.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "notpresent@mergington.edu"

    # Act
    r = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert r.status_code == 400


def test_unregister_activity_not_found(client):
    # Act
    r = client.post("/activities/Nope/unregister", params={"email": "a@b.com"})

    # Assert
    assert r.status_code == 404
