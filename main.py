from fastapi import FastAPI
from app.database import init_db
from app.router import professors, students, courses

app = FastAPI()

init_db()

app.include_router(professors.router)
app.include_router(students.router)
app.include_router(courses.router)