from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .db import close_db_connection, connect_to_db
from .deps import get_tx_session
from .insert_db import insert_db


def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.APP_NAME)
    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    async def home_get(request: Request, settings: Settings = Depends(get_settings)):
        return templates.TemplateResponse(
            "main.html",
            {
                "request": request,
                "liffID": settings.LIFFID,
            },
        )

    @app.get("/data/{statement}")
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

    @app.on_event("startup")
    async def on_startup() -> None:  # pragma: no cover
        connect_to_db(app)

    @app.on_event("shutdown")
    async def on_shutdown() -> None:  # pragma: no cover
        close_db_connection(app)

    return app
