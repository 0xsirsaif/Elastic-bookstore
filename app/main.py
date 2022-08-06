import logging

from fastapi import FastAPI

from app.api import bookstore, ping, covid
from app.elastic import get_elastic

logger = logging.getLogger("uvicorn")


def generate_app() -> FastAPI:
    application = FastAPI()

    application.include_router(ping.router)
    application.include_router(bookstore.router, prefix="/bookstore", tags=["bookstore"])
    application.include_router(covid.router, prefix="/covid", tags=["covid"])

    return application


app = generate_app()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    get_elastic()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting Down... Closing Elastic Connection..")
    ES = get_elastic()
    ES.close()


@app.router.get("/")
async def home():
    return "HELLO!"
