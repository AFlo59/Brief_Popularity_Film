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
    total_spectator = Field()
    copies = Field()

    def parse(self, response):
        hebdo_rank = -1
        copies = -1
        first_day = -1
        first_weekend = -1
        first_week = -1
        first_day = -1
        total_spectator = -1

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

        total_spectator = response.xpath(
            '//td[@class="col_poster_titre"]/h4[contains(text(), "Entrées")]/parent::td/following-sibling::td/text()'
        ).get()

        self["title"] = normalize(title)
        self["director"] = normalize(director)
        self["raw_title"] = title.strip()
        self["raw_director"] = director.strip()
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

        # print("parse", self)

        yield self


class BaseFilmAlloItem(Item):
    id = Field()
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
            '//div[contains(@class, "meta-body-info")]/span[contains(@class, "date")]/text()'
        ).get()

        if self["year_allo"] != -1 and year_allo is not None:
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
            "" if isinstance(distributor, str) is False else distributor.strip()
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

        # print(self)
        yield self


class FilmAlloSortieItem(BaseFilmAlloItem):
    thumbnail = Field()

    def parse(self, response):
        yield from super().parse(response)
        self.thumbnail = "ess"

        yield self


class FilmAlloItem(BaseFilmAlloItem):
    id_jp = Field()

    # self["id"] = "sdfs"           -> dans le spider allocine
    # self["id_jp"] = "sdfsJP"      -> dans le spider allocine
