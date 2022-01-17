from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from bearzzzbot.deps import get_tx_session
from bearzzzbot.drawings.schemas import DrawingCreateIn

from . import services as svc

router = APIRouter()


@router.post("")
async def upsert_drawing(
    drawing_in: DrawingCreateIn = Body(...),
    db_session: Session = Depends(get_tx_session),
):
    svc.upsert_drawing(db_session, drawing_in)
    return "OK"
