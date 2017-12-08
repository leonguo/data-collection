# -*- coding: utf-8 -*-

import scrapy
import json
import math
from datetime import date, datetime

from ..items import CodeItem
from scrapy.loader import ItemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


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
        code_table = response.xpath('//table[@class="table_data"]/tr')
        for code in code_table:
            l = ItemLoader(item=CodeItem(), selector=code)
            l.default_output_processor = scrapy.loader.processors.TakeFirst()
            l.add_xpath('sec_code', 'td[1]/nobr/a/text()')
            l.add_xpath('sec_name', 'td[2]/nobr/a/text()')
            yield l.load_item()
