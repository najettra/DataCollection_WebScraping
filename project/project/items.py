# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    partners = scrapy.Field()
    reporters = scrapy.Field()
    products = scrapy.Field()
    #trade = scrapy.Field()
    trade_value = scrapy.Field()
    years = scrapy.Field()
    #code = scrapy.Field()
                    
                    