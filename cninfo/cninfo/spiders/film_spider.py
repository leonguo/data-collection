# -*- coding: utf-8 -*


# http://58921.com 票房统计数据

import scrapy
import json
import logging
import psycopg2
import math
from datetime import date, datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FilmSpider(scrapy.Spider):
    name = "film"
    page = 1

    def start_requests(self):
        login_url = "http://58921.com/user/login"
        yield scrapy.FormRequest(url=login_url, callback=self.after_login, method = "POST",
                                  formdata={"mail": "469624718@qq.com", "pass": "123456"})

    def after_login(self, response):
        self.logger.warning("response: poster index page[%s] crawl status: %d", response.url, response.status)
        yield scrapy.Request(url="http://58921.com/alltime/2017?page=3",
                      callback=self.action)

    def action(self, response):
        self.logger.warning("response: poster index page[%s] crawl status: %d", response.url, response.status)
        self.logger.warning(response.body)