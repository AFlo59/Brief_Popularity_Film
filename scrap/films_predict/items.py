# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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
    copies = Field()

    def parse(self, response):
        hebdo_rank = -1
        copies = -1
        first_day = -1
        first_weekend = -1
        first_week = -1
        first_day = -1

        title = response.xpath("//h1/text()").get()
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

        self["title"] = normalize(title)
        self["director"] = normalize(director)
        self["raw_title"] = title.strip()
        self["raw_director"] = director.strip()
        self["url_jp"] = response.url
        self["year"] = convert_int(normalize(block_year_duration[0]))
        self["duration"] = TimeLength(block_year_duration[1]).to_seconds()
        self["country"] = block_country_genre[0]
        self["genre"] = block_country_genre[1]
        self["first_day"] = convert_int(normalize(first_day).replace(" ", ""))
        self["first_weekend"] = convert_int(normalize(first_weekend).replace(" ", ""))
        self["first_week"] = convert_int(normalize(first_week).replace(" ", ""))
        self["hebdo_rank"] = convert_int(hebdo_rank)
        self["copies"] = convert_int(normalize(copies).replace(" ", ""))

        # print("parse", self)

        yield self


class FilmAlloItem(Item):
    id = Field()
    id_jp = Field()
    rating_press = Field()
    rating_public = Field()
    casting = Field()
    synopsis = Field()
    distributor = Field()
    budget = Field()
    lang = Field()
    visa = Field()
    award = Field()

    def parse(self, response):
        ld_json = response.xpath(
            '//script[@type="application/ld+json"]/text()'
        ).extract()
        ld_json = json.loads(ld_json[0])

        casting = [actor["name"] for actor in ld_json["actor"]]
        synopsis = ld_json["description"]
        rating_public = ld_json["aggregateRating"]["ratingValue"]

        rating_press = response.xpath(
            '//div[@class="rating-mdl n25 stareval-stars"]/following-sibling::span[@class="stareval-note"]/text()'
        ).get()
        distributor = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "Distributeur")]]/span[contains(@class, "that blue-link")]/text()'
        ).get()
        award = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "Récompenses")]]/span[contains(@class, "that blue-link")]/text()'
        ).get()
        budget = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "Budget")]]/span[@class="that"]/text()'
        ).get()
        lang = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "Langues")]]/span[@class="that"]/text()'
        ).get()
        visa = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "Visa")]]/span[@class="that"]/text()'
        ).get()

        print(distributor)
        self["id"] = "sdfs"
        self["id_jp"] = "sdfsJP"
        self["rating_press"] = convert_float(rating_press)
        self["rating_public"] = convert_float(rating_public)
        self["casting"] = casting
        self["synopsis"] = synopsis
        self["distributor"] = distributor
        self["budget"] = convert_int(budget)
        self["lang"] = [normalize(lang) for lang in lang.split(sep=",")]
        self["visa"] = convert_int(visa.strip())

        if award is not None:
            match = re.search(r"([0-9]+) ?prix", award)
            try:
                award = match.groups()[0]
            except NoneType:
                award = 0

        self["award"] = convert_int(award)

        print(self)
        yield self
