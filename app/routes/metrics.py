from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee

router = APIRouter()


@router.get("/country/{country}")
def country_metrics(country: str, db: Session = Depends(get_db)):
    result = db.query(
        func.min(Employee.salary),
        func.max(Employee.salary),
        func.avg(Employee.salary),
    ).filter(Employee.country == country).first()

    if result[0] is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")

    return {
        "country": country,
        "min_salary": result[0],
        "max_salary": result[1],
        "avg_salary": round(result[2], 2),
    }


@router.get("/job-title/{job_title}")
def job_title_metrics(job_title: str, db: Session = Depends(get_db)):
    result = db.query(func.avg(Employee.salary)).filter(Employee.job_title == job_title).scalar()

    if result is None:
        raise HTTPException(status_code=404, detail="No employees found for this job title")

    return {
        "job_title": job_title,
        "avg_salary": round(result, 2),
    }
