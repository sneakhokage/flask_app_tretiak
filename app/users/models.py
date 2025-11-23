from .. import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import TYPE_CHECKING
from flask_bcrypt import generate_password_hash, check_password_hash

if TYPE_CHECKING:                
    from app.posts.models import Post

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def set_password(self, password):
        """Хешує пароль і зберігає його."""
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Перевіряє, чи співпадає введений пароль з хешем."""
        return check_password_hash(self.password, password)