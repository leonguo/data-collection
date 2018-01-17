# -*- coding: utf-8 -*

# images 抓取

import scrapy
import json
from datetime import date, datetime
import sys
# from ..items import FilmOfficeItem
# from scrapy.loader import ItemLoader

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageSpider(scrapy.Spider):
    name = "image"
    page = 0
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'cninfo.pipelines.FilmPipeline': 300,
    #     }
    # }

    start_urls = ['https://www.pinterest.com/login']
    # 先登录网站
    def parse(self, response):
        return scrapy.FormRequest.from_response(response, callback=self.after_login, method="POST",
                                                formdata={"id": "hotman8168@gmail.com", "password": "hotman8168com"})

    def after_login(self, response):
        self.logger.warning("response: poster index page[%s] crawl status: %d", response.url, response.status)
        yield scrapy.Request(url="https://www.pinterest.com",
                             callback=self.action)

    def action(self, response):
        self.logger.warning("response: image page url [%s] crawl status: %d", response.url, response.status)
        if response.status == 200:
            print response.content
