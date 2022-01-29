""" Database Product Model. """

from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from database import Base
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = 'student'

    students_record_book_id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    full_name = Column(String)
    studying_group = relationship('StudyingGroup', back_populates='students_of_group')
    references = relationship('Reference', back_populates='student_reference_creating_for')
