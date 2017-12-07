# -*- coding: utf-8 -*-

import scrapy
import json
import math
from datetime import date, datetime

from ..items import CodeItem
from scrapy.loader import ItemLoader

class CodeSpider(scrapy.Spider):
    name = "code"

    custom_settings = {
        'ITEM_PIPELINES': {
            'cninfo.pipelines.CodePipeline': 300,
        }
    }

    # allowed_domains = [""]
    start_urls = [
        "http://quote.cfi.cn/quotelist.aspx?sortcol=zdf&sortway=desc&sectypeid=1&cfidata=1",
    ]

    def parse(self, response):
        self.logger.warning("response: poster index page[%s] crawl status: %d", response.url, response.status)
        l = ItemLoader(item=CodeItem(), response=response)
        l.add_xpath('name', '//div[@class="product_name"]')
        l.add_xpath('name', '//div[@class="product_title"]')
        l.add_xpath('price', '//p[@id="price"]')
        # code_item['sec_code'] = 1000
        # code_item['sec_name'] = "ddd"
        return l.load_item()
