from .. import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager

if TYPE_CHECKING:                
    from app.posts.models import Post

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    image: Mapped[str] = mapped_column(String(20), nullable=True, default='profile_default.jpg')
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    about_me: Mapped[str | None] = mapped_column(String(140), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def set_password(self, password):
        """Хешує пароль і зберігає його."""
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Перевіряє, чи співпадає введений пароль з хешем."""
        return check_password_hash(self.password, password)