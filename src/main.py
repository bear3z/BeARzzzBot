from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import Settings, get_settings
from .insert_db import insert_db

app = FastAPI()
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
):
    stm = statement.split("&")
    data = []
    data.append(stm[0])

    for i in range(1, 6):
        if stm[i] == "true":
            data.append(1)
        else:
            data.append(0)
    insert_db(data)
    return "OK"
