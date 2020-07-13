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
async def create(products_group: schemas.ProductsGroupCreation, db: Session = Depends(get_db)):
    db_products_group = controller.get_products_group_by_id(db, products_group)
    if db_products_group:
        raise HTTPException(status_code=400, detail="Product is already registered.")
    controller.create_products_group(db=db, products_group=products_group)
    return {'status_code': '200'}
