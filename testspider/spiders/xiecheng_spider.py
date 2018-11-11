# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""
import urlparse

import os
import scrapy
from scrapy.loader import ItemLoader

from testspider.items import XiechengArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'xiecheng.log')

already_read = dict()

with open(logfile, 'rw') as logf:
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
                if href not in already_read:
                    with open(logfile, 'a+') as logf:
                        logf.write(href + '\n')
                    yield scrapy.Request(href, callback=self.get_content)
        next_page = response.css('a.left_arrow::attr(href)').extract()[-1]
        if next_page is not None:
            href = urlparse.urljoin("http://you.ctrip.com", next_page)
            yield response.follow(href, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=XiechengArticleItem(), response=response)
        if response.css('div.ctd_main_box'):  # 样式1
            l.add_css('title', 'div.ctd_head_con .title1::text')
            value = u""
            for node in response.xpath('//div[@class="ctd_content"]//p'):
                value += node.xpath('string()').extract_first() + "\n"
            l.add_value('content', value)
            #l.add_css('content', 'div.ctd_content *::text')
            l.add_css('author', 'a#authorDisplayName::text')
            l.add_css('time', 'div.ctd_head_con .time::text')
            l.add_value('url_path', response.url)
        else:  # 样式2
            l.add_css('title', 'div.ctd_head_left h2::text')
            value = u""
            for node in response.css('div.ctd_content p'):
                value += node.xpath("string()").extract_first() + "\n"
            l.add_value('content', value)
            # l.add_css('content', 'div.ctd_content::text')
            # for node in response.xpath('//div[@class="ctd_content"]'):
            #     value += node.xpath('string(.)').extract_first() + '\n'
            # l.add_value('content', value)
            l.add_css('author', 'a#authorDisplayName::text')
            l.add_css('time', 'div.ctd_content>h3::text')
            l.add_value('url_path', response.url)
        return l.load_item()


if __name__ == "__main__":
    pass
