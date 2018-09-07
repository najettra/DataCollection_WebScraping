# -*- coding: utf-8 -*-
import re
import scrapy
import time
from datetime import datetime
from project.items import ProjectItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from elasticsearch import Elasticsearch

class TrademapSpider(scrapy.Spider):
    name = 'trademap'
    allowed_domains = ['www.trademap.org']
    start_urls = ['https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|376||||TOTAL|||2|1|1|2|2|1|2|1|1']
    #start_urls = ['https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|643||||27|||2|1|1|2|2|1|2|1|1', 'https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|788||||85|||2|1|1|2|2|1|2|1|1', 'https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|504||||85|||2|1|1|2|2|1|2|1|1', 'https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|620||||85|||2|1|1|2|2|1|2|1|1','https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|788||||62|||2|1|1|2|2|1|2|1|1','https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|504||||62|||2|1|1|2|2|1|2|1|1', 'https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|792||||62|||2|1|1|2|2|1|2|1|1','https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1|818||||62|||2|1|1|2|2|1|2|1|1' ]
    
    elastic_connection = Elasticsearch(['http://localhost:9200'])
    counter = 0
    def parse(self, response):
        product = response.xpath('//span[@id="ctl00_Label_SubTitle"]/text()').extract()
        #reporters = "Tunisia"
        trade = "Export"
        products = product[0].split(":")[1]
        header = response.xpath('//table[@id="ctl00_PageContent_MyGridView1"]//th[@scope="col"]//text()').extract()
        target = response.xpath('//span[@id="ctl00_Label_Title"]/text()').extract_first()
        reporters = re.findall(r'exported by ([\w\s]+)',target)
        
        #print(reporters)
        rows = response.xpath('//table[contains(@id,"ctl00_PageContent")]//tr[position()>2]')
        for r in rows:
            partners = r.xpath(".//a/text()").extract()
            values = r.xpath(".//td[position()>2 ]//text()").extract()
            if len(values) >= 1 and len(header) == len(values)+2:
                for i in range(len(values)):
                    item = {}
                    item['partners'] = partners[0]
                    item['reporters'] = reporters[0]
                    item['products'] = ' '.join((products.split(',')[0]).split()[1:])
                    #item['trade'] = trade
                    item['trade_value'] = int((values[i]+'000').replace(',',''))
                    item['years'] = header[i+2].split()[-1]
                    item['retailers'] = "trademap"
                    yield item
                    dt = time.time()
                    doc_id = "%s-%s-%s"%('trademap.org',dt,self.counter)
                    self.elastic_connection.index(index='trade',doc_type='export',id= doc_id, body=item)
                    self.counter +=1
                    
        links = list(set(response.xpath("//a[contains(@href,'Page$')]//text()").extract()))
        driver = webdriver.Firefox()
        driver.get(response.url)
        
        for link in links:
            next_page = driver.find_element_by_link_text(link)
            next_page.click()
            driver.switch_to_active_element
            partners = driver.find_elements_by_xpath('//table[contains(@id,"ctl00_PageContent")]//tr[position()>2 and position() != last()]//a')
            elements = driver.find_elements_by_xpath('//table[contains(@id,"ctl00_PageContent")]//tr[position()>2]/td[position()>2]')
            values = elements[3:-1]
            k=0
            #print(len(partners),len(elements))
            for p in range(len(partners)):
                #print(partners[p].text)
                for n in range(5):
                    item = {}
                    item['partners'] = partners[p].text
                    item['reporters'] = reporters[0]
                    item['products'] = ' '.join((products.split(',')[0]).split()[1:])
                    #item['trade'] = trade
                    item['trade_value'] = int((elements[k+n].text+'000').replace(',',''))
                    item['years'] = header[n+2].split()[-1]
                    item['retailers'] = "trademap"
                    yield item
                    dt = time.time()
                    doc_id = "%s-%s-%s"%('trademap.org',dt,self.counter)
                    self.elastic_connection.index(index='trade',doc_type='export', id=doc_id, body=item)
                    self.counter +=1
                k+=5
         
        
        #driver.close()
                    
                    
      