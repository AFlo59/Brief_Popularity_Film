from urllib.parse import urlparse
from utils.environment import get_env
import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from films_predict.items import FilmItem

BASE_URL = get_env("SCRAP_JP")
# https://www.jpbox-office.com/fichfilm.php?id=10042&view=2
# https://www.jpbox-office.com/v9_demarrage.php?view=2&filtre=classg&limite=60&infla=0&variable=0&tri=champ0&order=DESC&limit5=0
url_regex = r"/fichfilm\.php"
extractor = LinkExtractor(allow=url_regex)


class AllMoviesSpider(scrapy.Spider):
    name = "all_movies"
    start_urls = [
        f"{BASE_URL}/v9_demarrage.php?view=2",
    ]

    def parse(self, response: Response):
        # item = FilmItem()
        # yield from item.parse(response)

        links = extractor.extract_links(response)
        print(links, len(links))
        # urls = set([])
        # for link in links:
        #     urls.add(urlparse(link.url).path)

        # for url in urls:
        #     yield scrapy.Request(f"{BASE_URL}{url}")
