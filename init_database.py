if input("Running this will clear the database. Are you sure you want to proceed? (Y/N)\n").lower() == "y":
    pass
else:
    quit()

import contextlib
from sqlalchemy import MetaData


import sqlalchemy as alchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
# if os.path.isfile("app.db"):
#     os.remove("app.db")
Base = declarative_base()

engine = create_engine('postgresql://postgres:password@localhost/MLB_app')

metadata = MetaData()

# Base.metadata.drop_all(engine)

from models import *
if engine.dialect.has_table(engine, 'records'):
    Records.__table__.drop(engine)
if engine.dialect.has_table(engine, 'franchises'):
    Franchises.__table__.drop(engine)
if engine.dialect.has_table(engine, 'annual_avgs'):
    Annual_Expansion_And_Non_Record.__table__.drop(engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
