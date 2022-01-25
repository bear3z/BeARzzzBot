from fastapi import HTTPException
from fastapi.param_functions import Body, Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from bearzzzbot.deps import get_db_session, get_tx_session
from bearzzzbot.drawings.schemas import DrawingCreateIn, DrawingRead

from . import services as svc

router = APIRouter()


@router.post("")
async def upsert_drawing(
    drawing_in: DrawingCreateIn = Body(...),
    db_session: Session = Depends(get_tx_session),
):
    svc.upsert_drawing(db_session, drawing_in)
    return "OK"


@router.get("", response_model=DrawingRead)
async def get_drawing(
    db_session: Session = Depends(get_db_session),
    owner: str = Query(""),
):
    if owner:
        return svc.get_drawing_by_owner(db_session, owner)
    raise HTTPException(status_code=404, detail="Drawing Not Found")
