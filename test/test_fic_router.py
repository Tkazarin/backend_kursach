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
def created_fic_id():
    body = {
        "title": f"Test Fic {unique_suffix}",
        "title_fandom": "string",
        "description": "Описание фика",
        "text": "Текст"
    }
    r = requests.post(f"{BASE_URL}/add_fic", json=body, cookies=admin_cookies)
    assert r.status_code == 200, f"Status not 200: {r.status_code} {r.text}"
    fandoms = requests.get(f"{BASE_URL}/fics").json()
    test_id = fandoms[-1]["id_fic"]
    yield test_id
    requests.delete(f"{BASE_URL}/fic", params={"id_fic": test_id}, cookies=admin_cookies)


# Пример тестов
def test_get_all_fics():
    r = requests.get(f"{BASE_URL}/fics")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_add_fic():
    body = {
        "title": f"Test Fandom {uuid.uuid4()}",
        "title_fandom": "string",
        "description": "Описание тестового фандома",
        "text": "Текст"
    }
    r = requests.post(f"{BASE_URL}/add_fic", json=body, cookies=admin_cookies)
    assert r.status_code == 200
    assert "message" in r.json()

def test_get_fic_by_fandom_id(fandom_id="1"):
    r = requests.get(f"{BASE_URL}/fic", params={"id_fandom": fandom_id})
    assert r.status_code == 200

def test_update_fic(created_fic_id):
    body = {
        "id_fic": created_fic_id,
        "title": "Test Fandom Updated",
        "description": "Описание изменено",
        "text": "Текст",
        "title_fandom": "string",
    }
    r = requests.patch(f"{BASE_URL}/fic", params={"id_fic": created_fic_id}, json=body, cookies=admin_cookies)
    assert r.status_code == 200
    fandom = r.json()
    assert fandom["title"] == "Test Fandom Updated"

def test_delete_fic(created_fic_id):
    r = requests.delete(f"{BASE_URL}/fic", params={"id_fic": created_fic_id}, cookies=admin_cookies)
    assert r.status_code in (200, 404)