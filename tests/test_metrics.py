import pytest


def create_employee(client, country, job_title, salary):
    return client.post("/employees/", json={
        "full_name": "Test Employee",
        "job_title": job_title,
        "country": country,
        "salary": salary,
    }).json()


def test_country_metrics_min_max_avg(client):
    create_employee(client, "India", "Engineer", 60000.0)
    create_employee(client, "India", "Manager", 90000.0)
    create_employee(client, "India", "Analyst", 75000.0)

    response = client.get("/metrics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "India"
    assert data["min_salary"] == 60000.0
    assert data["max_salary"] == 90000.0
    assert data["avg_salary"] == 75000.0


def test_country_metrics_single_employee(client):
    create_employee(client, "Germany", "Developer", 80000.0)

    response = client.get("/metrics/country/Germany")
    assert response.status_code == 200
    data = response.json()
    assert data["min_salary"] == 80000.0
    assert data["max_salary"] == 80000.0
    assert data["avg_salary"] == 80000.0


def test_country_metrics_not_found(client):
    response = client.get("/metrics/country/Narnia")
    assert response.status_code == 404


def test_country_metrics_excludes_other_countries(client):
    create_employee(client, "India", "Engineer", 70000.0)
    create_employee(client, "United States", "Engineer", 120000.0)

    response = client.get("/metrics/country/India")
    data = response.json()
    assert data["min_salary"] == 70000.0
    assert data["max_salary"] == 70000.0


def test_job_title_avg_salary(client):
    create_employee(client, "India", "Software Engineer", 80000.0)
    create_employee(client, "United States", "Software Engineer", 120000.0)

    response = client.get("/metrics/job-title/Software Engineer")
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Software Engineer"
    assert data["avg_salary"] == 100000.0


def test_job_title_avg_salary_not_found(client):
    response = client.get("/metrics/job-title/Wizard")
    assert response.status_code == 404


def test_job_title_avg_salary_single_employee(client):
    create_employee(client, "India", "CTO", 200000.0)

    response = client.get("/metrics/job-title/CTO")
    assert response.status_code == 200
    assert response.json()["avg_salary"] == 200000.0
