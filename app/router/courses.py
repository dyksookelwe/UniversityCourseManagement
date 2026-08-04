from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Course, Professor
from app.schemas import CreateCourse, ResponseCourse, ShortResponseProfessor

router = APIRouter(
    prefix="/course",
    tags=["courses"]
)

@router.get("/", response_model=list[ResponseCourse], status_code=200)
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@router.get("/{course_id}", response_model=ResponseCourse, status_code=200)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).where(Course.id == course_id).first()
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return course

@router.get("/{course_id}/professors", response_model=list[ShortResponseProfessor], status_code=200)
def get_professor_courses(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).where(Course.id == course_id).first()
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    if course.professor:
        raise HTTPException(
            status_code=404,
            detail="Professor has no courses"
        )
    return course.professor

@router.post("/", response_model=CreateCourse, status_code=201)
def create_course(course_info: Course, db: Session = Depends(get_db)):
    exist_course = db.query(Course).where(Course.name == course_info.name, Course.ects == course_info.ects).first()
    if exist_course is not None:
        raise HTTPException(
            status_code=404,
            detail="Professor already exist"
        )
    exist_professor = db.query(Professor).where(Professor.id == course_info.professor_id).first()
    if exist_professor is None or course_info.professor_id != exist_professor.id:
        raise HTTPException(
            status_code=404,
            detail="Professor is not exist"
        )
    new_course = Course(
        name = course_info.name,
        description = course_info.description,
        ects = course_info.ects
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.patch("/{course_id}", response_model=ResponseCourse, status_code=200)
def update_course(course_id: int, course_info: Course, db: Session = Depends(get_db)):
    exist_course = db.query(Course).where(Course.id == course_id).first()
    if exist_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    update_course = course_info.model_dump(exclude_unset=True)
    for key,value in update_course.items():
        setattr(exist_course,key,value)
    db.commit()
    db.refresh(exist_course)
    return exist_course

@router.delete("/{course_id}", status_code=204)
def delete_course(course_id:int, db:Session = Depends(get_db)):
    exist_course = db.query(Course).where(Course.id == course_id).first()
    if exist_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    if exist_course.students:
        raise HTTPException(
            status_code=400,
            detail="Course have students, delete them first"
        )
    db.delete(exist_course)
    db.commit()
    return 