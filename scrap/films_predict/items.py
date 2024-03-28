# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from utils.string import normalize
from scrapy.item import Item, Field
import isodate
from timelength import TimeLength


class FilmItem(Item):
    id = Field()
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

        hebdo_rank = -1
        copies = -1

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
        self["year"] = normalize(block_year_duration[0])
        self["duration"] = TimeLength(block_year_duration[1]).to_seconds()
        self["country"] = block_country_genre[0]
        self["genre"] = block_country_genre[1]
        self["first_day"] = normalize(first_day).replace(" ", "") * 1
        self["first_weekend"] = normalize(first_weekend).replace(" ", "") * 1
        self["first_week"] = normalize(first_week).replace(" ", "") * 1
        self["hebdo_rank"] = hebdo_rank * 1
        self["copies"] = copies * 1

        print("parse", self)

        yield self
