# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""

import os

import scrapy
import ujson
from scrapy.loader import ItemLoader

from testspider.items import YilongArticleItem, BaiduArticleItem

base_path = os.path.abspath(__file__)
logfile = os.path.join(os.path.dirname(base_path), 'baidu.log')

already_read = dict()

with open(logfile, 'a+r') as logf:
    for i in logf.readlines():
        already_read.update({i.strip():None})


class BaiduSpider(scrapy.spiders.Spider):
    name = "baidu"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_url = u'https://lvyou.baidu.com/search/ajax/search?format=ajax&word=朝鲜&pn=%s&surl=chaoxian&rn=10'
    def start_requests(self):
        urls = [
            self.base_url % "0"
            # 'https://lvyou.baidu.com/notes/90a5a03452374ac89ab433a3'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonBody = ujson.loads(response.body.encode('utf-8'))
        if 'data' in jsonBody:
            if 'search_res' in jsonBody["data"]:
                if 'notes_list' in jsonBody['data']['search_res']:
                    for data in jsonBody['data']['search_res']['notes_list']:
                        if data['loc'] and data['loc'] not in already_read:
                            yield scrapy.Request(data['loc'], callback=self.get_content)
                page = jsonBody["data"]["search_res"]["page"]
                next_pn = page.get("pn", 0) + 10
                if page.get('total', 0) > next_pn:
                    next_page = self.base_url % next_pn
                    yield response.follow(next_page, self.parse)

    def get_content(self, response):
        l = ItemLoader(item=BaiduArticleItem(), response=response)
        with open(logfile, 'a+') as logf:
            logf.write(response.url + '\n')
        l.add_css('title', '#J-notes-view-header > div.main-center.clearfix > div.note-header-main > div.notes-hd > h1 > strong::text')
        # l.add_css('content', '#pagelet_main .master-posts-list li .content::text')
        value = u''
        for node in response.css('#pagelet_main .master-posts-list li .content p'):
            value += node.xpath("string()").extract_first() + "\n"
        l.add_value('content', value)
        l.add_css('author', '#J-notes-view-header > div.main-center.clearfix > div.note-header-main > div.user-info-container > p > a.uname::text')
        l.add_css('time', 'span.time::text')
        l.add_value('url_path', response.url)

        return l.load_item()


if __name__ == "__main__":
    pass
