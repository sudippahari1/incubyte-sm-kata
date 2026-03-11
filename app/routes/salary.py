from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee

router = APIRouter()

TDS_RATES = {
    "India": 0.10,
    "United States": 0.12,
}


@router.get("/{employee_id}")
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    gross = employee.salary
    rate = TDS_RATES.get(employee.country, 0.0)
    tds = round(gross * rate, 2)

    return {
        "employee_id": employee.id,
        "gross_salary": gross,
        "tds": tds,
        "net_salary": round(gross - tds, 2),
    }
