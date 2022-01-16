from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm.session import Session

from src.bearzzzbot.drawings.schemas import DrawingCreate, DrawingCreateIn

from .models import Drawing


def upsert_drawing(db_session: Session, drawing_in: DrawingCreateIn):
    values = DrawingCreate(**drawing_in.dict()).dict()
    stmt = pg.insert(Drawing).values(values)

    update = stmt.on_conflict_do_update(
        index_elements=["owner"],
        set_=values,
    )
    db_session.execute(update)
