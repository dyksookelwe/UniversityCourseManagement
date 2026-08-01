from app.database import Base
from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Professor(Base):
    __tablename__ = "professors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True
    )
    name: Mapped[str] = mapped_column(
        String(50)
    )
    faculty: Mapped[str] = mapped_column(
        String(50)
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique = True
    )
    courses = relationship(
        "Course",
        back_populates = "professor"
    )

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True
    )
    name: Mapped[str] = mapped_column(
        String(50)
    )
    description: Mapped[str] = mapped_column(
        String(200)
    )
    ects: Mapped[int] = mapped_column(
        Integer
    )
    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professors.id")
    )

    professor = relationship(
        "Professor",
        back_populates = "courses"
    )
    students = relationship(
        "Student",
        secondary = student_course,
        back_populates = "courses"
        )

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True
    )
    name: Mapped[str] = mapped_column(
        String(50)
    )
    email: Mapped[str] = mapped_column(
        String(50),
        unique = True
    )
    year: Mapped[int] = mapped_column(
        Integer
    )
    courses = relationship(
        "Course",
        secondary = student_course,
        back_populates = "students"
    )