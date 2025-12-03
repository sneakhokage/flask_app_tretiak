from .. import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class CourseCategory(db.Model):
    __tablename__ = 'course_categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True) 

    courses: Mapped[list["Course"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"{self.name}"

class Course(db.Model):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=True) 
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category_id: Mapped[int] = mapped_column(ForeignKey('course_categories.id'), nullable=False)
    category: Mapped["CourseCategory"] = relationship(back_populates="courses")

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship("User") 

    def __repr__(self):
        return f"<Course {self.title}>"