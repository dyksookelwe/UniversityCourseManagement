from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(
    prefix="/student",
    tags=["students"]
)

@router.get("/", response_model=list[StudentResponse], status_code=200)
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.get("/{student_id}", response_model=StudentResponse, status_code=200)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).where(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student

@router.post("/", response_model=StudentCreate, status_code=201)
def create_student(student_info: Student, db: Session = Depends(get_db)):
    exist_student = db.query(Student).where(Student.name == student_info.name, Student.email == student_info.email).first()
    if exist_student is not None:
        raise HTTPException(
            status_code=404,
            detail="Student already exists"
        )
    new_student = Student(
        name = student_info.name,
        email = student_info.email,
        year = student_info.year
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.patch("/{student_id}", response_model = StudentUpdate, status_code=200)
def update_student(student_id: int, student_info: Student, db: Session = Depends(get_db)):
    exist_student = db.query(Student).where(Student.id == student_id).first()
    if exist_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    update_student = student_info.model_dump(exclude_unset=True)
    for key,value in update_student.items():
        setattr(exist_student, key, value)
    db.commit()
    db.refresh(exist_student)
    return exist_student

@router.delete("/{student_id}",status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    exist_student = db.query(Student).where(Student.id == student_id).first()
    if exist_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    if exist_student.courses:
        raise HTTPException(
            status_code=400,
            detail="Student have courses"
        )
    db.delete(exist_student)
    db.commit()
    return
    