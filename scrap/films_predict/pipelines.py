# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from db.database import connect_db
from itemadapter import ItemAdapter
from utils.environment import get_env

from .items import FilmsItem


class FilmsPipeline:
    def __init__(self) -> None:
        self.client = connect_db()

    def open_spider(self, spider):
        # print('********* open_spider')
        db = self.client[get_env("FILM_DB")]
        self.films = db["films"]

    def close_spider(self, spider):
        # print('********* close_spider')
        self.client.close()

    def process_item(self, item: FilmsItem, spider):
        json = ItemAdapter(item).asdict()

        self.films.update_one(
            filter={"_id": json["_id"]}, upsert=True, update={"$set": json}
        )
        return item
