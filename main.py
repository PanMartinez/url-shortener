from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from url_shortener.config.settings import get_settings


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()

