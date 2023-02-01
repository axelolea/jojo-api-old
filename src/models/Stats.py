from src.utils.database import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Stats(db.Model):

    __tablename__ = 'stats'
    
    id = Column(Integer, primary_key=True)
    power = Column(String(8), nullable = False)
    speed = Column(String(8), nullable = False)
    range = Column(String(8), nullable = False)
    durability = Column(String(8), nullable = False)
    precision = Column(String(8), nullable = False)
    potential = Column(String(8), nullable = False)
    stand_id = Column(Integer, ForeignKey('stands.id'))

    def __repr__(self) -> str:
        return f'<Stats >>> {self.stand_id}>'