# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def date_convert(value):
    try:
        value = re.sub(r'\s+', '', value)
        create_date = value[3:13]
    except Exception as e:
        create_date = ""
    return create_date


class ArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags),
                         output_processor=Join(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags),
                           output_processor=Join(), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags),
                          output_processor=Join(), )
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


class XiechengArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                         output_processor=Join(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                           output_processor=Join(), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                          output_processor=Join(), )
    time = scrapy.Field(input_processor=MapCompose(date_convert),
                        output_processor=TakeFirst())
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


class TestspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
