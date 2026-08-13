from fastapi import Depends, FastAPI

from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.routers.transactions import router as transaction_router
from backend.routers.categories import router as category_router
from backend.routers.users import router as user_router


app = FastAPI(
    title="Balanzo API",
    description="Personal finance management API",
    version="1.0.0",
)


app.include_router(transaction_router)

app.include_router(category_router)

app.include_router(user_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Balanzo API"
    }



@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/api/health/database")
def database_health_check(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }