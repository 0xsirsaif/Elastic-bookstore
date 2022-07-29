from fastapi import FastAPI

from app.api import ping
from app.api import bookstore

app = FastAPI()

app.include_router(ping.router)
app.include_router(bookstore.router, prefix="/bookstore", tags=["bookstore"])

