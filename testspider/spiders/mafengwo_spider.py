# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import os

import scrapy
from scrapy.loader import ItemLoader

from testspider.items import MafengwoArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'mafengwo.log')

already_read = dict()

with open(logfile, 'a+') as logf:
    for i in logf.readlines():
        already_read.update({i.strip():None})


def get_urls():
    base_path = os.path.abspath(__file__)
    logfile = os.path.join(os.path.dirname(base_path), 'ext_path.log')

    urls = []

    with open(logfile, 'rw') as logf:
        for i in logf.readlines():
            urls.append(i.strip())
    return urls


class MafengwoSpider(scrapy.spiders.Spider):
    name = "mafengwo"
    start = 'http://www.mafengwo.cn/search/s.php?q=%E6%9C%9D%E9%B2%9C&p={p}&t=info&kt=1'
    """
    A列：时间，B列：题目，C列：全文
    """
    def start_requests(self):
        urls = [self.start.format(p=i) for i in range(1, 51)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.att-list ul li'):
            href = quote.css('div.ct-text ._j_search_link::attr(href)').extract_first()
            if href and href not in already_read:
                yield scrapy.Request(href, callback=self.get_content)
        # next_page = response.css('div.m-pagination .next::attr(data-page)').extract_first()
        # if next_page is not None:
        #     href = self.start.format(p=next_page)
        #     yield response.follow(href, self.parse)

    def get_content(self, response):
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')

        l = ItemLoader(item=MafengwoArticleItem(), response=response)
        if response.css('#pnl_contentinfo'):  # 样式1
            l.add_css('title', 'div.post_title h1::text')
            value = u""
            for node in response.css('#pnl_contentinfo ._j_note_content *'):
                value += node.xpath("string()").extract_first() + "\n"
            l.add_value('content', value)
            # l.add_css('content', '#pnl_contentinfo ._j_note_content *::text')
            l.add_css('author', 'div.tools a::text')
            l.add_css('time', 'div.tools .date::text')
            l.add_value('url_path', response.url)
        else:  # 样式2
            l.add_css('title', 'div.view_info h1::text')
            value = u""
            for node in response.css('div._j_content_box div,p'):
                value += node.xpath("string()").extract_first() + "\n"
            l.add_value('content', value)
            # l.add_css('content', 'div.vc_article ._j_seqitem ::text')
            l.add_css('author', 'meta[name=author]::attr(content)')
            l.add_css('time', 'div.travel_directory .time::text')
            l.add_value('url_path', response.url)
        return l.load_item()


if __name__ == "__main__":
    pass
