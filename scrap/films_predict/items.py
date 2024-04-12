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


class FilmImdbItem(Item):
    id = Field()
    id_jp = Field()
    url = Field()
    title = Field()
    original_title = Field()
    director = Field()
    rating_press = Field()
    rating_public = Field()
    casting = Field()
    synopsis = Field()
    distributor = Field()
    budget = Field()
    lang = Field()
    award = Field()
    date = Field()

    def parse(self, response, raw_title, id_jp):
        # print("***** item", raw_title, id_jp)
        data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        data = json.loads(data)

        self["original_title"] = html.unescape(data["name"]) if "name" in data else None
        self["title"] = (
            html.unescape(data["alternateName"])
            if "alternateName" in data
            else self["original_title"]
        )
        self["url"] = data["url"] if "url" in data else None
        self["date"] = data["datePublished"] if "datePublished" in data else None
        self["rating_press"] = (
            convert_float(data["aggregateRating"]["ratingValue"])
            if "aggregateRating" in data
            else -1
        )
        self["synopsis"] = (
            html.unescape(data["description"]) if "description" in data else None
        )
        self["director"] = (
            normalize(data["director"][0]["name"]).strip('"')
            if "director" in data
            else None
        )
        self["casting"] = (
            [normalize(a["name"]) for a in data["actor"]] if "actor" in data else []
        )

        lang = response.xpath(
            "//li[@data-testid='title-details-languages']/descendant::li/a/text()"
        ).extract()
        self["lang"] = [normalize(a) for a in lang] if len(lang) > 0 else []

        budget = response.xpath(
            "//li[@data-testid='title-boxoffice-budget']//ul//span/text()"
        ).get()

        self["budget"] = -1
        if budget is not None:
            budget = normalize(budget)
            budget = re.sub(r"\s?[a-z]+", "", budget)
            self["budget"] = convert_int(budget)

        distributor = response.xpath(
            "//li[@data-testid='title-details-companies']//ul//a/text()"
        ).extract()
        self["distributor"] = (
            [normalize(a) for a in distributor] if len(distributor) > 0 else []
        )

        award = response.xpath(
            "//li[@data-testid='award_information']//span/text()"
        ).get()

        self["award"] = 0
        if award is not None:
            match = re.search(r"^[0-9]+", award)
            self["award"] = convert_int(match[0]) if match is not None else 0

        yield self


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
