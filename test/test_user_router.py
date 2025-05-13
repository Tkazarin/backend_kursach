import requests
import uuid

BASE_URL = "http://localhost:8000"
unique_suffix = str(uuid.uuid4())[:8]
userdata = {
    "nickname": f"testuser{unique_suffix}",
    "password": "testpass"
}

def test_register_user():
    response = requests.post(f"{BASE_URL}/register_user/", json=userdata)
    assert response.status_code == 200
    assert "успешно" in response.json()["message"]

def test_register_duplicate_user():
    response = requests.post(f"{BASE_URL}/register_user/", json=userdata)
    assert response.status_code == 409
    assert "Пользователь уже существует" in response.json()["detail"]

def test_login_user():
    response = requests.post(f"{BASE_URL}/login_user/", json=userdata)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "users_access_token" in response.cookies

def test_login_wrong_credentials():
    wrong_user = {
        "nickname": userdata["nickname"],
        "password": "wrongpass"
    }
    response = requests.post(f"{BASE_URL}/login_user/", json=wrong_user)
    assert response.status_code == 401
    assert "Неверная почта или пароль" in response.json()["detail"]

def test_get_me():
    login_resp = requests.post(f"{BASE_URL}/login_user/", json=userdata)
    cookies = login_resp.cookies
    response = requests.get(f"{BASE_URL}/me/", cookies=cookies)
    assert response.status_code == 200
    assert response.json()["nickname"] == userdata["nickname"]

new_data = {
    "nickname": f"testuser{unique_suffix}",
    "password": "newpass"
}

def test_update_user():
    login_resp = requests.post(f"{BASE_URL}/login_user/", json=userdata)
    cookies = login_resp.cookies
    response = requests.patch(
        f"{BASE_URL}/me/",
        json=new_data,
        cookies=cookies
    )
    assert response.status_code == 200
    assert response.json()["nickname"] == new_data["nickname"]

def test_logout_user():
    # Для выхода нужен свежий логин
    login_resp = requests.post(f"{BASE_URL}/login_user/", json={"nickname": "newuser", "password": "newpass"})
    cookies = login_resp.cookies
    response = requests.post(f"{BASE_URL}/logout/", cookies=cookies)
    assert response.status_code == 200
    assert "успешно вышел из системы" in response.json()["message"]

class TestUser:
    user_data = new_data