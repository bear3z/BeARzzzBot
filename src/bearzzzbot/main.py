from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import Settings, get_settings
from .db import close_db_connection, connect_to_db
from .routes import api_router


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

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def on_startup() -> None:  # pragma: no cover
        connect_to_db(app)

    @app.on_event("shutdown")
    async def on_shutdown() -> None:  # pragma: no cover
        close_db_connection(app)

    return app
