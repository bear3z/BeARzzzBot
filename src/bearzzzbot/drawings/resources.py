from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from bearzzzbot.deps import get_tx_session

from .insert_db import insert_db

router = APIRouter()


@router.get("/data/{statement}")
async def send_data_to_db(
    statement: str,
    db_session: Session = Depends(get_tx_session),
):
    stm = statement.split("&")
    data = []
    data.append(stm[0])

    for i in range(1, 6):
        if stm[i] == "true":
            data.append(1)
        else:
            data.append(0)
    insert_db(db_session, data)
    return "OK"
