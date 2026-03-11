# Salary Management API

A RESTful API for managing employee records and salary calculations, built with Python and FastAPI.

## Tech Stack

- **Python 3.13**
- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Pydantic** — request/response validation
- **pytest + httpx** — testing

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

## Running Tests

```bash
pytest
```

## API Endpoints

### Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/employees/` | Create employee |
| GET | `/employees/` | List all employees |
| GET | `/employees/{id}` | Get employee by ID |
| PATCH | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |

**Employee fields:** `full_name`, `job_title`, `country`, `salary` (all required)

### Salary Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/salary/{employee_id}` | Get gross, TDS deduction, and net salary |

**Deduction rules:**
- India: 10% TDS
- United States: 12% TDS
- All other countries: no deduction

### Salary Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/metrics/country/{country}` | Min, max, avg salary for a country |
| GET | `/metrics/job-title/{job_title}` | Avg salary for a job title |

## Example Requests

```bash
# Create an employee
curl -X POST http://localhost:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Alice Johnson", "job_title": "Software Engineer", "country": "India", "salary": 80000}'

# Get salary breakdown
curl http://localhost:8000/salary/1

# Get country metrics
curl http://localhost:8000/metrics/country/India

# Get job title avg
curl http://localhost:8000/metrics/job-title/Software%20Engineer
```

