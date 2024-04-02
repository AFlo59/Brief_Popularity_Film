from urllib.parse import quote
from films_predict.migrations import FilmModel
from utils.string import normalize
from utils.environment import get_env
import scrapy
from films_predict.items import FilmAlloItem
from scrapy.http import Response
from thefuzz import fuzz

from sqlalchemy import select
from db.database_mysql import engine

BASE_URL = get_env("SCRAP_ALLO")


class AlloCineMoviesSpider(scrapy.Spider):
    name = "allocine_movies"

    def __init__(self):
        self.conn = engine.connect()

    def start_requests(self):
        stmt = select(FilmModel.raw_title, FilmModel.id).limit(limit=30)
        query = self.conn.execute(stmt)
        films = query.fetchall()

        for item in films:
            url = f"{BASE_URL}/_/autocomplete/{quote(item.raw_title)}"
            yield scrapy.Request(
                url,
                callback=self.parse,
                cb_kwargs=dict(id_jp=item.id, raw_title=item.raw_title),
            )

        # self.query = "SPIDER-MAN : NO WAY HOME - VERSION LONGUE"
        # url = f"{BASE_URL}/_/autocomplete/{quote(self.query)}"

        # yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(id_jp="testets"))

    def parse(self, response: Response, id_jp="-1", id="-1", raw_title=""):
        if "fichefilm_gen_cfilm" in response.url:
            item = FilmAlloItem()
            item["id_jp"] = id_jp
            item["id"] = id
            yield from item.parse(response)
            print("parsed URL", response.url)
        else:
            json = response.json()
            if json["error"] is False:
                for result in json["results"]:
                    query_normalized = normalize(raw_title)
                    if (
                        normalize(result["original_label"]) == query_normalized
                        or normalize(result["label"]) == query_normalized
                    ):
                        yield self.create_request(result["entity_id"], id_jp, raw_title)
                    elif fuzz.ratio(result["original_label"], raw_title) > 90:
                        yield self.create_request(result["entity_id"], id_jp, raw_title)

    def create_request(self, entity_id, id_jp, raw_title):
        return scrapy.Request(
            f"{BASE_URL}/film/fichefilm_gen_cfilm={entity_id}.html",
            self.parse,
            cb_kwargs=dict(id_jp=id_jp, id=entity_id, raw_title=raw_title),
        )
