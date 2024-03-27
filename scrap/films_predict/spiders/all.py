from urllib.parse import urlparse
import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from films_predict.items import FilmsItem

BASE_URL = "https://www.imdb.com"
url_regex = r"/title\/(tt[0-9]+)(\/?\?ref_)+"
extractor = LinkExtractor(allow=url_regex)


class AllMoviesSpider(scrapy.Spider):
    name = "all_movies"
    start_urls = [
        "https://www.imdb.com/title/tt0094794",
    ]

    def parse(self, response: Response):
        item = FilmsItem()
        yield from item.parse(response)

        links = extractor.extract_links(response)
        urls = set([])
        for link in links:
            urls.add(urlparse(link.url).path)

        for url in urls:
            yield scrapy.Request(f"{BASE_URL}{url}")
