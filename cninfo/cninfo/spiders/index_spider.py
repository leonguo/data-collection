import scrapy
import json

class IndexSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
        urls = [
            'http://www.cninfo.com.cn/cninfo-new/disclosure/szse_latest',
            'http://www.cninfo.com.cn/cninfo-new/disclosure/sse_latest',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("response: poster index page[%s] crawl status: %d", response.url, response.status)
