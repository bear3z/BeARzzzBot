from typing import cast

from fastapi import Request
from fastapi.param_functions import Depends
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from .db import transaction


def get_db_engine(request: Request) -> Engine:
    return request.app.state.engine


def get_db_session(
    engine: Engine = Depends(get_db_engine),
):
    with Session(engine) as session:
        yield cast("Session", session)


def get_tx_session(session: Session = Depends(get_db_session)):
    with transaction(session):
        yield session
