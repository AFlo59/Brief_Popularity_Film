import re
from urllib.parse import quote
from films_predict.migrations import FilmModel, FilmSortieModel
from films_predict.items.imdb import CopiesFromAllocine
from utils.string import convert_int, normalize
from utils.environment import get_env
import scrapy
from scrapy.http import Response
from thefuzz import fuzz

from sqlalchemy import select
from db.database_mysql import engine

BASE_URL = get_env("SCRAP_ALLO")


class AlloCineSeancesSpider(scrapy.Spider):
    name = "allocine_seances"

    def __init__(self):
        self.conn = engine.connect()

    def start_requests(self):
        stmt = select(
            FilmSortieModel.id,
            FilmSortieModel.title,
            FilmSortieModel.original_title,
            FilmSortieModel.date,
            FilmSortieModel.director,
        )  # .limit(limit=1)
        query = self.conn.execute(stmt)
        films = query.fetchall()

        for item in films:
            url = f"https://www.allocine.fr/film/agenda/sem-{item.date}/"
            print(item.id)
            yield scrapy.Request(
                url,
                callback=self.parse,
                cb_kwargs=dict(
                    id=item.id,
                    title=item.title,
                    original_title=item.original_title,
                    date=item.date,
                    director=item.director,
                ),
            )

            print("parsed URL", url)

    def parse(
        self,
        response: Response,
        id=None,
        title="",
        original_title="",
        date=None,
        director="",
    ):
        item = CopiesFromAllocine()
        return item.parse(
            response,
            id=id,
            title=title,
            original_title=original_title,
            date=date,
            director=director,
        )
