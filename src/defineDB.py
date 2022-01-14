import os
from dotenv import load_dotenv
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"), echo=True)

conn = engine.connect()

metadata = MetaData()
users = Table('users', metadata,
    
    Column('id', Integer, primary_key=True),
    Column('owner', String, unique=True, index=True),
    # Column('owner', String),
    Column('wood', Boolean),
    Column('fire', Boolean),
    Column('one', Boolean),
    Column('two', Boolean),
    Column('three', Boolean),
)
metadata.create_all(engine)