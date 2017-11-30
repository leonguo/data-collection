import scrapy


class IndexSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
        urls = [
            'http://www.cninfo.com.cn/cninfo-new/index',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = "index"
        filename = 'cninfo-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)