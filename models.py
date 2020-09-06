import sqlalchemy as alchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Franchises(Base):
    __tablename__ = 'franchises'

    # id = Column(Integer, primary_key=True)
    team_id = Column(String, primary_key=True)
    org_founded = Column(Integer)
    expansion = Column(Boolean)


class Records(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    team_id = Column(String, ForeignKey("franchises.team_id"))
    league = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    franchise = relationship(Franchises)
    # franchise_id = relationship("Franchises", back_populates="records")


# class Alt_Names(Base):
#     __tablename__ = 'alt_names'

#     alternate_name = Column(String, primary_key=True)
#     team_id = Column(String, ForeignKey('records.team_id'))
