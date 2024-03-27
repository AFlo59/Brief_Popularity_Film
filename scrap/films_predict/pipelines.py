# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime, timezone
from db.database_pg import session
from itemadapter import ItemAdapter
from films_predict.migrations import FilmModel
from utils.environment import get_env

from .items import FilmItem


class FilmsPipeline:
    def __init__(self) -> None:
        pass

    # def open_spider(self, spider):
    #     # print('********* open_spider')
    #     db = self.client[get_env("FILM_DB")]
    #     self.films = db["films"]

    # def close_spider(self, spider):
    #     # print('********* close_spider')
    #     self.client.close()

    def process_item(self, item: FilmItem, spider):
        film = FilmModel()
        film_item = ItemAdapter(item)
        film.title = film_item.get("title")
        film.time_updated = datetime.now(timezone.utc)

        print("process_item", film.__dict__)

        session.add(film)
        session.commit()
        return item
