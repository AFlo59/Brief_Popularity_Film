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


class BaseFilmAlloItem(Item):
    url_allo = Field()
    year_allo = Field()
    director_allo = Field()
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

        casting = []
        synopsis = ""
        rating_public = -1
        year_allo = -1
        director = []

        if len(ld_json) > 0:
            ld_json = json.loads(ld_json[0])

            try:
                casting = [actor["name"] for actor in ld_json["actor"]]
            except Exception:
                pass

            try:
                synopsis = ld_json["description"]
            except Exception:
                pass

            try:
                rating_public = ld_json["aggregateRating"]["ratingValue"]
            except Exception:
                pass

            if "director" in ld_json:
                try:
                    director = [
                        normalize(director["name"]) for director in ld_json["director"]
                    ]
                except Exception:
                    director = [normalize(ld_json["director"]["name"])]

        rating_press = response.xpath(
            '//*[contains(@class, "rating-title") and contains(text(), "Presse")]/parent::div/div/span[@class="stareval-note"]/text()'
        ).get()
        if rating_public == -1:
            rating_public = response.xpath(
                '//*[contains(@class, "rating-title") and contains(text(), "Spectateur")]/parent::div/div/span[@class="stareval-note"]/text()'
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

        year_allo = response.xpath(
            #'//div[contains(@class, "meta-body-info")]/span[contains(@class, "date")]/text()'
            '//div[@class="item" and span[@class="what light" and contains(text(), "de production")]]/span[@class="that"]/text()'
        ).get()

        if year_allo is not None:
            year_allo = re.findall("([0-9]{4})", year_allo)
            try:
                self["year_allo"] = convert_int(year_allo[0])
            except Exception:
                pass

        self["url_allo"] = response.url
        self["rating_press"] = convert_float(rating_press)
        self["rating_public"] = convert_float(rating_public)
        self["casting"] = casting
        self["synopsis"] = (
            "" if isinstance(synopsis, str) is False else synopsis.strip()
        )
        self["distributor"] = (
            "" if isinstance(distributor, str) is False else normalize(distributor)
        )
        self["budget"] = convert_int(budget)
        self["lang"] = [normalize(lang) for lang in lang.split(sep=",")]
        self["visa"] = convert_int(visa.strip())
        self["director_allo"] = director

        if award is not None:
            match = re.search(r"([0-9]+) ?prix", award)
            try:
                award = match.groups()[0]
            except Exception:
                award = 0

        self["award"] = convert_int(award, 0)

        yield self


class FilmAlloItem(BaseFilmAlloItem):
    id = Field()
    id_jp = Field()

    # self["id"] = "sdfs"           -> dans le spider allocine
    # self["id_jp"] = "sdfsJP"      -> dans le spider allocine


class FilmAlloSortieItem(BaseFilmAlloItem):
    thumbnail = Field()
    title = Field()
    director_raw = Field()
    duration = Field()
    genre = Field()

    def parse(self, response):
        year_allo = response.xpath(
            '//div[@class="item" and span[@class="what light" and contains(text(), "de production")]]/span[@class="that"]/text()'
        ).get()

        if year_allo is not None:
            year_allo = re.findall("([0-9]{4})", year_allo)
            try:
                year_allo = convert_int(year_allo[0])
            except Exception:
                pass

        if year_allo == datetime.datetime.now().year:
            ld_json = response.xpath(
                '//script[@type="application/ld+json"]/text()'
            ).extract()

            if len(ld_json) > 0:
                ld_json = json.loads(ld_json[0])

                if "director" in ld_json:
                    try:
                        self["director_raw"] = ld_json["director"]["name"]
                    except Exception:
                        self["director_raw"] = [ld_json["director"]["name"]]

                if "genre" in ld_json:
                    try:
                        self["genre"] = ld_json["genre"]
                    except Exception:
                        self["genre"] = [
                            response.xpath(
                                '//a[contains(@href, "genre-") and contains(@clas, "dark-grey-link")]/text()'
                            ).get()
                        ]

            self["thumbnail"] = response.xpath(
                '//section/div//img[@class="thumbnail-img"]/@src'
            ).get()
            self["title"] = response.xpath(
                '//main//div[@class="titlebar-title titlebar-title-xl"]/text()'
            ).get()

            duration = response.xpath(
                '//div[@class="meta-body-item meta-body-info"]/strong/following-sibling::span/following-sibling::text()'
            ).get()

            self["duration"] = (
                TimeLength(duration).to_seconds() if len(duration) >= 1 else None
            )

            return super().parse(response)

        return True
