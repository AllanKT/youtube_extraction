import scrapy
from scrapy.crawler import CrawlerProcess

from src.utils import *
from src.settings import *

class YoutubeSpider(scrapy.Spider):
    name = 'youtube_spider'
    start_urls = [configs.URL_YOUTUBE_SCRAP]

    def parse(self, response):
        script = response.xpath("//script[contains(text(), 'videoRenderer')]").extract_first()
        for item in get_recursively(list(extract_json(script))[0], 'videoRenderer'):
            yield {
                'title': item['title']['runs'][0]['text'].encode().decode('utf-8', 'ignore'),
                'link': configs.URL_YOUTUBE_WATCH + item['videoId'],
            }
