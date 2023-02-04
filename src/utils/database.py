from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, Table, ForeignKey

# Connection Database
db = SQLAlchemy()

# Many to many raltion tables 

character_stand = db.Table(
    'character_stand_table',
    Column('character_id', Integer, ForeignKey('characters_table.id'), primary_key=True),
    Column('stand_id', Integer, ForeignKey('stands_table.id'), primary_key=True)
)

character_part = db.Table(
    'character_part_table',
    Column('character_id', Integer, ForeignKey('characters_table.id'), primary_key=True),
    Column('part_id', Integer, ForeignKey('parts_table.id'), primary_key=True)
)

stand_part = db.Table(
    'stand_part_table',
    Column('stand_id', Integer, ForeignKey('stands_table.id'), primary_key=True),
    Column('part_id', Integer, ForeignKey('parts_table.id'), primary_key=True)
)


class Character(db.Model):
    
    __tablename__ = 'characters_table'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable = False)
    alther_name = Column(String(100))
    japanese_name = Column(String(100), nullable = False)
    catchphrase = Column(String(200))
    is_hamon_user = Column(Boolean, nullable = False)
    is_stand_user = Column(Boolean, nullable = False)
    is_gyro_user = Column(Boolean, nullable = False)
    living = Column(Boolean)
    is_human = Column(Boolean, nullable = False)
    country_id = Column(ForeignKey('countries_table.id'))
    images_id = Column(ForeignKey('images_table.id'))

    # One to One relationships

    user_images = db.relationship('Image', back_populates = 'character_images')
    user_country = db.relationship('Country', back_populates = 'character_country')

    # Many to many relationships

    user_stands = db.relationship('Stand', secondary = character_stand , backref='users')
    user_parts = db.relationship('Part', secondary = character_part , backref='users')

    def __repr__(self) -> str:
        return format_repr('Character', self.name)


class Country(db.Model):

    __tablename__ = 'countries_table'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    country_name = Column(String(50), nullable = False)
    country_code = Column(String(2), nullable = False)

    # One to one relationships 
    character_country = db.relationship('Character', back_populates = 'user_country')

    def __repr__(self) -> str:
        return format_repr('Country', self.country_code)


class Image(db.Model):

    __tablename__ = 'images_table'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    half_body = Column(Text, nullable = False)
    full_body = Column(Text)

    # One to one relationship 

    character_images = db.relationship('Character', back_populates = 'user_images')


    def __repr__(self) -> str:
        return format_repr('Image', self.id)


class Part(db.Model):

    __tablename__ = 'parts_table'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable = False, unique=True)
    number = Column(Integer, nullable=False, unique=True)
    japanese_name = Column(String(100), nullable = False, unique=True)
    romanization_name = Column(String(100), nullable = False, unique=True)
    alther_name = Column(String(100))

    # Many to many relationship 

    part_users = db.relationship('Character', secondary = character_part , backref='parts', viewonly=True)
    part_stands = db.relationship('Stand', secondary = stand_part , backref='parts', viewonly=True)
    
    def __repr__(self) -> str:
        return format_repr('Part', self.name)


class Stand(db.Model):

    __tablename__ = 'stands_table'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable = False)
    japanese_name = Column(String(100), nullable = False)
    alther_name = Column(String(100))
    abilities = Column(Text, nullable = False)
    battlecry = Column(String(120))
    images_id = Column(Integer, ForeignKey('images_table.id'))

    # Many to many relationship 

    stand_users = db.relationship('Character', secondary = character_stand , backref='stands', viewonly=True)
    stand_parts = db.relationship('Part', secondary = stand_part , backref='stands')

    def __repr__(self) -> str:
        return format_repr('Stand', self.name)


class Stats(db.Model):

    __tablename__ = 'stats_table'
    
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    power = Column(String(8), nullable = False)
    speed = Column(String(8), nullable = False)
    range = Column(String(8), nullable = False)
    durability = Column(String(8), nullable = False)
    precision = Column(String(8), nullable = False)
    potential = Column(String(8), nullable = False)
    stand_id = Column(Integer, ForeignKey('stands_table.id'))

    def __repr__(self) -> str:
        return format_repr('Stats', self.stand_id)





# Format class __repr__
def format_repr(name, value):
    return f'<{name} >>> {value}>'