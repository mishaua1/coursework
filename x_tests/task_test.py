import requests
from faker import Faker

fake = Faker()
BASE_URL = "https://api.clickup.com/api/v2"
LIST_ID = "901510628795"

my_headers = {
    "Authorization": "pk_188597364_IKLIHFB9CR730I763J5VT6J0MMWZZIMK",
    "Content-Type": "application/json"
}

task_id = None
original_name = fake.file_name()
updated_name = fake.file_name()

def test_create_task():
    global task_id
    body = {
        "name": original_name
    }
    response = requests.post(f"{BASE_URL}/list/{LIST_ID}/task", headers=my_headers, json=body)
    print("Create:", response.status_code, response.text)
    assert response.status_code == 200
    task_id = response.json()["id"]
    assert response.json()["name"] == original_name

def test_get_task_valid():
    response = requests.get(f"{BASE_URL}/task/{task_id}", headers=my_headers)
    print("Get valid:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["name"] == original_name

def test_get_task_invalid():
    response = requests.get(f"{BASE_URL}/task/invalid_task_id", headers=my_headers)
    print("Get invalid:", response.status_code, response.text)
    assert response.status_code in [400, 401, 404]

def test_get_task_no_token():
    response = requests.get(f"{BASE_URL}/task/{task_id}")
    print("No token:", response.status_code, response.text)
    assert response.status_code in [400, 401, 403]

def test_update_task():
    body = {
        "name": updated_name
    }
    response = requests.put(f"{BASE_URL}/task/{task_id}", headers=my_headers, json=body)
    print("Update:", response.status_code, response.text)
    assert response.status_code == 200

def test_get_updated_task():
    response = requests.get(f"{BASE_URL}/task/{task_id}", headers=my_headers)
    print("Get updated:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["name"] == updated_name

def test_delete_task():
    response = requests.delete(f"{BASE_URL}/task/{task_id}", headers=my_headers)
    print("Delete:", response.status_code, response.text)
    assert response.status_code in [200, 204]

def test_get_deleted_task():
    response = requests.get(f"{BASE_URL}/task/{task_id}", headers=my_headers)
    print("Get deleted:", response.status_code, response.text)
    assert response.status_code == 404
