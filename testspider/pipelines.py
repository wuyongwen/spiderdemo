# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os

from testspider.items import ArticleItem, XiechengArticleItem


class Pipeline_ToCSV(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        fields_dick = {
            "xuerenmusic": ['标题', '正文', '作者', '链接'],
            "xiecheng": ['标题', '正文', '作者', '时间', '链接']
        }
        # csv文件的位置,无需事先创建
        file_path = "/spiders/{}.csv".format(spider.name)
        store_file = os.path.dirname(__file__) + file_path
        self.file = open(store_file, 'wb')
        # csv写法
        self.writer = csv.writer(self.file)
        fields = fields_dick.get(spider.name)
        self.writer.writerow(fields)

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.writer.writerow((item['title'], item['content'], item['author'], item['url_path']))
        if isinstance(item, XiechengArticleItem):
            self.writer.writerow((item.get('title'), item.get('content'), item.get('author'), item.get('time', ""),
                                  item.get('url_path')))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class TestspiderPipeline(object):
    def process_item(self, item, spider):
        return item
