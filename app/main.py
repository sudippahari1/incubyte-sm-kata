from fastapi import FastAPI
from app.database import Base, engine
from app.routes import employees, salary, metrics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salary Management API")

app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(salary.router, prefix="/salary", tags=["salary"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
