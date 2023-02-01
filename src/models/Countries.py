from src.utils.database import db
from sqlalchemy import Column, Integer, String

class Country(db.Model):

    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(50), nullable = False)
    country_code = Column(String(2), nullable = False)

    def __repr__(self) -> str:
        return f'<Country >>> {self.country_code}>'