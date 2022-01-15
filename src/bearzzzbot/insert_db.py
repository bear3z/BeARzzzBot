import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, Column, Boolean, Integer, String, MetaData
from sqlalchemy.dialects.postgresql import insert

load_dotenv()
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"), echo=True, future=True)

def insert_db(state):
    metadata = MetaData()
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('owner', String, unique=True, index=True),
        Column('wood', Boolean),
        Column('fire', Boolean),
        Column('one', Boolean),
        Column('two', Boolean),
        Column('three', Boolean),
    )

    with engine.connect() as conn:
        stmt = insert(users).values(
            owner = state[0],
            wood = state[1],
            fire = state[2],
            one = state[3],
            two = state[4],
            three = state[5]
        )

        update = stmt.on_conflict_do_update(
            index_elements=['owner'],
            set_= {
                "owner": state[0],
                "wood": state[1],
                "fire": state[2],
                "one": state[3],
                "two": state[4], 
                "three": state[5]
            }
        )
        result = conn.execute(update)
        conn.commit()