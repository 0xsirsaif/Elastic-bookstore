from fastapi import FastAPI

from app.api import bookstore, ping

app = FastAPI()

app.include_router(ping.router)
app.include_router(bookstore.router, prefix="/bookstore", tags=["bookstore"])


@app.router.get("/")
async def home():
    return "HELLO!"
