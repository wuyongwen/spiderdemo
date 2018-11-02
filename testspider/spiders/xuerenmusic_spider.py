# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import scrapy
from scrapy.loader import ItemLoader

from testspider.items import ArticleItem


class XuerenmusicSpider(scrapy.spiders.Spider):
    name = "xuerenmusic"

    def start_requests(self):
        urls = [
            'https://www.xuerenmusic.com/page/1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//article'):
            if quote.xpath("./h2/a"):
                href = quote.css('h2 a::attr(href)').extract_first()
                yield scrapy.Request(href, callback=self.get_content)
        next_page = response.css('li.next-page a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_css('title', 'h1.article-title a::text')
        l.add_css('content', 'article.article-content p::text')
        l.add_css('author', 'header.article-header .name_1::text')
        l.add_value('url_path', response.url)
        return l.load_item()
