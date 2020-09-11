if input("Running this will clear the database. Are you sure you want to proceed? (Y/N)\n").lower() == "y":
    pass
else:
    quit()


import sqlalchemy as alchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
if os.path.isfile("app.db"):
    os.remove("app.db")
Base = declarative_base()
engine = create_engine('sqlite:///app.db')

metadata = MetaData()

from models import *


if __name__ == "__main__":
    Base.metadata.create_all(engine)
