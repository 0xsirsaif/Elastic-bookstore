from fastapi import FastAPI, APIRouter


router = APIRouter()


@router.get("/ping")
async def ping():
    return {"PING": "PONG"}
