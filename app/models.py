from app.database import Base
from sqlalchemy import Integer, String
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
        "Professor",
        back_populates = "professors"
    )