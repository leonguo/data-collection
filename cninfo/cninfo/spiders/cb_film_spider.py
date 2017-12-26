# -*- coding: utf-8 -*

import scrapy
import json
from datetime import date, datetime
import sys
from ..items import FilmOfficeItem
from scrapy.loader import ItemLoader
from urllib import parse

# 中国票房 数据
class CbFilmSpider(scrapy.Spider):
    name = "cbfilm"
    page = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'cninfo.pipelines.FilmPipeline': 300,
        }
    }

    area_list = {
        "14": "西班牙",
        "42": "墨西哥",
        "11": "澳大利亚",
        "43": "印度",
        "2102": "尼日利亚",
        "24": "丹麦",
        "20": "荷兰",
        "26": "瑞典",
        "32": "捷克",
        "8": "巴西",
        "22": "阿根廷",
        "19": "比利时",
        "9": "菲律宾",
        "6": "瑞士",
        "45": "芬兰",
        "33": "匈牙利",
        "17": "奥地利",
        "31": "俄罗斯",
        "29": "韩国",
        "69": "爱尔兰",
        "3": "波兰",
        "44": "葡萄牙",
        "13": "挪威",
        "10": "以色列",
        "21": "希腊",
        "74": "古巴",
        "60": "智利",
        "15": "土耳其",
        "28": "新西兰",
        "39": "立陶宛",
        "41": "马耳他",
        "75": "伊朗",
        "54": "泰国",
        "46": "保加利亚",
        "64": "克罗地亚",
        "51": "印度尼西亚",
        "23": "哥伦比亚",
        "66": "罗马尼亚",
        "18": "南非",
        "35": "马来西亚",
        "48": "塞浦路斯",
        "49": "巴拿马",
        "82": "南联盟",
        "5": "新加坡",
        "27": "秘鲁",
        "52": "黎巴嫩",
        "53": "波多黎各",
        "38": "埃及",
        "47": "委内瑞拉",
        "55": "牙买加",
        "36": "爱沙尼亚",
        "56": "特立尼达和多巴哥",
        "65": "斯洛文尼亚",
        "57": "多米尼加",
        "12": "冰岛",
        "34": "卢森堡",
        "58": "危地马拉",
        "68": "斯洛伐克",
        "59": "乌拉圭",
        "61": "厄瓜多尔",
        "62": "玻利维亚",
        "63": "拉脱维亚",
        "67": "南斯拉夫",
        "70": "肯尼亚",
        "72": "乌克兰",
        "73": "摩洛哥",
        "76": "坦桑尼亚",
        "77": "波黑",
        "78": "越南",
        "79": "津巴布韦",
        "80": "阿尔及利亚",
        "81": "巴勒斯坦",
        "83": "塞内加尔",
        "84": "巴基斯坦",
        "85": "阿尔巴尼亚",
        "86": "格鲁吉亚",
        "87": "布基纳法索",
        "88": "亚美尼亚",
        "89": "海地",
        "90": "吉尔吉斯坦",
        "91": "尼泊尔",
        "92": "哈萨克斯坦",
        "93": "突尼斯",
        "94": "卢旺达",
        "95": "纳米比亚",
        "96": "乌兹别克斯坦",
        "97": "斯里兰卡",
        "98": "喀麦隆",
        "99": "加纳",
        "100": "巴哈马",
        "101": "中国澳门",
        "102": "西德",
        "103": "前苏联",
        "104": "捷克斯洛伐克",
        "105": "东德",
        "106": "摩纳哥",
        "107": "列支敦士登",
        "108": "利比亚",
        "109": "象牙海岸",
        "110": "乍得",
        "111": "博茨瓦纳",
        "112": "阿富汗",
        "113": "格陵兰岛",
        "114": "蒙古",
    }

    # www.cbooo.cn
    def start_requests(self):
        for area in self.area_list:
            url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area={0}&type=0&year=0&initial=%E5%85%A8%E9%83%A8&pIndex=1'.format(
                area)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.warning("response: film page url [%s] crawl status: %d", response.url, response.status)
        if response.status == 200:
            cur_url = parse.urlparse(response.url)
            url_query = parse.parse_qs(cur_url.query)
            area = url_query["area"][0]
            area_name = self.area_list[area]
            json_body = json.loads(unicode(response.body, "utf-8"))
            t_page = json_body.get("tPage", None)
            if json_body.get("pData", None):
                for row in json_body["pData"]:
                    name = row.get("MovieName", None)
                    if name:
                        loader = ItemLoader(item=FilmOfficeItem())
                        loader.default_output_processor = scrapy.loader.processors.TakeFirst()
                        loader.add_value("film_name", row["MovieName"])
                        loader.add_value("film_eng_name", row["MovieEnName"])
                        loader.add_value("film_year", row["releaseYear"])
                        loader.add_value("cb_box_office", row["BoxOffice"])
                        loader.add_value("film_area", area_name)
                        yield loader.load_item()

            if self.page <= t_page:
                self.page += 1
                next_page_url = "http://www.cbooo.cn/Mdata/getMdata_movie?area={0}&type=0&year=0&initial=%E5%85%A8%E9%83%A8&pIndex={1}".format(
                    area, self.page)
                self.logger.warning("crawl www.cbooo.cn page url :: [%s] ", next_page_url)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
