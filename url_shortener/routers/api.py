from fastapi import APIRouter
from url_shortener.routers.auth import auth_router

router = APIRouter()

API_PREFIX = "/api"


def include_api_routes():
    router.include_router(auth_router, prefix=API_PREFIX)


include_api_routes()
