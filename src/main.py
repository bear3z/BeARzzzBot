import os
from .insert_db import insert_db
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
load_dotenv()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home_get(
    request: Request,
):
    liffID = os.getenv("liffID")
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "liffID": liffID,
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