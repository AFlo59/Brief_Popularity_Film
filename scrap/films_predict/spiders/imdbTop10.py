import json
from sqlalchemy import text
from films_predict.migrations import FilmSortieModel
from utils.environment import get_env
import scrapy
from films_predict.items.imdb import SortieImdbItem
from scrapy.http import Response
from db.database_mysql import engine
import dateparser


BASE_URL = get_env("SCRAP_IMDB")


class ImdbTop10MoviesSpider(scrapy.Spider):
    name = "imdb_top10_movies"

    start_urls = [
        f"{BASE_URL}/calendar/?region=FR",
    ]

    def __init__(self):
        conn = engine.connect()
        conn.execute(text(f"TRUNCATE TABLE {FilmSortieModel.__tablename__}"))
        # conn.commit()

    def parse(
        self, response: Response, id="", date=None, thumbnail="", title="", director=""
    ):
        if f"{BASE_URL}/title" in response.url:
            item = SortieImdbItem()
            item["id"] = id
            yield from item.parse(response, date, thumbnail)
            print("parsed URL", response.url)
        else:
            data = response.xpath('//script[@type="application/json"]/text()').get()
            data = json.loads(data)

            groups = data["props"]["pageProps"]["groups"]
            for group in groups:
                date = dateparser.parse(group["group"], languages=["fr"])

                date = date.date()

                for entry in group["entries"]:
                    if entry["titleType"]["id"] == "movie":
                        thumbnail = (
                            f"{entry['imageModel']['url']}"
                            if "imageModel" in entry
                            else "",
                        )

                        thumbnail = (
                            entry["imageModel"]["url"] if "imageModel" in entry else "",
                        )

                        yield scrapy.Request(
                            f"{BASE_URL}/title/{entry['id']}",
                            callback=self.parse,
                            cb_kwargs=dict(
                                id=entry["id"],
                                date=date,
                                thumbnail=thumbnail,
                            ),
                        )
