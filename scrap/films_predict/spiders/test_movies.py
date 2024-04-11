from utils.environment import get_env
import scrapy
from films_predict.items import FilmItem, FilmAlloItem
from scrapy.http import Response

SCRAP_JP = get_env("SCRAP_JP")
SCRAP_ALLO = get_env("SCRAP_ALLO")


class TestMoviesSpider(scrapy.Spider):
    name = "test_movies"
    start_urls = [
        f"{SCRAP_JP}/fichfilm.php?id=19753&view=2",
        # f"{SCRAP_ALLO}/film/fichefilm_gen_cfilm=28546.html"
    ]

    def parse(self, response: Response):
        item = FilmItem()
        # item = FilmAlloItem()
        # item["id_jp"] = "testidjp"
        # item["id"] = "testid"
        yield from item.parse(response=response)
