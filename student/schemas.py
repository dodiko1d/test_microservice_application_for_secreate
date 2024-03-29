""" Types Models for data between-components transferring.
I tried to use them less because in this specific situation it was easier
 and more operative-memory-friendly. """

from pydantic import BaseModel


class StudentCreation(BaseModel):
    faculty_id: int
    group_id: int
    student_id: int
    name: str
    surname: str
    patronymic: str
