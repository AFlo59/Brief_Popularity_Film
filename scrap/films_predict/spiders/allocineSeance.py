import datetime
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
        stmt = (
            select(
                FilmSortieModel.date,
            )
            .group_by(FilmSortieModel.date)
            .order_by(FilmSortieModel.date)
        )

        query = self.conn.execute(stmt)
        dates = query.fetchall()

        for date in dates:
            print(date.date)
            stmt = select(
                FilmSortieModel.id,
                FilmSortieModel.title,
                FilmSortieModel.original_title,
                FilmSortieModel.director,
            ).where(FilmSortieModel.date == date.date)

            query = self.conn.execute(stmt)
            films = query.fetchall()

            url = f"https://www.allocine.fr/film/agenda/sem-{date.date}/"
            yield scrapy.Request(
                url,
                callback=self.parse,
                cb_kwargs=dict(films=films),
            )

            # print("parsed URL", url)

    def parse(self, response: Response, films):
        item = CopiesFromAllocine()
        return item.parse(response, films)
