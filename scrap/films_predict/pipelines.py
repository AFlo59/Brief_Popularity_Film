# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from sqlalchemy import inspect
from db.database_pg import engine

from sqlalchemy.dialects.postgresql import insert
from itemadapter import ItemAdapter
from films_predict.migrations import FilmModel

from .items import FilmItem


class FilmsPipeline:
    def __init__(self) -> None:
        insp = inspect(engine)
        self.pk_constraint_id = insp.get_pk_constraint(FilmModel.__tablename__)["name"]

    def open_spider(self, spider):
        print("********* open_spider")
        self.conn = engine.connect()

    def close_spider(self, spider):
        print("********* close_spider")
        self.conn.close()

    def process_item(self, item: FilmItem, spider):
        film_item = ItemAdapter(item)

        id = f"{film_item.get('title')}-{film_item.get('director')}".encode("utf-8")
        film_item["id"] = hashlib.md5(id).hexdigest()

        save_item = film_item.asdict()

        insert_stmt = insert(FilmModel).values(save_item)

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint=self.pk_constraint_id, set_=save_item
        )

        self.conn.execute(do_update_stmt)
        self.conn.commit()

        return item
