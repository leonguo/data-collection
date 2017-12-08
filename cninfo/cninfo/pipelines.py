# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import logging


class CodePipeline(object):
    def __init__(self, psql_dsn):
        self.psql_dsn = psql_dsn
        self.logger = logging.getLogger()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            psql_dsn=crawler.settings.get('POSTGRESQL_DSN'),
        )

    def open_spider(self, spider):
        self.client = psycopg2.connect(self.psql_dsn)
        self.cur = self.client.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()

    def process_item(self, item, spider):
        self.logger.warning(item)
        if item.get("sec_code"):
            sec_code = item["sec_code"]
            sec_name = item["sec_name"]
            insert_q = "INSERT INTO share_certificate(sec_code,sec_name) VALUES ('{0}','{1}') ON CONFLICT DO NOTHING;".format(
                sec_code, sec_name)
            # self.logger.warning(unicode(insert_q, "utf-8"))
            try:
                self.cur.execute(insert_q)
            except psycopg2.Error:
                self.logger.exception('Database error')
            self.client.commit()
        return item
        #
        # def process_item(self, item, spider):
        #     return item
