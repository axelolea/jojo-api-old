from src.utils.database import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Character(db.Model):

    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable = False)
    japanese_name = Column(String(100), nullable = False)
    catchphrase = Column(String(200))
    is_stand_user = Column(Boolean, nullable = False)
    living = Column(Boolean)
    is_human = Column(Boolean, nullable = False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    images_id = Column(Integer, ForeignKey('images.id'))

    def __repr__(self) -> str:
        return f'<Character >>> {self.name}>'