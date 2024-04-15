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
        if self["date"] is None:
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


class FilmImdbItem(BaseImdbItem):
    id_jp = Field()

    def parse(self, response):
        return super().parse(response)


class SortieImdbItem(BaseImdbItem):
    thumbnail = Field()
    copies = Field()
    score_pred = Field()
    genre = Field()
    duration = Field()

    def parse(self, response, date=None, thumbnail=""):
        self["date"] = date
        self["thumbnail"] = thumbnail
        self["genre"] = ""
        self["duration"] = 0

        return super().parse(response)


class CopiesFromAllocine(Item):
    copies = Field()

    def parse(
        self,
        response,
        id=None,
        title="",
        original_title="",
        date=None,
        director="",
    ):
        item = SortieImdbItem()
        item["id"] = id

        path = "//div[contains(@class, 'gd-col-left')]//a[contains(@href, 'fichefilm') and contains(@class, 'meta-title-link')]/text()"

        all_links = response.xpath(f"{path}").extract()
        print(date, all_links)

        # path = f'//a[contains(@class, "meta-title-link") and contains(@href, "fiche") and contains(text(), "{title}")]'
        # has_title = response.xpath(f"{path}/text()").get()
        # print(date, title, has_title)
        # if has_title is not None:
        #     copies = response.xpath(
        #         f'{path}/parent::h2/parent::div/following-sibling::div/span/span[contains(text(), "Séance")]/text()'
        #     ).get()

        #     if copies is not None:
        #         match = re.search(r"([0-9]+)", copies)
        #         item["copies"] = convert_int(match[0]) if match is not None else -1

        #         yield item

        yield None


# @._V1_QL75_UY74_CR1,0,50,74_.jpg
