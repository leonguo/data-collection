# -*- coding: utf-8 -*-

import scrapy
import json
import logging
import math
from datetime import date, datetime
from ..items import AnnouncementItem
from scrapy.loader import ItemLoader


# 最新公告爬取

class IndexSpider(scrapy.Spider):
    name = "index"
    page = 1

    custom_settings = {
        'ITEM_PIPELINES': {
            'cninfo.pipelines.AnnouncementPipeline': 300,
        }
    }

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
        json_body = json.loads(response.body)
        has_more = json_body["hasMore"]
        rowcount = 0
        for row in json_body["announcements"]:
            if row.get("announcementId", None):
                loader = ItemLoader(item=AnnouncementItem())
                loader.default_output_processor = scrapy.loader.processors.TakeFirst()
                loader.add_value("announcement_id", row["announcementId"])
                loader.add_value("announcement_title", row["announcementTitle"])
                loader.add_value("announcement_time",
                                 datetime.fromtimestamp(math.floor(row["announcementTime"] / 1000)))
                loader.add_value("adjunct_url", row["adjunctUrl"])
                loader.add_value("adjunct_size", row["adjunctSize"])
                loader.add_value("adjunct_type", row["adjunctType"])
                loader.add_value("sec_code", row["secCode"])
                loader.add_value("sec_name", row["secName"])
                loader.add_value("org_id", row["orgId"])
                yield loader.load_item()
                rowcount = rowcount + 1

        # 批量插入数据
        if rowcount and rowcount > 0:
            if has_more:
                self.page += 1
                print(self.page)
                yield scrapy.FormRequest(url=response.url, callback=self.parse,
                                         formdata=self.get_request_body(self.page))
