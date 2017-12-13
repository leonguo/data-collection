# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CodeItem(scrapy.Item):
    # define the fields for your item here like:
    sec_code = scrapy.Field()
    sec_name = scrapy.Field()
    # pass

class FilmOfficeItem(scrapy.Item):
    # define the fields for your item here like:
    film_name = scrapy.Field()
    film_box_office = scrapy.Field()
    film_box_office_img = scrapy.Field()
    film_year = scrapy.Field()