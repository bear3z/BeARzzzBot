from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import insert


def insert_db(db_session, state):
    metadata = MetaData()
    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("owner", String, unique=True, index=True),
        Column("wood", Boolean),
        Column("fire", Boolean),
        Column("one", Boolean),
        Column("two", Boolean),
        Column("three", Boolean),
    )

    stmt = insert(users).values(
        owner=state[0],
        wood=state[1],
        fire=state[2],
        one=state[3],
        two=state[4],
        three=state[5],
    )

    update = stmt.on_conflict_do_update(
        index_elements=["owner"],
        set_={
            "owner": state[0],
            "wood": state[1],
            "fire": state[2],
            "one": state[3],
            "two": state[4],
            "three": state[5],
        },
    )
    db_session.execute(update)
