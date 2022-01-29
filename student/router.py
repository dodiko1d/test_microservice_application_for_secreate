""" Site paths work control - call necessary controllers. """

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


async def check_product_existence(product_id: int, db: Session = Depends(get_db)):
    db_product = controller.get_product_data_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=400, detail='Product with this id does not exist.')


@router.post('/create/', summary='Create student account.')
async def create(student: schemas.StudentCreation, db: Session = Depends(get_db)):
    db_student = controller.get_by_students_record_book_id(
        db=db,
        students_record_book_id=student.faculty_id + student.group_id + student.student_id
    )
    if db_student:
        raise HTTPException(status_code=400, detail='Some student already has this id.')
    student_record = controller.create(db=db, student=student)
    return {
        'status_code': 200,
        'data': student_record,
    }


@router.post(
    '/remove/{product_id}',
    summary='Remove a product.',
    dependencies=[Depends(check_product_existence)]
)
async def remove(product_id: int, db: Session = Depends(get_db)):
    controller.remove_product(db=db, product_id=product_id)
    return {'status_code': '200'}


@router.post(
    '/change_property/{product_id}/{property_name}/{new_property_value}',
    summary='Change product property.',
    dependencies=[Depends(check_product_existence)]
)
async def change_product_property(product_id: int, property_name: str, new_property_value, db: Session = Depends(get_db)):
    return controller.change_product_property(db=db, product_id=product_id,
                                              property_name=property_name,
                                              new_property_value=new_property_value)


@router.post(
    '/increase_stock_balance/{product_id}/{increasing_value}',
    summary='Increase product stock balance.',
    dependencies=[Depends(check_product_existence)]
)
def increase_stock_balance(product_id: int, increasing_value: int, db: Session = Depends(get_db)):
    return controller.increase_stock_balance(db=db, product_id=product_id, increasing_value=increasing_value)


@router.post(
    '/reduce_stock_balance/{product_id}/{reducing_value}',
    summary='Reduce product stock balance.',
    dependencies=[Depends(check_product_existence)]
)
def reduce_stock_balance(product_id: int, reducing_value: int, db: Session = Depends(get_db)):
    return controller.reduce_stock_balance(db=db, product_id=product_id, reducing_value=reducing_value)


@router.post(
    '/get_rest_not_reserved_product/{product_id}',
    summary='Get rest not reserved product amount.',
    dependencies=[Depends(check_product_existence)]
)
def get_rest_not_reserved_product(product_id: int, db: Session = Depends(get_db)):
    return controller.get_rest_not_reserved_product(db=db, product_id=product_id)


@router.post(
    '/increase_reserved_product/{product_id}/{increasing_value}',
    summary='Increase reserved product.',
    dependencies=[Depends(check_product_existence)]
)
def increase_reserved_product(product_id: int, increasing_value: int, db: Session = Depends(get_db)):
    controller.increase_reserved_product(db=db, product_id=product_id, increasing_value=increasing_value)


@router.post(
    '/reduce_reserved_product/{product_id}/{reducing_value}',
    summary='Reduce reserved product.',
    dependencies=[Depends(check_product_existence)]
)
def reduce_reserved_product(product_id: int, reducing_value: int, db: Session = Depends(get_db)):
    return controller.reduce_reserved_product(db=db, product_id=product_id, reducing_value=reducing_value)


@router.post(
    '/reduce_reserved_product/{product_id}/{new_group_id}',
    summary='Change product group.',
    dependencies=[Depends(check_product_existence)]
)
def change_product_group(product_id: int, new_group_id: int, db: Session = Depends(get_db)):
    return controller.change_product_group(db=db, product_id=product_id, new_group_id=new_group_id)
