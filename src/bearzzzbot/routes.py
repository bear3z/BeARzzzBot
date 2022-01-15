from fastapi.routing import APIRouter

from bearzzzbot.drawings.resources import router as drawing_router

api_router = APIRouter()


api_router.include_router(drawing_router, prefix="/drawing")
