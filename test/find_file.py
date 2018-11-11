# !/usr/bin/env python
# -*- coding:utf-8 -*-
import re

error_path = []


def load_file(file):
    pix = r'Spider error processing <GET (.+?)>'
    with open(file, 'r') as file:
        for line in file.readlines():
            error_path.extend(re.findall(pix, line))


def main():
    load_file("nohup.out")
    if error_path:
        with open('error.log', 'a+') as logfile:
            for i in error_path:
                logfile.write(i+'\n')


if __name__ == '__main__':
    main()
