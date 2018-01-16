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

    start_urls = ['http://58921.com/user/login']

    # http://58921.com/user/login/ajax?ajax=submit&__q=user/login
    # mail:469624718 @ qq.com
    # pass:123456
    # form_id:user_login_form
    # form_token:c58a2194ff6c2db654c3dbf82be32459
    # submit:登录
    def parse(self, response):
        return scrapy.FormRequest.from_response(response, callback=self.after_login, method="POST",
                                                formdata={"mail": "469624718@qq.com", "pass": "123456"})

    def after_login(self, response):
        self.logger.warning("response: poster index page[%s] crawl status: %d", response.url, response.status)
        yield scrapy.Request(url="http://58921.com/alltime/2017",
                             callback=self.action)

    def action(self, response):
        self.logger.warning("response: film page url [%s] crawl status: %d", response.url, response.status)
        if response.status == 200:
            print 'dd'
