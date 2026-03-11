import pytest


EMPLOYEE_PAYLOAD = {
    "full_name": "Alice Johnson",
    "job_title": "Software Engineer",
    "country": "India",
    "salary": 80000.0,
}


def test_create_employee(client):
    response = client.post("/employees/", json=EMPLOYEE_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Alice Johnson"
    assert data["job_title"] == "Software Engineer"
    assert data["country"] == "India"
    assert data["salary"] == 80000.0
    assert "id" in data


def test_create_employee_missing_field_returns_422(client):
    response = client.post("/employees/", json={"full_name": "Bob"})
    assert response.status_code == 422


def test_create_employee_negative_salary_returns_422(client):
    response = client.post("/employees/", json={**EMPLOYEE_PAYLOAD, "salary": -1000})
    assert response.status_code == 422


def test_get_all_employees(client):
    client.post("/employees/", json=EMPLOYEE_PAYLOAD)
    client.post("/employees/", json={**EMPLOYEE_PAYLOAD, "full_name": "Bob Smith"})

    response = client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_all_employees_empty(client):
    response = client.get("/employees/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_employee_by_id(client):
    created = client.post("/employees/", json=EMPLOYEE_PAYLOAD).json()
    response = client.get(f"/employees/{created['id']}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Alice Johnson"


def test_get_employee_not_found(client):
    response = client.get("/employees/999")
    assert response.status_code == 404


def test_update_employee(client):
    created = client.post("/employees/", json=EMPLOYEE_PAYLOAD).json()
    response = client.patch(f"/employees/{created['id']}", json={"salary": 95000.0})
    assert response.status_code == 200
    assert response.json()["salary"] == 95000.0
    assert response.json()["full_name"] == "Alice Johnson"


def test_update_employee_not_found(client):
    response = client.patch("/employees/999", json={"salary": 95000.0})
    assert response.status_code == 404


def test_delete_employee(client):
    created = client.post("/employees/", json=EMPLOYEE_PAYLOAD).json()
    response = client.delete(f"/employees/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/employees/{created['id']}")
    assert response.status_code == 404


def test_delete_employee_not_found(client):
    response = client.delete("/employees/999")
    assert response.status_code == 404
