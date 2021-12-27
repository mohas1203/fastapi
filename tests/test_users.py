from fastapi.testclient import TestClient
from jose import jwt
from app import schemas
import pytest
from app.config import settings


# Test post request to create user
def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "test1123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 202
    assert new_user.email == "test1@gmail.com"


# Testing authenticating user
def test_authenticate_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=settings.signing_algorithm)
    user_id = payload.get("user_id")
    assert user_id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


# Testing incorrect auth
@pytest.mark.parametrize("email, password, status_code", [
    ("test@gmail.com", "wrong_password", 403),
    ("wrong_email@gmail.com", "test123", 403),
    (None, "test123", 422),
    ("test@gmail.com", None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == status_code
