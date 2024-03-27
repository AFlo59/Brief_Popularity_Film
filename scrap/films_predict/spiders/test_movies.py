from utils.environment import get_env
import scrapy
from films_predict.items import FilmItem
from scrapy.http import Response

BASE_URL = get_env("SCRAP_JP")


class TestMoviesSpider(scrapy.Spider):
    name = "test_movies"
    start_urls = [
        f"{BASE_URL}/v9_demarrage.php?view=2",
    ]

    def parse(self, response: Response):
        item = FilmItem()
        return item.parse(response=response)
