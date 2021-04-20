import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from asiaccb.items import Article
import requests
import json


class asiaccbSpider(scrapy.Spider):
    name = 'asiaccb'
    start_urls = ['https://www.asia.ccb.com/hongkong/personal/index.html']

    def parse(self, response):
        articles = True
        page = 0
        page_limit = 50
        while articles and page <= page_limit:
            json_response = json.loads(requests.get(f"https://iportal5.infocast.hk/iportal-api/ajax/news/getNewsList?type=&locale=en_US&extraMarketNewsIds=&pageSize=12&curShowingPage={1}").text)
            articles = json_response["newsData"]
            if articles:
                yield response.follow(response.url, self.parse_json, dont_filter=True, cb_kwargs=dict(articles=articles))
                page += 1

    def parse_json(self, response, articles):
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            timestamp = int(float(article["time"])/1000)
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            title = " ".join(article["headline"].split("&nbsp;"))
            content = article["content"]

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()