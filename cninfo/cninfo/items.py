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
    cb_box_office = scrapy.Field()
    film_eng_name = scrapy.Field()
    film_area = scrapy.Field()

class AnnouncementItem(scrapy.Item):
    # define the fields for your item here like:
    announcement_id = scrapy.Field()
    announcement_title = scrapy.Field()
    announcement_time = scrapy.Field()
    adjunct_url = scrapy.Field()
    adjunct_size = scrapy.Field()
    adjunct_type = scrapy.Field()
    sec_code = scrapy.Field()
    sec_name = scrapy.Field()
    org_id = scrapy.Field()