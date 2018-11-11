# !/usr/bin/env python
# -*- coding:utf-8 -*-

# http://search.qyer.com/bbs?wd=%E6%9C%9D%E9%B2%9C&time_mode=1&time_interval_start=&time_interval_end=&fid=0&type=1&order=1&page=1
import urlparse

import scrapy
import os

from scrapy.loader import ItemLoader

from testspider.items import QongyouArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'qiongyou.log')

already_read = dict()

with open(logfile, 'a+') as logf:
    for i in logf.readlines():
        already_read.update({i.strip():None})


class QiongyouSpider(scrapy.spiders.Spider):

    name = "qiongyou"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_url = 'http://strip.elong.com/solr/index.html?req=%s'
    def start_requests(self):
        urls = [
            'http://search.qyer.com/bbs?wd=%E6%9C%9D%E9%B2%9C&time_mode=1&time_interval_start=&time_interval_end=&fid=0&type=1&order=1&page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.shResultGlobalList2 li'):
            href = quote.css('h2.title a::attr(href)').extract_first()
            if href and href not in already_read:
                yield scrapy.Request(href, callback=self.get_content)
        next_page = response.css('div.ui_page .ui_page_next::attr(href)').extract_first()
        if next_page is not None:
            href = urlparse.urljoin("http://search.qyer.com", next_page)
            yield response.follow(href, self.parse)

    def get_content(self, response):
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        l = ItemLoader(item=QongyouArticleItem(), response=response)
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        if response.css('div.article_center'):  # article_center
            l.add_css('title', 'div.ty_center .ty_left_header h1::text')
            # value = u""
            # for node in response.xpath('//div[@class="ctd_content"]//p'):
            #     value += node.xpath('string()').extract_first() + "\n"
            # l.add_value('content', value)
            l.add_css('content', 'div.article_center p::text')
            l.add_css('author', 'div.nickname b::text')
            l.add_css('time', 'div.act_header .act_date::text')
            l.add_value('url_path', response.url)
        else:  # photo_center
            l.add_css('title', 'div.ty_center .ty_left_header h1 a::text')
            # value = u""
            # for node in response.css('div.ctd_content p'):
            #     value += node.xpath("string()").extract_first() + "\n"
            # l.add_value('content', value)
            l.add_css('content', 'div.photo_center p::text')
            l.add_css('author', 'div.nickname b::text')
            l.add_css('time', 'div.act_header .act_date::text')
            l.add_value('url_path', response.url)
        return l.load_item()
