import pytest


def create_employee(client, country, salary=100000.0):
    return client.post("/employees/", json={
        "full_name": "Test Employee",
        "job_title": "Developer",
        "country": country,
        "salary": salary,
    }).json()


def test_salary_calculation_india(client):
    employee = create_employee(client, country="India", salary=100000.0)
    response = client.get(f"/salary/{employee['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["tds"] == 10000.0
    assert data["net_salary"] == 90000.0


def test_salary_calculation_united_states(client):
    employee = create_employee(client, country="United States", salary=100000.0)
    response = client.get(f"/salary/{employee['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["tds"] == 12000.0
    assert data["net_salary"] == 88000.0


def test_salary_calculation_other_country(client):
    employee = create_employee(client, country="Germany", salary=100000.0)
    response = client.get(f"/salary/{employee['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["tds"] == 0.0
    assert data["net_salary"] == 100000.0


def test_salary_calculation_employee_not_found(client):
    response = client.get("/salary/999")
    assert response.status_code == 404


def test_salary_response_includes_employee_id(client):
    employee = create_employee(client, country="India", salary=50000.0)
    response = client.get(f"/salary/{employee['id']}")
    assert response.json()["employee_id"] == employee["id"]
