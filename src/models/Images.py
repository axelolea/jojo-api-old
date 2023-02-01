from src.utils.database import db
from sqlalchemy import Column, Text, Integer

class Image(db.Model):

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    half_body = Column(Text, nullable = False)
    full_body = Column(Text)

    def __repr__(self) -> str:
        return f'<Image >>> {self.id}>'