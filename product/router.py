from fastapi import APIRouter, Depends, HTTPException
from . import schemas, controller
from sqlalchemy.orm import Session
from database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post('/create/')
async def create(product: schemas.ProductCreation, db: Session = Depends(get_db)):
    db_product = controller.get_product_by_stock_keeping_unit(db, product)
    if db_product:
        raise HTTPException(status_code=400, detail="Product is already registered.")
    controller.create_product(db=db, product=product)
    return {'status_code': '200'}
