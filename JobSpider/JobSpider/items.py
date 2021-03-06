# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()    # 职位名称
    company = scrapy.Field()
    location = scrapy.Field()    # 地点
    salary = scrapy.Field()
    description = scrapy.Field()    # 职位描述
    requirement = scrapy.Field()    # 职位要求

