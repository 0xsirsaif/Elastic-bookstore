import os
import logging
from typing import Optional

from elasticsearch import AsyncElasticsearch

logger = logging.getLogger("uvicorn")

HTTP_CERT: str = os.getenv("ES_HTTP_CERT", "../../http_ca.crt")
ELASTIC_PASSWORD: str = os.getenv("ELASTIC_PASSWORD", "YNEx6c+8MPj+Ehe1Gp2I")

ES: Optional[AsyncElasticsearch] = None


def get_elastic():
    global ES
    if not ES:
        ES = AsyncElasticsearch(f"https://elastic:{ELASTIC_PASSWORD}@localhost:9200", verify_certs=False)
    return ES
