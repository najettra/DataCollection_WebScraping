# -*- coding: utf-8 -*-
import re
import time
import pandas as pd
import scrapy
from project.items import ProjectItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from elasticsearch import Elasticsearch

class ProductTradeSpider(scrapy.Spider):
    name = 'product_trade'
    allowed_domains = ['www.trademap.org']
    start_urls = ['https://www.trademap.org/Product_SelCountry_TS.aspx?nvpm=1|788||||TOTAL|||2|1|1|2|2|1|1|1|1']
    elastic_connection = Elasticsearch(['http://localhost:9200'])
    counter = 0
    
    def parse(self, response):
        
        
        driver = webdriver.Firefox()
        driver.get(response.url)
        driver.switch_to_active_element
        product_list = driver.find_elements_by_xpath("//table[@id='ctl00_PageContent_MyGridView1']//tr[position() > 2]")
        driver.switch_to_active_element
        target = driver.find_elements_by_xpath('//span[@id="ctl00_Label_Title"]')
        reporters = re.findall(r'exported by ([\w\s]+)',target[0].text)[0]
        header = driver.find_elements_by_xpath('//table[@id="ctl00_PageContent_MyGridView1"]')
        
        for m in range(len(header)):
            print(header[m].text)
        for co in product_list[:-1]:
            driver.switch_to_active_element
            line=' '.join(co.text.split(' ')[1:])
            products=re.findall(r'[\D,\s.\'()_-]*',line)[0].strip()
            vals=line[len(products)+1:].split()
            for i in range(len(vals)):
                
                item = {}
                item['partners'] = "All"
                item['reporters'] = reporters
                item['products'] = products
                driver.switch_to_active_element
                item['trade_value'] = int((vals[i]+'000').replace(',',''))
                driver.switch_to_active_element
                item['years'] = (header[i+4]).text.split()[-1]
                yield item
    
    
    
        links = list(set(response.xpath("//a[contains(@href,'Page$')]//text()").extract()))
        driver.switch_to_active_element
        for link in links:
            next_page = driver.find_element_by_link_text(link)
            next_page.click()
            driver.switch_to_active_element
            
            product_list = driver.find_elements_by_xpath("//table[@id='ctl00_PageContent_MyGridView1']//tr[position() > 2]")
            target = driver.find_elements_by_xpath('//span[@id="ctl00_Label_Title"]')
            reporters = re.findall(r'exported by ([\w\s]+)',target[0].text)[0]
            header = driver.find_elements_by_xpath('//table[@id="ctl00_PageContent_MyGridView1"]//th[@scope="col"]')
            for co in product_list[:-1]:
                line=' '.join(co.text.split(' ')[1:])
                products=re.findall(r'[\D,\s.\'()_-]*',line)[0].strip()
                vals=line[len(products)+1:].split()
                for i in range(len(vals)):
                    item = {}
                    item['partners'] = "All"
                    item['reporters'] = reporters
                    item['products'] = products
                    driver.switch_to_active_element
                    item['trade_value'] = int((vals[i]+'000').replace(',',''))
                    driver.switch_to_active_element
                    item['years'] = (header[i+4]).text.split()[-1]
                    yield item
                
         
        
        #driver.close()
                    
                    
      
