# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""
import urlparse

import scrapy
from scrapy.loader import ItemLoader

from testspider.items import XiechengArticleItem


class XiechengSpider(scrapy.spiders.Spider):
    name = "xiecheng"
    """
    A列：时间，B列：题目，C列：全文
    """
    def start_requests(self):
        urls = [
            'http://you.ctrip.com/searchsite/travels/?query=%E6%9C%9D%E9%B2%9C&isAnswered=&isRecommended=&publishDate=&PageNo=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('ul.youji-ul li'):
            if quote.xpath("./dl/dt/a"):
                href = quote.css('dl dt a::attr(href)').extract_first()
                href = urlparse.urljoin("http://you.ctrip.com", href)
                yield scrapy.Request(href, callback=self.get_content)
        next_page = response.css('a.left_arrow::attr(href)').extract()[-1]
        if next_page is not None:
            href = urlparse.urljoin("http://you.ctrip.com", next_page)
            yield response.follow(href, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=XiechengArticleItem(), response=response)
        l.add_css('title', 'div.ctd_head_left h2::text')
        l.add_css('content', 'div.ctd_content p::text')
        l.add_css('author', 'a#authorDisplayName::text')
        l.add_css('time', 'div.ctd_content>h3::text')
        l.add_value('url_path', response.url)
        return l.load_item()


if __name__ == "__main__":
    pass
