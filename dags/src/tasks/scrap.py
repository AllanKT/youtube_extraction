import scrapy
from scrapy.crawler import CrawlerProcess

from src.models.youtube_spider import YoutubeSpider
from src.settings import *

def scrap():
    print("taks: scrap function running")
    process = CrawlerProcess(configs.PROCESS)
    process.crawl(YoutubeSpider)
    process.start()
