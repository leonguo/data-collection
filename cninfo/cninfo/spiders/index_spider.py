# -*- coding: utf-8 -*-

import scrapy
import json
import logging
import psycopg2
import math
from datetime import date, datetime


class IndexSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
        urls = [
            'http://www.cninfo.com.cn/cninfo-new/announcement/query',
        ]
        today = datetime.today()
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse,
                                     formdata={"seDate": today.strftime('%Y-%m-%d'), "tabName": "fulltext",
                                               "sortName": "time",
                                               "sortType": "desc", "column": "szse", "pageNum": "1",
                                               "pageSize": "30"})

    def parse(self, response):
        logger = logging.getLogger()
        logger.warn("response: poster index page[%s] crawl status: %d", response.url, response.status)
        # logger.warn(unicode(response.body, "utf-8"))
        jsonBody = json.loads(unicode(response.body, "utf-8"))
        totalRecordNum = jsonBody["totalRecordNum"]
        data = []
        for row in jsonBody["announcements"]:
            ann = (
                row["announcementId"],
                row["announcementTitle"],
                datetime.fromtimestamp(math.floor(row["announcementTime"]/1000)),
                row["adjunctUrl"],
                row["adjunctSize"],
                row["adjunctType"],
                row["secCode"],
                row["secName"],
                row["orgId"]
            )
            data.append(ann)
        # 批量插入数据
        conn = psycopg2.connect(database="app", user="postgres", password="123456", host="120.24.229.18", port="5432")
        cur = conn.cursor()
        query_data = ','.join(cur.mogrify('(%s,%s,%s,%s,%s,%s,%s,%s,%s)', row) for row in data)
        # announcement_id,announcement_title,announcement_time,adjunct_url,adjunct_size,adjunct_type,sec_code,sec_name,org_id
        insert_q = "INSERT INTO cninfo_announcement(announcement_id,announcement_title,announcement_time,adjunct_url,adjunct_size,adjunct_type,sec_code,sec_name,org_id) VALUES {0} ON CONFLICT DO NOTHING;".format(query_data)
        logger.warn(unicode(insert_q, "utf-8"))
        try:
            cur.execute(insert_q)
        except psycopg2.Error:
            self.logger.exception('Database error')
        conn.commit()
        cur.close()
        conn.close()
