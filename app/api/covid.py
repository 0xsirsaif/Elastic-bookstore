from fastapi import APIRouter

from app.elastic import get_elastic

ES = get_elastic()

router = APIRouter()


@router.get("/count")
async def count_docs():
    """
    count all documents in the books index
    """
    total_count = await ES.count(index="covid")
    return total_count["count"]