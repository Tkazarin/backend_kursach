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
def created_comm_id():
    body = {
        "id_fic": "1",
        "text": "Текст"
    }
    r = requests.post(f"{BASE_URL}/add_comm", json=body, cookies=admin_cookies)
    assert r.status_code == 200, f"Status not 200: {r.status_code} {r.text}"
    comments = requests.get(f"{BASE_URL}/comms", params={"id_fic": "1"}).json()
    if not isinstance(comments, list) or not comments:
        raise Exception(f"Не удалось получить комментарии: {comments}")
    test_id = comments[-1]["id_comment"]
    yield test_id
    requests.delete(f"{BASE_URL}/comm", params={"id_comment": test_id}, cookies=admin_cookies)


# Пример тестов
def test_get_all_comms():
    r = requests.get(f"{BASE_URL}/comms", params={"id_fic": "1"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_add_comm():
    body = {
        "id_fic": "1",
        "text": "Текст"
    }
    r = requests.post(f"{BASE_URL}/add_comm", json=body, cookies=admin_cookies)
    assert r.status_code == 200
    assert "message" in r.json()

def test_get_comm_by_id(created_comm_id):
    r = requests.get(f"{BASE_URL}/comm", params={"id_comment": created_comm_id})
    assert r.status_code == 200

def test_update_comm(created_comm_id):
    body = {
        "id_comment": created_comm_id,
        "text": "Текст 2"
    }
    r = requests.patch(f"{BASE_URL}/comm", params={"id_comment": created_comm_id}, json=body, cookies=admin_cookies)
    assert r.status_code == 200
    fandom = r.json()
    assert fandom["text"] == "Текст 2"

def test_delete_fic(created_comm_id):
    r = requests.delete(f"{BASE_URL}/сomm", params={"id_comment": created_comm_id}, cookies=admin_cookies)
    assert r.status_code in (200, 404)