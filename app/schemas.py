from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import List

### nested schemas must be defined first
class ShortResponseCourse(BaseModel):
    id: int
    name: str
    description: str
    ects: int

    class Config:
        from_attributes = True
    
class ShortResponseProfessor(BaseModel):
    id: int
    name: str
    faculty: str
    email: EmailStr

    class Config:
        from_attributes = True

### Base schemas

class CreateProfessor(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    faculty: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class UpdateProfessor(BaseModel):
    name: str = Field(default = None, min_length=1, max_length=50)
    faculty: str = Field(default = None, min_length=1, max_length=50)
    email: EmailStr = Field(default = None)

class ResponseProfessor(BaseModel):
    id: int
    name: str
    faculty: str
    email: EmailStr
    courses: List[ShortResponseCourse] = []

    class Config:
        from_attributes = True
 
class CreateCourse(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=200)
    ects: int = Field(..., ge=1, le=10)

class UpdateCourse(BaseModel):
    name: str = Field(default = None, min_length=1, max_length=50)
    description: str = Field(default = None, min_length=1, max_length=200)
    ects: int = Field(default = None, ge=1, le=10)

class ResponseCourse(BaseModel):
    id: int
    name: str
    description: str
    ects: int
    professor: ShortResponseProfessor

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    year: int = Field(..., ge=2000)

    @field_validator("year")
    @classmethod
    def year_validator(cls, value: int) -> int:
        if value > datetime.now().year:
            raise ValueError("Year cannot be in future")
        return value


class StudentUpdate(BaseModel):
    name: str = Field(default = None, min_length=1, max_length=50)
    email: EmailStr = Field(default = None)
    year: int = Field(default = None, ge=2000)

    @field_validator("year")
    @classmethod
    def year_validator(cls, value: int) -> int:
        if value > datetime.now().year:
            raise ValueError("Year cannot be in future")
        return value

class ShortStudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    year: int

class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    year: int
    course: ShortResponseCourse

    class Config:
        from_attributes = True


