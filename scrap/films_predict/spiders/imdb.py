import time
from urllib.parse import quote
from films_predict.migrations import FilmModel
from utils.string import convert_int, normalize
from utils.environment import get_env
import scrapy
from films_predict.items import FilmImdbItem
from scrapy.http import Response
from thefuzz import fuzz

from sqlalchemy import select
from db.database_mysql import engine

BASE_URL = get_env("SCRAP_IMDB")


class ImdbMoviesSpider(scrapy.Spider):
    name = "imdb_movies"

    def __init__(self):
        self.conn = engine.connect()

    def start_requests(self):
        stmt = select(
            FilmModel.id, FilmModel.raw_title, FilmModel.original_title, FilmModel.year
        ).where(FilmModel.scraped == 0)

        query = self.conn.execute(stmt)
        films = query.fetchall()
        for film in films:
            url = f"https://v3.sg.media-imdb.com/suggestion/x/{quote(film.raw_title)}.json?includeVideos=0"

            if film.original_title is not None:
                url = f"https://v3.sg.media-imdb.com/suggestion/x/{quote(film.original_title)}.json?includeVideos=0"

            yield scrapy.Request(
                url,
                callback=self.parse,
                cb_kwargs=dict(
                    id_jp=film.id,
                    raw_title=film.raw_title,
                    original_title=film.original_title,
                    year_jp=film.year,
                ),
            )

            time.sleep(0.2)

    def parse(
        self,
        response: Response,
        id_jp="-1",
        id="-1",
        year_jp=0,
        raw_title="",
        original_title="",
    ):
        if f"{BASE_URL}/title" in response.url:
            item = FilmImdbItem()
            item["id_jp"] = id_jp
            item["id"] = id
            yield from item.parse(response)
            print("** parsed URL", response.url)
        else:
            json = response.json()
            if json["v"] == 1:
                for result in json["d"]:
                    if "qid" in result and result["qid"] == "movie" and "y" in result:
                        id_imdb = result["id"]
                        year = convert_int(result["y"])
                        title_l_norm = normalize(result["l"])
                        query_normalized = original_title
                        if title_l_norm == query_normalized:
                            # print("search equality", original_title)
                            # if year == year_jp:
                            yield self.create_request(
                                id_imdb,
                                id_jp,
                                year_jp=year,
                                raw_title=raw_title,
                                original_title=original_title,
                            )
                            return True
                        elif (
                            fuzz.ratio(
                                title_l_norm,
                                query_normalized,
                            )
                            > 50
                            # and year == year_jp
                        ):
                            # print("search original_label")
                            yield self.create_request(
                                id_imdb,
                                id_jp,
                                year_jp=year,
                                raw_title=raw_title,
                                original_title=original_title,
                            )
                            return True
            return True

    def create_request(
        self, id_imdb, id_jp, year_jp=0, raw_title="", original_title=""
    ):
        return scrapy.Request(
            f"{BASE_URL}/title/{id_imdb}",
            self.parse,
            cb_kwargs=dict(
                id_jp=id_jp,
                id=id_imdb,
                year_jp=year_jp,
                raw_title=raw_title,
                original_title=original_title,
            ),
        )
