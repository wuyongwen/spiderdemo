# !/usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import datetime

import ujson

import requests
from selenium import webdriver
import os, sys
import time

reload(sys)
sys.setdefaultencoding('utf8')
from selenium.common.exceptions import NoSuchElementException


def get_chrome_path():
    base_path = os.path.abspath(__file__)
    print base_path
    chrome_path = os.path.join(os.path.dirname(base_path), 'chromedriver')
    print chrome_path
    return chrome_path


links = []


def get_page_link(browser):
    att_list = browser.find_element_by_class_name("att-list")
    if att_list is not None:
        title_h3 = att_list.find_elements_by_tag_name("h3")
        for h3 in title_h3:
            title_a = h3.find_element_by_tag_name("a")
            if title_a:
                links.append(title_a.get_attribute("href"))


def has_next_page(browser):
    next_btn = None
    try:
        next_btn = browser.find_elements_by_css_selector("#_j_search_pagination .next")
        return next_btn[-1]
    except NoSuchElementException, e:
        print "no next page btn!"
    return next_btn


def get_browser(proxy=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_prefs = dict()
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')

    if proxy:
        print "使用代理：%s " % proxy
        chrome_options.add_argument("--proxy-server=http://{0}".format(proxy))
    browser = webdriver.Chrome(
        executable_path=get_chrome_path(),
        chrome_options=chrome_options
    )
    browser.set_page_load_timeout(10)
    browser.get("http://httpbin.org/ip")
    print("当前ip：%s" % browser.page_source)
    return browser


def crawl_main():
    browser = get_browser()
    browser.get("http://www.mafengwo.cn/search/s.php?q=%E6%9C%9D%E9%B2%9C&t=info&kt=1")
    browser.implicitly_wait(5)
    get_page_link(browser)
    next_btn = has_next_page(browser)
    while next_btn:
        try:
            time.sleep(5)
            print u"开始点击第：%s 页， 链接：%s" % (next_btn.get_attribute("data-page"), len(links))
            next_btn.click()
            browser.implicitly_wait(5)
            get_page_link(browser)
            next_btn = has_next_page(browser)
        except Exception, e:
            print e
            next_btn = None

    browser.quit()
    with open("mafengwo.txt", 'a+') as file:
        file.write("\n".join(links))


def get_links(filename, skip_count=0):
    _links = []
    with open(filename, 'r') as file:
        page_linkes = file.readlines()
        for index, i in enumerate(page_linkes):
            if index >= skip_count:
                _links.append(i.strip())
    return _links


class ExcelWriter(object):
    def __init__(self):
        file_path = "/{}_{}.csv".format("mafengwo", datetime.datetime.now().strftime("%Y%m%d"))
        store_file = os.path.dirname(__file__) + file_path
        self.file = open(store_file, 'a+')
        self.writer = csv.writer(self.file)

    def write(self, title, content, author, _time, url):
        self.writer.writerow((title, content, author, _time, url))

    def close(self):
        self.file.close()


excel_writer = ExcelWriter()


def get_proxy():
    proxys = set()
    url = "http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions="
    proxy_str = requests.get(url).content
    proxy = ujson.loads(proxy_str)
    for ip_port in proxy.get("data"):
        po = "%s:%s" % (ip_port.get('ip'), ip_port.get('port'))
        proxys.add(po)
    print "获取代理： %s" % proxys

    return proxys


def crawl_page():
    proxys = get_proxy()
    _links = get_links('mafengwo.txt', 694)
    proxy = proxys.pop()
    browser = get_browser(proxy)

    def get_el_by_class(b, class_name):
        try:
            el = b.find_element_by_class_name(class_name)
            return el
        except NoSuchElementException, e:
            return None

    def get_el_by_id(b, id):
        try:
            el = b.find_element_by_id(id)
            return el
        except NoSuchElementException, e:
            return None

    total = len(_links)
    index = 0
    while index < total:
        link = _links[index]
        print "爬虫： %s, URL: %s" % (index, link)
        browser.get(link)
        browser.implicitly_wait(2)
        time.sleep(2)
        main = get_el_by_class(browser, "main")
        post_main = get_el_by_class(browser, "post_main")
        if main or post_main:
            el = browser.find_element_by_tag_name("body")
            has_more = True
            c_height = el.size.get("height", 0)
            while has_more:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                _c_height = el.size.get("height", 0)
                if _c_height == c_height:
                    has_more = False
                else:
                    c_height = _c_height
        if main:
            _j_content_box = get_el_by_class(main, "_j_content_box")
            headtext = get_el_by_class(main, "headtext")
            per_name = get_el_by_class(main, "per_name")
            vc_time = get_el_by_class(main, 'time')
            content = _j_content_box.text if _j_content_box else u""
            author = per_name.text if per_name else u""
            _time = vc_time.text if vc_time else u""
            _title = headtext.text if headtext else u""
            excel_writer.write(_title, content, author, _time, link)
            index += 1
        elif post_main:
            pnl_contentinfo = get_el_by_id(post_main, "pnl_contentinfo")
            post_title = get_el_by_class(browser, 'post_title')
            name = get_el_by_class(post_main, 'name')
            date = get_el_by_class(post_main, 'date')
            content = pnl_contentinfo.text if pnl_contentinfo else u""
            title = post_title.text if post_title else u""
            _name = name.text if name.text else u""
            _date = date.text if date else u""
            excel_writer.write(title, content, _name, _date, link)
            index += 1
        else:
            browser.quit()
            print "无法处理爬虫： %s, URL: %s " % (index, link)
            if len(proxys) == 0:
                proxys = get_proxy()
            browser = get_browser(proxys.pop())

    browser.quit()
    excel_writer.close()


if __name__ == '__main__':
    print "开始"
    crawl_main()
    crawl_page()
