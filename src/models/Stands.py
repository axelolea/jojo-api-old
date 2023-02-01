from src.utils.database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey

class Stand(db.Model):

    __tablename__ = 'stands'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable = False)
    japanese_name = Column(String(100), nullable = False)
    alther_name = Column(String(100))
    abilities = Column(Text, nullable = False)
    battlecry = Column(String(120))
    images_id = Column(Integer, ForeignKey('images.id'))

    def __repr__(self) -> str:
        return f'<Character >>> {self.name}>'