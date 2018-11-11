# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import os
import urlparse

import scrapy
from scrapy.loader import ItemLoader

from testspider.items import QongyouArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'quna.log')

already_read = dict()

with open(logfile, 'r+') as logf:
    for i in logf.readlines():
        already_read.update({i.strip(): None})


class YilongSpider(scrapy.spiders.Spider):
    name = "quna"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_ulr = 'http://travel.qunar.com'

    def start_requests(self):
        urls = [
            'http://travel.qunar.com/search/gonglue/24-chaoxian-300555/hot_heat/1.htm'
            # 'http://travel.qunar.com/youji/5996140'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css('ul.b_strategy_list li'):
            _href = article.css("h2 a::attr(href)").extract_first()
            href = urlparse.urljoin(self.base_ulr, _href)
            if href and href not in already_read:
                yield scrapy.Request(href, callback=self.get_content)

        next_page = response.css('div.b_paging>.next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=QongyouArticleItem(), response=response)
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        l.add_css('title','#booktitle::text')
        # l.add_css('content', '#pagelet_main .master-posts-list li .content::text')
        value = u''
        for node in response.css('div.e_main .e_day p'):
            value += node.xpath("string()").extract_first() + "\n"
        l.add_value('content', value)
        l.add_css('author', 'div.e_line2 .head a::text')
        l.add_css('time', '#js_mainleft .data::text')
        l.add_value('url_path', response.url)
        return l.load_item()

if __name__ == "__main__":
    pass
