# -*- coding: utf-8 -*


# http://58921.com 票房统计数据

import scrapy
import json
from datetime import date, datetime
import sys
from ..items import FilmOfficeItem
from scrapy.loader import ItemLoader

reload(sys)
sys.setdefaultencoding('utf-8')


class FilmSpider(scrapy.Spider):
    name = "film"
    page = 0
    custom_settings = {
        'ITEM_PIPELINES': {
            'cninfo.pipelines.FilmPipeline': 300,
        }
    }

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
            film_table = response.xpath('//table/tbody/tr')
            if len(film_table) > 1:
                for film in film_table:
                    l = ItemLoader(item=FilmOfficeItem(), selector=film)
                    l.default_output_processor = scrapy.loader.processors.TakeFirst()
                    l.add_xpath('film_name', 'td[3]/a/text()')
                    l.add_xpath('film_box_office_img', 'td[4]/img/@src')
                    l.add_xpath('film_year', 'td[7]/text()')
                    yield l.load_item()
                    
                if self.page <= 30:
                    self.page += 1
                    next_page_url = "http://58921.com/alltime/2017?page={0}".format(
                        self.page)
                    self.logger.warning("crawl page url :: [%s] ", next_page_url)
                    yield scrapy.Request(url=next_page_url, callback=self.action)
