# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from db.database_mysql import engine

import sqlalchemy.dialects.mysql as mysql
from itemadapter import ItemAdapter
from films_predict.migrations import FilmModel as model_jp
from films_predict.migrations import FilmAlloModel as model_allo

from .items import FilmAlloItem, FilmItem


class FilmsPipeline:
    # for postgres upsert
    # def __init__(self) -> None:
    # from sqlalchemy import inspect
    # insp = inspect(engine)
    # self.pk_constraint_id = insp.get_pk_constraint(model.__tablename__)["name"]

    def open_spider(self, spider):
        print("********* open_spider")
        self.conn = engine.connect()

    def close_spider(self, spider):
        print("********* close_spider")
        self.conn.close()

    def process_item(self, item: FilmItem | FilmAlloItem, spider):
        if isinstance(item, FilmItem):
            return self.handle_jp(item, spider)
        if isinstance(item, FilmAlloItem):
            return self.handle_allo(item, spider)

    def handle_jp(self, item: FilmItem, spider):
        film_item = ItemAdapter(item)

        id = f"{film_item.get('title')}-{film_item.get('director')}".encode("utf-8")
        film_item["id"] = hashlib.md5(id).hexdigest()

        save_item = film_item.asdict()

        ups_stmt = mysql.insert(model_jp).values(save_item)
        ups_stmt = ups_stmt.on_duplicate_key_update(**save_item)

        self.conn.execute(ups_stmt)
        self.conn.commit()

        return item

    def handle_allo(self, item: FilmAlloItem, spider):
        film_item = ItemAdapter(item)
        save_item = film_item.asdict()

        ups_stmt = mysql.insert(model_allo).values(save_item)
        ups_stmt = ups_stmt.on_duplicate_key_update(**save_item)

        self.conn.execute(ups_stmt)
        self.conn.commit()

        return item

    # upsert for postgres
    # from sqlalchemy.dialects.postgresql import insert
    # def process_item(self, item: FilmItem, spider):
    #     film_item = ItemAdapter(item)

    #     id = f"{film_item.get('title')}-{film_item.get('director')}".encode("utf-8")
    #     film_item["id"] = hashlib.md5(id).hexdigest()

    #     save_item = film_item.asdict()

    #     insert_stmt = insert(model).values(save_item)

    #     do_update_stmt = insert_stmt.on_conflict_do_update(
    #         constraint=self.pk_constraint_id, set_=save_item
    #     )

    #     self.conn.execute(do_update_stmt)
    #     self.conn.commit()

    #     return item
