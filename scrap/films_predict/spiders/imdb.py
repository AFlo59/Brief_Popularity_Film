import json
import time
from urllib.parse import quote
from films_predict.migrations import FilmModel
from utils.string import normalize
from utils.environment import get_env
import scrapy
from films_predict.items.imdb import FilmImdbItem
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
        stmt = (
            select(
                FilmModel.id,
                FilmModel.raw_title,
                FilmModel.original_title,
                FilmModel.year,
            )
            .where(FilmModel.scraped == 0)
            .order_by(FilmModel.total_spectator.desc())
        )
        query = self.conn.execute(stmt)
        films = query.fetchall()
        print("nb films : ", len(films))

        for film in films:
            url = f"https://www.imdb.com/find/?q={quote(film.original_title)}&s=tt&exact=true&ref_=fn_tt_ex"
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

            # time.sleep(0.2)

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
            yield from item.parse(response, raw_title, id_jp)
            print("parsed URL", response.url, raw_title)
        else:
            query_normalized = original_title
            raw_title_normalized = normalize(raw_title)

            data = response.xpath('//script[@type="application/json"]/text()').get()
            data = json.loads(data)

            results = data["props"]["pageProps"]["titleResults"]["results"]

            if len(results) == 0:
                url = f"https://www.imdb.com/find/?q={quote(original_title)}&ref_=nv_sr_sm"
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    cb_kwargs=dict(
                        id_jp=id_jp,
                        raw_title=raw_title,
                        original_title=original_title,
                        year_jp=year_jp,
                    ),
                )
                return None

            if len(results) == 1:
                id_imdb = results[0]["id"]
                year = (
                    results[0]["titleReleaseText"]
                    if "titleReleaseText" in results[0]
                    else None
                )
                yield self.create_request(
                    id_imdb,
                    id_jp,
                    year_jp=year,
                    raw_title=raw_title,
                    original_title=original_title,
                )
                return None

            similarities = []
            for result in results:
                if "imageType" in result and result["imageType"] == "movie":
                    id_imdb = result["id"]
                    year = (
                        result["titleReleaseText"]
                        if "titleReleaseText" in result
                        else None
                    )
                    title_l_norm = normalize(result["titleNameText"])

                    params = dict(
                        id_imdb=id_imdb,
                        id_jp=id_jp,
                        year_jp=year,
                        raw_title=raw_title,
                        original_title=original_title,
                    )

                    if (
                        title_l_norm == query_normalized
                        or title_l_norm == raw_title_normalized
                    ):
                        # print("search equality", raw_title, id_jp)
                        similarities.append(params)
                    elif (
                        fuzz.ratio(
                            title_l_norm,
                            query_normalized,
                        )
                        > 60
                        or fuzz.ratio(
                            title_l_norm,
                            raw_title_normalized,
                        )
                        > 60
                    ):
                        # print("search fuzz", raw_title, id_jp)
                        similarities.append(params)

            if len(similarities) == 1:
                yield self.create_request(**similarities[0])
            if len(similarities) > 1:
                for sim in similarities:
                    # print(sim, year_jp)
                    if sim["year_jp"] is not None and int(sim["year_jp"]) == year_jp:
                        yield self.create_request(**sim)

            return None

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
