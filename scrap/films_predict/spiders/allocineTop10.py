from sqlalchemy import text
from films_predict.migrations import FilmSortieModel
from utils.environment import get_env
import scrapy
from films_predict.items.allocine import FilmAlloSortieItem
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from db.database_mysql import engine


BASE_URL = get_env("SCRAP_ALLO")
url_regex = r"/film/fichefilm_gen_cfilm=[0-9]+\.html$"
extractor = LinkExtractor(allow=url_regex, restrict_xpaths="//section/div/ul")


class AlloCineTop10MoviesSpider(scrapy.Spider):
    name = "allocine_top10_movies"

    start_urls = [
        f"{BASE_URL}/film/agenda/",
    ]

    def __init__(self):
        conn = engine.connect()
        conn.execute(text(f"TRUNCATE TABLE {FilmSortieModel.__tablename__}"))
        conn.commit()

    def parse(self, response: Response):
        try:
            # print("url before", response.url)
            item = FilmAlloSortieItem()
            yield from item.parse(response)
            print("parsed URL", response.url)
        except Exception as e:
            # print("******", e)
            pass

        links = extractor.extract_links(response)
        films = set([])
        for link in links:
            films.add(link.url)

        for film in films:
            yield scrapy.Request(film)

        # yield scrapy.Request(
        #     "https://www.allocine.fr/film/fichefilm_gen_cfilm=312488.html"
        # )
