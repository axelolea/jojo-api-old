from src.utils.database import db
from sqlalchemy import Column, Integer, String

class Part(db.Model):

    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable = False, unique=True)
    japanese_name = Column(String(100), nullable = False, unique=True)
    romanization_name = Column(String(100), nullable = False, unique=True)
    alther_name = Column(String(100))

    def __repr__(self) -> str:
        return f'<Part >>> {self.name}>'