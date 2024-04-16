# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import html
import json
import re
from utils.string import convert_float, convert_int, normalize
from scrapy.item import Item, Field
import isodate
from timelength import TimeLength
from thefuzz import fuzz


class BaseImdbItem(Item):
    id = Field()
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
    genre = Field()
    genre_raw = Field()

    def parse(self, response):
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

        # if self["date"] is None:
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

        self["genre_raw"] = (
            [html.unescape(g) for g in data["genre"]] if "genre" in data else []
        )
        self["genre"] = [normalize(g) for g in self["genre_raw"]]

        yield self


class FilmImdbItem(BaseImdbItem):
    id_jp = Field()

    def parse(self, response):
        return super().parse(response)


class SortieImdbItem(BaseImdbItem):
    thumbnail = Field()
    copies = Field()
    score_pred = Field()
    duration = Field()

    def parse(self, response, date=None, thumbnail=""):
        data = response.xpath('//script[@type="application/ld+json"]/text()').extract()
        data = json.loads(data[0])

        duration = response.xpath(
            '//*[@data-testid="hero__pageTitle"]/following::ul/child::li[last()]/text()'
        ).get()
        duration = TimeLength(duration).to_seconds() if duration is not None else None

        if duration is None:
            duration = (
                isodate.parse_duration(data["duration"]).total_seconds()
                if "duration" in data
                else -1
            )

        self["date"] = date
        self["thumbnail"] = thumbnail
        self["duration"] = int(duration)

        return super().parse(response)


class CopiesFromAllocine(Item):
    copies = Field()

    def parse(self, response, films):
        path_title = "//div[contains(@class, 'gd-col-left')]//a[contains(@href, 'fichefilm') and contains(@class, 'meta-title-link')]/text()"
        all_title = response.xpath(f"{path_title}").extract()

        all = []
        for titre in all_title:
            titre = titre[: titre.index('"')] if '"' in titre else titre
            path = f'//a[contains(@class, "meta-title-link") and contains(@href, "fiche") and starts-with(text(), "{titre}")]'
            copies = response.xpath(
                f'{path}/parent::h2/parent::div/following-sibling::div/span/span[contains(text(), "Séance")]/text()'
            ).get()

            if copies is not None:
                match = re.search(r"([0-9]+)", copies)
                copies = convert_int(match[0]) if match is not None else -1
                all.append({"title": normalize(titre), "copies": copies})

        for film in films:
            item_sortie = SortieImdbItem()
            item_sortie["id"] = film.id
            item_sortie["copies"] = -1

            title = normalize(film.title)
            original_title = normalize(film.original_title)

            for item in all:
                if item["title"] == title or item["title"] == original_title:
                    item_sortie["copies"] = item["copies"]
                elif (
                    fuzz.ratio(
                        item["title"],
                        title,
                    )
                    > 60
                    or fuzz.ratio(
                        item["title"],
                        original_title,
                    )
                    > 60
                ):
                    item_sortie["copies"] = item["copies"]

            yield item_sortie if item_sortie["copies"] != -1 else None
