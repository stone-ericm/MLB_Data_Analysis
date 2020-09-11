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

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(metadata.sorted_tables):
        con.execute(table.delete())
    trans.commit()

from models import *


if __name__ == "__main__":
    Base.metadata.create_all(engine)
