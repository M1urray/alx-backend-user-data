#!/usr/bin/env python3
import requests


def register_user(email: str, password: str) -> None:
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/register", json={"email": email, "password": password})
    assert response.status_code == 200, "Registration failed"


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/login", json={"email": email, "password": password})
    assert response.status_code == 401, "Login with wrong password should return 401 Unauthorized"


def log_in(email: str, password: str) -> str:
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/login", json={"email": email, "password": password})
    assert response.status_code == 200, "Login failed"
    session_id = response.json()["session_id"]
    return session_id


def profile_unlogged() -> None:
    response = requests.get("http://0277166ee741.cc517a00.alx-cod.online:5000/profile")
    assert response.status_code == 401, "Access to profile should be unauthorized"


def profile_logged(session_id: str) -> None:
    headers = {"session-id": session_id}
    response = requests.get("http://0277166ee741.cc517a00.alx-cod.online:5000/profile", headers=headers)
    assert response.status_code == 200, "Access to profile failed"


def log_out(session_id: str) -> None:
    headers = {"session-id": session_id}
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/logout", headers=headers)
    assert response.status_code == 200, "Logout failed"


def reset_password_token(email: str) -> str:
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/reset_password", json={"email": email})
    assert response.status_code == 200, "Reset password token request failed"
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.post("http://0277166ee741.cc517a00.alx-cod.online:5000/update_password", json=payload)
    assert response.status_code == 200, "Password update failed"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
