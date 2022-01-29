""" Controllers are containing main part of site's business-logic. """

from sqlalchemy.orm import Session
from sqlalchemy import literal
# from products_group import controller as products_group_controller

from . import model, schemas


def get_by_students_record_book_id(db: Session, students_record_book_id: int):
    return db.query(model.Student).filter(model.Student.students_record_book_id == students_record_book_id).first()


def get_student_data_by_students_record_book_id(db: Session, students_record_book_id: int):
    db_student = db.query(model.Student).filter(model.Student.students_record_book_id == students_record_book_id).first()
    return {
        'students_record_book_id': db_student.students_record_book_id,
        'name': db_student.name,
        'surname': db_student.surname,
        'patronymic': db_student.patronymic,
        'full_name': db_student.full_name,
        'group_id': db_student.studying_group.id,
        'group_specialization': db_student.studying_group.specialization,
        'faculty_id': db_student.studying_group.faculty.id,
        'faculty_name': db_student.studying_group.faculty.name,
        'reference_list': [reference.text for reference in db_student.references],
    }


def create(db: Session, student: schemas.StudentCreation):
    db_student = model.Student(
        students_record_book_id=student.faculty_id + student.group_id + student.student_id,
        name=student.name,
        surname=student.surname,
        patronymic=student.patronymic,
        full_name=f'{student.surname} {student.name} {student.patronymic}'
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return get_student_data_by_students_record_book_id(student.faculty_id + student.group_id + student.student_id)


def remove_by_students_record_book_id(db: Session, students_record_book_id: int):
    student = get_by_students_record_book_id(db=db, students_record_book_id=students_record_book_id)
    db.delete(student)
    db.commit()
    return {'200': 'Student has been successfully removed.'}


def create_reference(db: Session, students_record_book_id: int, reference_text: str):
    pass


# def change_studying_group(db: Session, students_record_book_id: int, new_studying_group_id: int):
#     product = __get_product_instance_by_id(db=db, product_id=product_id)
#     group = products_group_controller.__get_products_group_instance_by_id(db=db, products_group_id=new_group_id)
#     if not group:
#         return 'There is not group with such ID'
#     product.group_id = new_group_id
#     product.group = group
#     db.commit()
#     db.refresh(product)
#     return product

