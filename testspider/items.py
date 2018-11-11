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
        if len(value) > 13:
            create_date = value[3:13]
        else:
            create_date = value
    except Exception as e:
        create_date = ""
    return create_date


def replace_p2enter(value):
    try:
        p = re.compile('<?p>', re.I)
        p.sub(value, '\n')
    except Exception, e:
        pass
    return value


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


class MafengwoArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                         output_processor=Join(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                           output_processor=Join(), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                          output_processor=Join(), )
    time = scrapy.Field(input_processor=MapCompose(),
                        output_processor=TakeFirst())
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


class YilongArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                         output_processor=Join(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                           output_processor=Join('\n'), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                          output_processor=Join(), )
    time = scrapy.Field(input_processor=MapCompose(),
                        output_processor=TakeFirst())
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


class QongyouArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                         output_processor=TakeFirst(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                           output_processor=Join('\n'), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                          output_processor=Join(), )
    time = scrapy.Field(input_processor=MapCompose(),
                        output_processor=TakeFirst())
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


def baidu_date(value):
    reg = r"(\d{4}-\d{1,2}-\d{1,2})"
    g = re.findall(reg, value)
    return "-".join(g)

class BaiduArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                         output_processor=Join(), )
    content = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                           output_processor=Join('\n'), )
    author = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip),
                          output_processor=Join(), )
    time = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip, baidu_date),
                        output_processor=TakeFirst())
    url_path = scrapy.Field(input_processor=MapCompose(remove_tags),
                            output_processor=TakeFirst(), )


class TestspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
