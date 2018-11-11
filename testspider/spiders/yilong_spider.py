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
logfile = os.path.join(os.path.dirname(base_path), 'yilong.log')

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


class YilongSpider(scrapy.spiders.Spider):
    name = "yilong"
    """
    A列：时间，B列：题目，C列：全文
    """
    base_url = 'http://strip.elong.com/solr/index.html?req=%s'
    def start_requests(self):
        query = []
        for i in range(1, 48):
            q = {"kw": u"朝鲜", "type": 5, "pageindex": i, "pagenums": 20}
            query.append(q)
        urls = [
            self.base_url % ujson.dumps(i) for i in query
            # 'http://lvyou.elong.com/moxiaohe/tour/a9db17q7.html'
            # 'http://lvyou.elong.com/5204892/pictorial/a1i4pq76.html'
            # 'http://lvyou.elong.com/5113393/tour/a9dcp4v6.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonBody = ujson.loads(response.body.encode('utf-8'))
        if 'data' in jsonBody:
            for data in jsonBody["data"]:
                yield scrapy.Request(data["identifier"], callback=self.get_content)

    def get_content(self, response):
        l = ItemLoader(item=YilongArticleItem(), response=response)
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


if __name__ == "__main__":
    pass
