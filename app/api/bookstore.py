import json
import os
from datetime import date

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Extra

from elasticsearch import AsyncElasticsearch


class Prices(BaseModel):
    USD: str = "0.0"
    GPB: str = "0.0"
    EUR: str = "0.0"

    class Config:
        extra = Extra.allow


class Book(BaseModel):
    title: str
    author: str
    release_date: date = ""
    amazon_rating: int = ""
    best_seller: bool = ""
    prices: Prices = {}


router = APIRouter()

HTTP_CERT = os.getenv("ES_HTTP_CERT", "../../http_ca.crt")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD", "YNEx6c+8MPj+Ehe1Gp2I")

ES = AsyncElasticsearch(f"https://elastic:{ELASTIC_PASSWORD}@localhost:9200", verify_certs=False)


@router.put("/{book_id}")
async def add_book(book_id, payload: Book):
    await ES.index(index="books", id=book_id, document=jsonable_encoder(payload))
    return book_id


@router.get("/{book_id}")
async def get_book(book_id):
    resp = await ES.get(index="books", id=book_id)
    return resp["_source"]


@router.get("/")
async def get_all():
    all_books = await ES.search(index="books", body={
        'size': 10000,
        'query': {
            'match_all': {}
        }
    })
    print([doc["_source"] for doc in all_books["hits"]["hits"]])
