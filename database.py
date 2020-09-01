import sqlalchemy as alchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///app.db')

metadata = MetaData()


class Records(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    team = Column(String)
    league = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    org_founded = Column(Integer)
    expansion = Column(Boolean)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
