from utils.environment import get_env
import scrapy
from films_predict.items import FilmItem, FilmAlloItem
from scrapy.http import Response

BASE_URL = get_env("SCRAP_JP")


class TestMoviesSpider(scrapy.Spider):
    name = "test_movies"
    start_urls = [
        # f"{BASE_URL}/fichfilm.php?id=22276&view=2",
        "https://www.allocine.fr/film/fichefilm_gen_cfilm=59308.html"
    ]

    def parse(self, response: Response):
        # item = FilmItem()
        item = FilmAlloItem()
        yield from item.parse(response=response)
