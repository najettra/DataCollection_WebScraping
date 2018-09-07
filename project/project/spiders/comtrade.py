# -*- coding: utf-8 -*-
import scrapy


class ComtradeSpider(scrapy.Spider):
    name = 'comtrade'
    allowed_domains = ['https://comtrade.un.org/data']
    start_urls = ['https://comtrade.un.org/api/getmax=500&type=C&freq=A&px=HS&ps=2016,2015,2014,2013&r=788&p=all&rg=2&cc=85&uitoken=4c599ed9273b53b875f870451acdf719']

    def parse(self, response):
        pass
    
    
    
   
