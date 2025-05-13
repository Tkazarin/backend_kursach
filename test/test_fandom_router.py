import requests
import pytest
import uuid

BASE_URL = "http://localhost:8000"
unique_suffix = str(uuid.uuid4())[:8]

def admin_cookies():
    userdata = {
        "nickname": "string_",  # исправлено!
        "password": "string"
    }
    resp = requests.post(f"{BASE_URL}/login_user/", json=userdata)
    resp.raise_for_status()
    return resp.cookies

admin_cookies = admin_cookies()


@pytest.fixture
def created_fandom_id():
    body = {
        "title": f"Test Fandom {unique_suffix}",
        "description": "Описание тестового фандома",
        "type": "movie"
    }
    r = requests.post(f"{BASE_URL}/add_fandom", json=body, cookies=admin_cookies)
    assert r.status_code == 200, f"Status not 200: {r.status_code} {r.text}"
    fandoms = requests.get(f"{BASE_URL}/fandoms").json()
    test_id = fandoms[-1]["id_fandom"]
    yield test_id
    requests.delete(f"{BASE_URL}/fandom", params={"id_fandom": test_id}, cookies=admin_cookies)


# Пример тестов
def test_get_all_fandoms():
    r = requests.get(f"{BASE_URL}/fandoms")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_add_fandom():
    body = {
        "title": f"Test Fandom {uuid.uuid4()}",
        "description": "Описание тестового фандома",
        "type": "movie"
    }
    r = requests.post(f"{BASE_URL}/add_fandom", json=body, cookies=admin_cookies)
    assert r.status_code == 200
    assert "message" in r.json()

def test_get_fandom_by_id(created_fandom_id):
    r = requests.get(f"{BASE_URL}/fandom", params={"id_fandom": created_fandom_id})
    assert r.status_code == 200
    fandom = r.json()
    assert str(fandom.get("id_fandom", created_fandom_id)) == str(created_fandom_id)

def test_update_fandom(created_fandom_id):
    body = {
        "id_fandom": created_fandom_id,
        "title": "Test Fandom Updated",
        "description": "Описание изменено",
        "type": "series"
    }
    r = requests.patch(f"{BASE_URL}/fandom", params={"id_fandom": created_fandom_id}, json=body, cookies=admin_cookies)
    assert r.status_code == 200
    fandom = r.json()
    assert fandom["title"] == "Test Fandom Updated"

def test_delete_fandom(created_fandom_id):
    r = requests.delete(f"{BASE_URL}/fandom", params={"id_fandom": created_fandom_id}, cookies=admin_cookies)
    assert r.status_code in (200, 404)