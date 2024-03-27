# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import html
import isodate
from timelength import TimeLength


class FilmItem(Item):
    title = Field()
    director = Field()
    year = Field()
    country = Field()
    duration = Field()
    genre = Field()
    first_day = Field()
    first_weekend = Field()
    first_week = Field()
    hebdo_rank = Field()
    copies = Field()

    def parse(self, response):
        print(response.url)
        title = response.xpath(
            "//*[@id='content']/table[2]/tr[2]/td[3]/h3/a/text()"
        ).extract()

        self["title"] = html.unescape(title.pop())

        print("parse", self["title"])

        yield self
