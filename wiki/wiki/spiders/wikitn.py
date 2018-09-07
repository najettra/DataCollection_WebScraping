# -*- coding: utf-8 -*-
import scrapy


class WikitnSpider(scrapy.Spider):
    name = 'wikitn'
    allowed_domains = ['https://www.wiki.tn/pc-portable/laptop-versus-vbook-7225.html']
    start_urls = ['http://https://www.wiki.tn/pc-portable/laptop-versus-vbook-7225.html/']

    def parse(self, response):
        name = response.xpath('//h1[@itemprop="name"]/text()').extract()
        print(name)

