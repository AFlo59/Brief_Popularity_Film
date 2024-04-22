from films_predict.migrations import FilmModel
from utils.environment import get_env
import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from films_predict.items.jpbox import FilmItem

from sqlalchemy import select
from db.database_mysql import engine

BASE_URL = get_env("SCRAP_JP")
url_regex = r"/fichfilm\.php\?.*view=2$"
extractor = LinkExtractor(
    allow=url_regex, restrict_xpaths='//table[@class="tablesmall tablesmall5"]'
)


class AllMoviesSpider(scrapy.Spider):
    name = "all_movies"
    start_urls = [
        f"{BASE_URL}/v9_demarrage.php?view=2",
    ]

    def __init__(self):
        self.conn = engine.connect()
        stmt = select(FilmModel.url_jp)
        query = self.conn.execute(stmt)
        res = query.fetchall()
        self.films_exist = [r[0] for r in res]

    def parse(self, response: Response):
        try:
            item = FilmItem()
            yield from item.parse(response)
            print("parsed URL", response.url)
        except Exception:
            pass

        links = extractor.extract_links(response)

        urls = set([])
        for link in links:
            if link.url not in self.films_exist:
                urls.add(link.url)

        if len(urls) > 0:
            for url in urls:
                yield scrapy.Request(f"{url}")

        # check for next page in pagination
        next_page = response.xpath(
            '//div[@class="pagination"]/a[contains(text(), ">")]/@href'
        ).get()

        if next_page:
            yield scrapy.Request(f"{BASE_URL}{next_page}")
