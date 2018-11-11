# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import os

import scrapy
import ujson
from scrapy.loader import ItemLoader

from testspider.items import YilongArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'tongcheng.log')

already_read = dict()

with open(logfile, 'a+') as logf:
    for i in logf.readlines():
        already_read.update({i.strip():None})


class YilongSpider(scrapy.spiders.Spider):
    name = "tongcheng"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_url = 'https://www.ly.com/travels/%s.html'
    def start_requests(self):
        urls = [
            'https://www.ly.com/travels/travel/getSearchYouJiList?k=%E6%9C%9D%E9%B2%9C&pindex=1&psize=100&rt=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonBody = ujson.loads(response.body.encode('utf-8'))
        if 'youJiList' in jsonBody:
            for data in jsonBody["youJiList"]:
                yield scrapy.Request(self.base_url % data["travelNoteId"], callback=self.get_content)

    def get_content(self, response):
        l = ItemLoader(item=YilongArticleItem(), response=response)
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        l.add_css('title', 'div.titlemid  h1 em::text')
        l.add_css('content', 'div.contentall .content p::text')
        l.add_css('author', '#head > div.bottomdiv > div > div.headLeftBox > div.headname > a::text')
        l.add_css('time', '#head > div.bottomdiv > div > div.headLeftBox > div.headmid > span.createTime > em::text')
        l.add_value('url_path', response.url)

        return l.load_item()


if __name__ == "__main__":
    pass
