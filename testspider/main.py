# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""

@author warden
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.cmdline import execute


def main():
    execute(['scrapy', 'crawl', 'quna'])


if __name__ == '__main__':
    main()
