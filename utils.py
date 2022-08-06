import random
import sys

import faker
from elasticsearch.helpers import bulk
from faker.providers import BaseProvider, currency, date_time, lorem, person, address

from app.elastic import get_elastic

fake = faker.Faker()


class Amazon(BaseProvider):
    def rate(self):
        return random.randint(1, 5)

    def is_best_seller(self):
        return random.choice([True, False])


class PriceList(BaseProvider):
    def price_list(self):
        return {
            fake.currency()[0]: fake.pricetag() for _ in range(random.randint(2, 5))
        }


class Covid(BaseProvider):
    def stats(self):
        return random.randint(1000, 100000)


fake.add_provider(person)
fake.add_provider(date_time)
fake.add_provider(currency)
fake.add_provider(lorem)
fake.add_provider(address)
fake.add_provider(Amazon)
fake.add_provider(PriceList)
fake.add_provider(Covid)


def gen_fake_books(num_docs: int):
    for doc_id in range(1, num_docs):
        _doc = {
            "_index": "books",
            "_id": doc_id,
            "_source": {
                "title": fake.sentence(nb_words=10),
                "author": fake.first_name() + " " + fake.last_name(),
                "release_date": fake.date(),
                "amazon_rating": fake.rate(),
                "best_seller": fake.is_best_seller(),
                "prices": fake.price_list(),
            },
        }
        print(f"{doc_id}: {_doc}")
        print("==================")
        yield _doc


def gen_fake_covid_stats(num_docs: int):
    for doc_id in range(1, num_docs):
        _doc = {
            "_index": "covid",
            "_id": doc_id,
            "_source": {
                "country": fake.country(),
                "date": fake.date(),
                "cases": fake.stats(),
                "deaths": fake.stats(),
                "recovered": fake.stats(),
                "critical": fake.stats(),
            },
        }
        print(f"{doc_id}: {_doc}")
        print("==================")
        yield _doc


if __name__ == "__main__":
    # establish connection.
    ES = get_elastic()

    # parse command line arguments
    num_records = int(sys.argv[1])
    index_name = sys.argv[2]

    print(num_records, index_name)

    if index_name == "books":
        bulk(ES, gen_fake_books(num_records))
    elif index_name == "covid":
        bulk(ES, gen_fake_covid_stats(num_records))

    ES.close()
