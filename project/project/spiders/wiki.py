# -*- coding: utf-8 -*-
import scrapy


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['https://www.wiki.tn/pc-portable-120.html']
    start_urls = ['https://www.wiki.tn/pc-portable-120.html']
    #start_urls = ['https://www.wiki.tn/pc-portable/pc-portable-vegabook-10-quad-core-2go-32-go-gold-white-8524.html']

    def parse(self, response):
        #name = response.xpath('//h1[@itemprop="name"]/text()').extract()
        #marque = response.xpath('//span[@class="marque"]/img/@title').extract()
        #ref = response.xpath('//p[@id="product_reference"]').extract()
        #price = response.xpath('//span[@id="our_price_display"]/@data-price').extract()
        #print(name,marque)
        #print(float(price[0]))
        
        #products = response.xpath("//div[contains(@class,'ajax_bloc')]")
        #for product in products:
            #link = product.xpath(".//").extract()
            #price = 
            #yield scrapy.Request(link, self.parse_item, meta=['price':price])
        
        #next_page = 
        #if next_page:
            #yield scrapy.Request(url, self.parse)
        pass    
        
        
    #def parse_item(self, response):
        #price = response.meta['price']
        #title = 
            
            
         
    
