# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class CodePipeline(object):
    def __init__(self, psql_dsn):
        self.psql_dsn = psql_dsn

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            psql_dsn=crawler.settings.get('POSTGRESQL_DSN'),
        )

    def open_spider(self, spider):
        self.client = psycopg2.connect(self.psql_dsn)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print "ddd"
        return item
    #
    # def process_item(self, item, spider):
    #     return item
