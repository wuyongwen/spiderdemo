# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import os
import urlparse

import scrapy
import ujson
from scrapy.loader import ItemLoader

from testspider.items import YilongArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'xinxin.log')

already_read = dict()

with open(logfile, 'r+') as logf:
    for i in logf.readlines():
        already_read.update({i.strip():None})


class YilongSpider(scrapy.spiders.Spider):
    name = "xinxin"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_ulr = 'https://abroad.cncn.com'
    def start_requests(self):
        urls = [
            'https://abroad.cncn.com/chaoxian/gonglue'
            # 'https://abroad.cncn.com/article/71333/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css('div.arctle ul li'):
            _href = article.css("a.title::attr(href)").extract_first()
            href = urlparse.urljoin(self.base_ulr, _href)
            if href and href not in already_read:
                yield scrapy.Request(href, callback=self.get_content)

        next_page = response.css('div.cutpage>.next a::attr(href)').extract_first()
        if next_page:
            next = urlparse.urljoin(self.base_ulr, next_page)
            yield response.follow(next, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=YilongArticleItem(), response=response)
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        l.add_css('title', 'div.infoShow>h1::text')
        l.add_css('content', 'div.infoCon *::text')
        l.add_css('author', 'body > div.warpper > div.sideR > div.infoShow > p > span::text')
        l.add_css('time', 'body > div.warpper > div.sideR > div.infoShow > p > a::text')
        l.add_value('url_path', response.url)

        return l.load_item()


if __name__ == "__main__":
    pass
