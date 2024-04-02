from urllib.parse import quote
from utils.string import normalize
from utils.environment import get_env
import scrapy
from films_predict.items import FilmAlloItem
from scrapy.http import Response
from thefuzz import fuzz

BASE_URL = get_env("SCRAP_ALLO")


class TestAlloSpider(scrapy.Spider):
    name = "test_allo"

    def start_requests(self):
        # Les Ames soeurs
        self.query = "Matrix"
        url = f"{BASE_URL}/_/autocomplete/{quote(self.query)}"

        print("start")
        yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(id_jp="testets"))

    def parse(self, response: Response, id_jp="-1", id="-1"):
        if "fichefilm_gen_cfilm" in response.url:
            print("parse 2")
            item = FilmAlloItem()
            item["id_jp"] = id_jp
            item["id"] = id
            yield from item.parse(response)
            print("parsed URL", response.url)
        else:
            print("parse 3")
            json = response.json()
            if json["error"] is False:
                for result in json["results"]:
                    query_normalized = normalize(self.query)

                    if (
                        normalize(result["original_label"]) == query_normalized
                        or normalize(result["label"]) == query_normalized
                    ):
                        print("okkokoko")
                        yield self.create_request(result["entity_id"], id_jp)
                        return True
                    elif fuzz.ratio(result["original_label"], self.query) > 90:
                        yield self.create_request(result["entity_id"], id_jp)
                        return True

    def create_request(self, entity_id, id_jp):
        return scrapy.Request(
            f"{BASE_URL}/film/fichefilm_gen_cfilm={entity_id}.html",
            self.parse,
            cb_kwargs=dict(id_jp=id_jp, id=entity_id),
        )
