# -*- coding: utf-8 -*-

import scrapy
import json
import logging
import datetime


class IndexSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
        urls = [
            'http://www.cninfo.com.cn/cninfo-new/announcement/query',
        ]
        today = datetime.date.today()
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata={"seDate": "2017-12-01","tabName":"fulltext"})

    def parse(self, response):
        logger = logging.getLogger()
        logger.info("response: poster index page[%s] crawl status: %d", response.url, response.status)
        logger.info(unicode(response.body,"utf-8"))
        # jsonBody = json.loads(response.body)
        # print  json.dumps(jsonBody)
