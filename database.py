from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# database settings
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'password',
    'database': 'apartments'
}

DeclarativeBase = declarative_base()


class Apartment(DeclarativeBase):
    __tablename__ = 'apartment'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    imageURL = Column('imageURL', String)
    title = Column('title', String)
    date = Column('date', String)
    location = Column('location', String)
    bedrooms = Column('bedrooms', String)
    description = Column('description', String)
    price = Column('price', String)


    def __repr__(self):
        return "".format(self.code)

def database_connection():
    engine = create_engine(URL(**DATABASE))

    DeclarativeBase.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    new_apartment = Apartment(imageURL='URL',
                              title='Title',
                              date='09-10-2022',
                              location='LA',
                              bedrooms='4',
                              description='Some text',
                              price='500')
    session.add(new_apartment)

    session.commit()

    for item in session.query(Apartment):
        print(item)