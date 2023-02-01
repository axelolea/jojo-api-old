from src.utils.database import db
from sqlalchemy import Column, Integer, String, Boolean

class Characther(db.Model):
    __tablename__ = 'characthers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    japanese_name = Column(String)
    catchphrase = Column(String)
    is_stand_user = Column(Boolean)
    living = Column(Boolean)
    is_human = Column(Boolean)
    country_id = Column(Integer)
    images_id = Column(Integer)
