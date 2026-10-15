from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.db import get_db

router = APIRouter(prefix="/api")


@router.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(body: schemas.CategoryIn, db: Session = Depends(get_db)) -> models.Category:
    cat = models.Category(name=body.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[models.Category]:
    return list(db.scalars(select(models.Category).order_by(models.Category.name)))


@router.post("/expenses", response_model=schemas.ExpenseOut, status_code=201)
def create_expense(body: schemas.ExpenseIn, db: Session = Depends(get_db)) -> models.Expense:
    if db.get(models.Category, body.category_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "category not found")
    exp = models.Expense(**body.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.get("/expenses", response_model=list[schemas.ExpenseOut])
def list_expenses(year: int, month: int, db: Session = Depends(get_db)) -> list[models.Expense]:
    start, end = services.month_bounds(year, month)
    stmt = (
        select(models.Expense)
        .where(models.Expense.spent_at >= start, models.Expense.spent_at < end)
        .order_by(models.Expense.spent_at.desc())
    )
    return list(db.scalars(stmt))


@router.get("/summary", response_model=list[schemas.CategoryTotal])
def summary(year: int, month: int, db: Session = Depends(get_db)) -> list[schemas.CategoryTotal]:
    start, end = services.month_bounds(year, month)
    rows = db.execute(
        select(models.Category.name, models.Expense.amount)
        .join(models.Expense.category)
        .where(models.Expense.spent_at >= start, models.Expense.spent_at < end)
    ).tuples()
    totals = services.totals_by_category(rows)
    return [schemas.CategoryTotal(category=k, total=v) for k, v in totals.items()]
