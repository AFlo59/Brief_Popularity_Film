from urllib.parse import quote
from utils.string import convert_int, normalize
from utils.environment import get_env
import scrapy
from films_predict.items import FilmAlloItem
from scrapy.http import Response
from thefuzz import fuzz

BASE_URL = get_env("SCRAP_ALLO")


class TestAlloSpider(scrapy.Spider):
    name = "test_allo"

    def start_requests(self):
        self.query = "Samba"
        url = f"{BASE_URL}/_/autocomplete/{quote(self.query)}"

        print("start")
        yield scrapy.Request(
            url,
            callback=self.parse,
            cb_kwargs=dict(id_jp="testets", year=2000, director=""),
        )

    def parse(self, response: Response, id_jp="-1", id="-1", year=0, director=""):
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
                    query_normalized = normalize(self.query)
                    director_allo = normalize(result["data"]["director_name"][0])
                    if result["entity_type"] == "movie":
                        if (
                            normalize(result["original_label"]) == query_normalized
                            or normalize(result["label"]) == query_normalized
                        ):
                            if director == director_allo:
                                yield self.create_request(
                                    result["entity_id"], id_jp, year
                                )

                            return True
                        elif fuzz.ratio(result["original_label"], self.query) > 90:
                            if director == director_allo:
                                yield self.create_request(
                                    result["entity_id"], id_jp, year
                                )

                            return True

    def create_request(self, entity_id, id_jp, year):
        return scrapy.Request(
            f"{BASE_URL}/film/fichefilm_gen_cfilm={entity_id}.html",
            self.parse,
            cb_kwargs=dict(id_jp=id_jp, id=entity_id, year=year),
        )
