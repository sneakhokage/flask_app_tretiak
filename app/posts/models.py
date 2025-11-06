from app import db  
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column  
from sqlalchemy import String, Text, DateTime, func  

class Post(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)


    title: Mapped[str] = mapped_column(String(100), nullable=False)


    content: Mapped[str] = mapped_column(Text, nullable=False)


    posted: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'