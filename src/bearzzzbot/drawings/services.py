from sqlalchemy.dialects import postgresql as pg

from .models import Drawing


def upsert_drawing(db_session, state):
    stmt = pg.insert(Drawing).values(
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
