# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime, timezone
import hashlib

from sqlalchemy import insert, update
from db.database_pg import session
from sqlalchemy.orm.exc import NoResultFound
from itemadapter import ItemAdapter
from films_predict.migrations import FilmModel

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
        film_item = ItemAdapter(item)

        print(f"{film_item.get('title')}-{film_item.get('director')}")

        id = f"{film_item.get('title')}-{film_item.get('director')}".encode("utf-8")
        film_item["id"] = hashlib.md5(id).hexdigest()

        save_item = film_item.asdict()
        # save_item["time_updated"] = datetime.now(timezone.utc)

        print("process_item", save_item)

        if session.get(FilmModel, save_item["id"]) is None:
            session.execute(insert(FilmModel), [save_item])
        else:
            session.execute(update(FilmModel), [save_item])

        session.commit()
        return item
