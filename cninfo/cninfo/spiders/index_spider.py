# -*- coding: utf-8 -*-

import scrapy
import json
import logging
import psycopg2
import math
from datetime import date, datetime


class IndexSpider(scrapy.Spider):
    name = "index"
    page = 1

    def get_request_body(self, num):
        today = datetime.today()
        return {"seDate": today.strftime('%Y-%m-%d'), "tabName": "fulltext",
                "sortName": "time",
                "sortType": "desc", "column": "szse", "pageNum": str(num),
                "pageSize": "30"}

    def start_requests(self):
        urls = [
            'http://www.cninfo.com.cn/cninfo-new/announcement/query',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse,
                                     formdata=self.get_request_body(self.page))

    def parse(self, response):
        logger = logging.getLogger()
        logger.warn("response: poster index page[%s] crawl status: %d", response.url, response.status)
        # logger.warn(unicode(response.body, "utf-8"))
        jsonBody = json.loads(unicode(response.body, "utf-8"))
        # totalRecordNum = jsonBody["totalRecordNum"]
        hasMore = jsonBody["hasMore"]
        data = []
        rowcount = 0
        for row in jsonBody["announcements"]:
            ann = (
                row["announcementId"],
                row["announcementTitle"],
                datetime.fromtimestamp(math.floor(row["announcementTime"] / 1000)),
                row["adjunctUrl"],
                row["adjunctSize"],
                row["adjunctType"],
                row["secCode"],
                row["secName"],
                row["orgId"]
            )
            data.append(ann)
        # 批量插入数据
        conn = psycopg2.connect(self.settings.get('POSTGRESQL_DSN'))
        cur = conn.cursor()
        query_data = ','.join(cur.mogrify('(%s,%s,%s,%s,%s,%s,%s,%s,%s)', row) for row in data)
        # announcement_id,announcement_title,announcement_time,adjunct_url,adjunct_size,adjunct_type,sec_code,sec_name,org_id
        insert_q = "INSERT INTO cninfo_announcement(announcement_id,announcement_title,announcement_time,adjunct_url,adjunct_size,adjunct_type,sec_code,sec_name,org_id) VALUES {0} ON CONFLICT DO NOTHING;".format(
            query_data)
        logger.warn(unicode(insert_q, "utf-8"))
        try:
            cur.execute(insert_q)
            rowcount = cur.rowcount
        except psycopg2.Error:
            self.logger.exception('Database error')
        if rowcount and rowcount > 0:
            if hasMore:
                self.page += 1
                print  self.page
                yield scrapy.FormRequest(url=response.url, callback=self.parse,
                                         formdata=self.get_request_body(self.page))

        conn.commit()
        cur.close()
        conn.close()
