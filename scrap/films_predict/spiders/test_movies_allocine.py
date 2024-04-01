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
        self.query = "Les Bronzés 3: Amis pour la vie"
        url = f"{BASE_URL}/_/autocomplete/{quote(self.query)}"

        yield scrapy.Request(url, self.parse)

    def parse(self, response: Response):
        if "fichefilm_gen_cfilm" in response.url:
            item = FilmAlloItem()
            yield from item.parse(response)
            print("parsed URL", response.url)
        else:
            json = response.json()
            if json["error"] is False:
                for result in json["results"]:
                    if normalize(result["original_label"]) == normalize(self.query):
                        yield self.create_request(result["entity_id"])
                    elif fuzz.ratio(result["original_label"], self.query) > 90:
                        yield self.create_request(result["entity_id"])

    def create_request(self, entity_id):
        return scrapy.Request(
            f"{BASE_URL}/film/fichefilm_gen_cfilm={entity_id}.html", self.parse
        )
