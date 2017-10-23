# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DzdpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    comment = scrapy.Field()
    cpp = scrapy.Field()  # 人均消费
    score = scrapy.Field()
    envir = scrapy.Field()
    cjmc = scrapy.Field()
    city = scrapy.Field()
    href = scrapy.Field()
    pass
