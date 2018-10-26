import scrapy
import logging
class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ['file:///Users/Rossonero/Developer/jjzl_zdjj.jsp']


    # def __init__(self, stats):
    #     logger = logging.getLogger('test')
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.stats)

    def parse(self, response):

        print('====___', self.crawler.stats.spider_stats)
        # print(self.crawler.spider_stats)
        yield {
            1:2
        }