import contextlib

from typing import TYPE_CHECKING

from fastapi import FastAPI
from loguru import logger
from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import PendingRollbackError

from .config import get_settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def make_db_engine():
    db_uri = get_settings().SQLALCHEMY_DATABASE_URI
    assert db_uri, db_uri
    url = make_url(str(db_uri)).set(drivername=db_uri.scheme)
    engine = create_engine(url, future=True)
    return engine


def connect_to_db(app: FastAPI) -> None:
    logger.debug("Connecting to db")

    engine = make_db_engine()
    app.state.engine = engine

    with engine.connect():
        ...

    logger.debug("Db connection established")


def close_db_connection(app: FastAPI) -> None:
    logger.debug("Closing connection to database")

    app.state.engine.dispose()

    logger.debug("Db connection closed")


def _rollback_implicit_tx(session: "Session") -> None:
    tx = session.transaction
    if session.in_transaction() and (not hasattr(tx, "_explicit") or not tx._explicit):
        session.rollback()


def _to_explicit_tx(session: "Session") -> None:
    tx = session.transaction
    setattr(tx, "_explicit", True)


@contextlib.contextmanager
def transaction(session: "Session"):
    try:
        _rollback_implicit_tx(session)

        if not session.in_transaction():
            with session.begin():
                _to_explicit_tx(session)
                yield
        else:
            with session.begin_nested():
                _to_explicit_tx(session)
                yield
    except PendingRollbackError:
        session.rollback()


__all__ = (
    "connect_to_db",
    "close_db_connection",
    "transaction",
)
