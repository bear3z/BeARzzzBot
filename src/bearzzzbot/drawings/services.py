from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from bearzzzbot.drawings.schemas import DrawingCreate, DrawingCreateIn, DrawingInDB

from .models import Drawing


def upsert_drawing(db_session: Session, drawing_in: DrawingCreateIn):
    values = DrawingCreate(**drawing_in.dict()).dict()
    stmt = pg.insert(Drawing).values(values)

    update = stmt.on_conflict_do_update(
        index_elements=["owner"],
        set_=values,
    )
    db_session.execute(update)


def get_drawing_by_owner(db_session: Session, owner: str):
    stmt = select(Drawing).where(Drawing.owner == owner)
    r = db_session.execute(stmt).scalars().first()
    if r:
        return DrawingInDB.from_orm(r)
