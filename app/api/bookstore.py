from fastapi import FastAPI, APIRouter

from elasticsearch import Elasticsearch

router = APIRouter()

# Create the client instance

@router.get("/")
async def get_info():
    client = Elasticsearch("https://localhost:9200")
    return {"INFO", client.info()}
