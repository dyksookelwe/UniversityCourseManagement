from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Professor
from app.database import get_db
from app.schemas import CreateProfessor, ResponseProfessor, ShortResponseCourse, UpdateProfessor

router = APIRouter(
    prefix="/professor",
    tags=["professors"]
)

@router.get("/{professor_id}", response_model=ResponseProfessor, status_code=200)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.query(Professor).where(Professor.id == professor_id).first()
    if professor is None: 
        raise HTTPException(
            status_code = 404,
            detail = "Professor not found"
        )
    return professor

@router.get("/", response_model=list[ResponseProfessor], status_code=200)
def get_professors(db: Session = Depends(get_db)):
    professors = db.query(Professor).all()
    return professors

@router.get("/{professor_id}/courses", response_model=list[ShortResponseCourse], status_code=200)
def get_professor_courses(professor_id: int, db: Session = Depends(get_db)):
    exist_professor = db.query(Professor).where(Professor.id == professor_id).first()
    if exist_professor is None:
        raise HTTPException(
            status_code=404,
            detail="Professor not found"
        )
    if not exist_professor.courses:
        raise HTTPException(
            status_code=404,
            detail="Professor has no courses"
        )
    return exist_professor.courses

@router.post("/", response_model=CreateProfessor, status_code=201)
def create_professor(professor_info: Professor, db: Session = Depends(get_db)):
    existing_professor = db.query(Professor).where(Professor.name == professor_info.name, Professor.email == professor_info.email).first()
    if existing_professor is not None:
        raise HTTPException(
            status_code=409,
            detail = "Professor is already exist"
        )
    new_professor = Professor(
        name = professor_info.name,
        faculty = professor_info.faculty,
        email = professor_info.email
    )
    db.add(new_professor)
    db.commit()
    db.refresh(new_professor)
    return new_professor

@router.patch("/{professor_id}", response_model=UpdateProfessor, status_code=200)
def update_professor(professor_data: Professor, db: Session = Depends(get_db)):
    exist_professor = db.query(Professor).where(Professor.id == professor_data.id).first()
    if exist_professor is None:
        raise HTTPException(
            status_code=404,
            detail="Professor not found"
        )
    update_professor = professor_data.model_dump(exclude_unset=True)
    for key, value in update_professor.items():
        setattr(exist_professor,key,value)
    db.commit()
    db.refresh(exist_professor)
    return exist_professor

@router.delete("/{professor_id}", status_code=204)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    exist_professor = db.query(Professor).where(Professor.id == professor_id).first()
    if exist_professor is None:
        raise HTTPException(
            status_code=404,
            detail="Professor not found"
        )
    if exist_professor.courses:
        raise HTTPException(
            status_code=400,
            detail="Professor have courses, delete them first"
        )
    db.delete(exist_professor)
    db.commit()
    return
    

    
