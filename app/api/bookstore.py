import os
from datetime import date

from elasticsearch import AsyncElasticsearch

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Extra


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

ES = AsyncElasticsearch(
    f"https://elastic:{ELASTIC_PASSWORD}@localhost:9200", verify_certs=False
)


async def query_param_as_list(q: str):
    list_of_params = [str(doc_id) for doc_id in q.split(",")]
    return list_of_params


@router.get("/count")
async def count_docs():
    """
    count all documents in the books index
    """
    total_count = await ES.count(index="books")
    return total_count["count"]


@router.get("/all")
async def get_all():
    """
    Get all Documents
    {
        'took': 1,
        'timed_out': False,
        '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
        'hits': {'total': {'value': 10000, 'relation': 'gte'}, 'max_score': 1.0, 'hits': [*** DATA IS HERE ***]}
    }
    """
    all_books = await ES.search(
        index="books", body={"size": 1000, "query": {"match_all": {}}}
    )

    return [doc["_source"] for doc in all_books["hits"]["hits"]]


@router.get("/multi")
async def get_multiple_docs(ids: list = Depends(query_param_as_list)):
    multiple_books = await ES.search(index="books", query={"ids": {"values": ids}})
    return [doc["_source"] for doc in multiple_books["hits"]["hits"]]


@router.get("/by_field/{field}/{field_value}")
async def get_docs_by_field(field: str = None, field_value: str = None, exact: bool = False):
    """
    By default, the engine is implicitly adding an (OR) operator when creating a search query with multiple words.
    Use (AND) Operator explicitly
    """
    query = {
        "match": {
            field: field_value
        }
    }
    if exact:
        query["match"] = {field: {"query": field_value, "operator": "AND"}}

    docs = await ES.search(index="books", query=query)

    return [doc["_source"] for doc in docs["hits"]["hits"]]


@router.put("/{book_id}")
async def add_doc(book_id: str, payload: Book):
    """
    Add new or modify an existing document
    """
    await ES.index(index="books", id=book_id, document=jsonable_encoder(payload))
    return book_id


@router.get("/{book_id}")
async def get_doc(book_id: str):
    """
    Get Document by id
    """
    resp = await ES.get_source(index="books", id=book_id)
    return resp

