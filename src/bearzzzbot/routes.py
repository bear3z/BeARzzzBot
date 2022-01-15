from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from bearzzzbot.drawings.resources import router as drawing_router

api_router = APIRouter(default_response_class=ORJSONResponse)


api_router.include_router(drawing_router, prefix="/drawing")
