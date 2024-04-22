from urllib.parse import quote
from films_predict.migrations import FilmModel
from utils.string import convert_int, normalize
from utils.environment import get_env
import scrapy
from films_predict.items.allocine import FilmAlloItem
from scrapy.http import Response
from thefuzz import fuzz

from sqlalchemy import select
from db.database_mysql import engine

BASE_URL = get_env("SCRAP_ALLO")


class TestAlloSpider(scrapy.Spider):
    name = "test_allo"

    def __init__(self):
        self.conn = engine.connect()

    def start_requests(self):
        stmt = select(
            FilmModel.id, FilmModel.raw_title, FilmModel.year, FilmModel.director
        ).where(FilmModel.id == "0f20ac5b4bb8ca8c50a0ab930dc35309")
        query = self.conn.execute(stmt)
        film = query.fetchone()
        print("start", film.raw_title)

        url = f"{BASE_URL}/_/autocomplete/{quote(film.raw_title)}"

        yield scrapy.Request(
            url,
            callback=self.parse,
            cb_kwargs=dict(
                id_jp=film.id,
                raw_title=film.raw_title,
                year=film.year,
                director=film.director,
            ),
        )

    def parse(
        self, response: Response, id_jp="-1", id="-1", raw_title="", year=0, director=""
    ):
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
                    if (
                        "director_name" in result["data"]
                        and len(result["data"]["director_name"]) > 0
                    ):
                        print(result)
                        year_allo = convert_int(result["data"]["year"])
                        query_normalized = normalize(raw_title)
                        director_allo = normalize(result["data"]["director_name"][0])
                        if result["entity_type"] == "movie":
                            if (
                                normalize(result["original_label"]) == query_normalized
                                or normalize(result["label"]) == query_normalized
                            ):
                                print("search equality")
                                if director == director_allo and year_allo == year:
                                    yield self.create_request(
                                        result["entity_id"],
                                        id_jp,
                                        year,
                                        raw_title,
                                        director,
                                    )
                                    return True
                            elif (
                                fuzz.ratio(
                                    normalize(result["original_label"]),
                                    query_normalized,
                                )
                                > 85
                            ):
                                print("search original_label")
                                if director == director_allo and year_allo == year:
                                    yield self.create_request(
                                        result["entity_id"],
                                        id_jp,
                                        year,
                                        raw_title,
                                        director,
                                    )
                                    return True
                            else:
                                if (
                                    "text_search_data" in result
                                    and len(result["text_search_data"]) > 0
                                ):
                                    search_string = result["text_search_data"][0]

                                    if search_string is not None:
                                        for item_string in search_string.split(","):
                                            ratio = fuzz.ratio(
                                                normalize(item_string), query_normalized
                                            )
                                            print(
                                                "search string",
                                                ratio,
                                                normalize(item_string),
                                                query_normalized,
                                            )
                                            if ratio > 85:
                                                if (
                                                    director == director_allo
                                                    and year_allo == year
                                                ):
                                                    yield self.create_request(
                                                        result["entity_id"],
                                                        id_jp,
                                                        year,
                                                        raw_title,
                                                        director,
                                                    )
                    print()
            return True

    def create_request(self, entity_id, id_jp, year=0, raw_title="", director=""):
        return scrapy.Request(
            f"{BASE_URL}/film/fichefilm_gen_cfilm={entity_id}.html",
            self.parse,
            cb_kwargs=dict(
                id_jp=id_jp, id=entity_id, year=year, raw_title="", director=""
            ),
        )
