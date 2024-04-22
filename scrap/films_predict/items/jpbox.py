# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
import html
import json
import re
from types import NoneType
from utils.string import convert_float, convert_int, normalize
from scrapy.item import Item, Field
import isodate
from timelength import TimeLength


class FilmItem(Item):
    id = Field()
    title = Field()
    original_title = Field()
    director = Field()
    raw_title = Field()
    raw_director = Field()
    url_jp = Field()
    year = Field()
    country = Field()
    duration = Field()
    genre = Field()
    first_day = Field()
    first_weekend = Field()
    first_week = Field()
    hebdo_rank = Field()
    total_spectator = Field()
    copies = Field()
    date = Field()

    def parse(self, response):
        hebdo_rank = -1
        copies = -1
        first_day = -1
        first_weekend = -1
        first_week = -1
        first_day = -1
        total_spectator = -1

        title = response.xpath("//h1/text()").get()
        original_title = response.xpath("//h1/following-sibling::h2/text()").get()
        director = response.xpath("//h1/following-sibling::h4/a/text()").get()

        block_year_duration = response.xpath(
            "//h1/following-sibling::h3/text()"
        ).extract()
        block_year_duration = [normalize(info) for info in block_year_duration]
        block_year_duration = [info for info in block_year_duration if info]

        block_country_genre = response.xpath(
            "//h1/following-sibling::h3/a/text()"
        ).extract()
        block_country_genre = [normalize(info) for info in block_country_genre]

        first_day = response.xpath(
            '//td[@class="col_poster_titre"]/*[contains(text(), "Premier jour")]/parent::td/following-sibling::td[@class="col_poster_contenu_majeur"]/text()'
        ).get()

        first_weekend = response.xpath(
            '//td[@class="col_poster_titre"][contains(text(), "Premier week-end")]/following-sibling::td/text()'
        ).get()

        first_week = response.xpath(
            '//td[@class="col_poster_titre"][contains(text(), "Première semaine")]/following-sibling::td/text()'
        ).get()

        date_sortie = response.xpath(
            '//div[@class="bloc_infos_center tablesmall1b"]/p[contains(text(), "Sortie")]/a/text()'
        ).get()

        if date_sortie is not None:
            date_sortie = date_sortie.strip()
            hebdo_rank = response.xpath(
                f'//h4/a[contains(text(), "{date_sortie}")]/ancestor::tr/td[5]/text()'
            ).get()
            copies = response.xpath(
                f'//h4/a[contains(text(), "{date_sortie}")]/ancestor::tr/td[6]/text()'
            ).get()

            d = datetime.datetime.strptime(date_sortie, "%d/%m/%Y")
            date_sortie = f"{d.year}-{d.month}-{d.day}"

        total_spectator = response.xpath(
            '//td[@class="col_poster_titre"]/h4[contains(text(), "Entrées")]/parent::td/following-sibling::td/text()'
        ).get()

        self["title"] = normalize(title)
        self["original_title"] = (
            normalize(original_title) if original_title is not None else self["title"]
        )
        self["director"] = normalize(director) if director is not None else None
        self["raw_director"] = director.strip() if director is not None else None
        self["raw_title"] = title.strip()
        self["url_jp"] = response.url
        self["year"] = convert_int(normalize(block_year_duration[0]))
        self["duration"] = (
            -1
            if len(block_year_duration) == 1
            else TimeLength(block_year_duration[1]).to_seconds()
        )
        self["country"] = block_country_genre[0]
        self["genre"] = block_country_genre[1]
        self["first_day"] = convert_int(normalize(first_day).replace(" ", ""))
        self["first_weekend"] = convert_int(normalize(first_weekend).replace(" ", ""))
        self["first_week"] = convert_int(normalize(first_week).replace(" ", ""))
        self["hebdo_rank"] = convert_int(hebdo_rank)
        self["copies"] = convert_int(normalize(copies).replace(" ", ""))
        self["total_spectator"] = convert_int(
            normalize(total_spectator).replace(" ", "")
        )
        self["date"] = date_sortie

        print(self["raw_title"])
        # print("parse", self)

        yield self
