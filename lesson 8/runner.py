from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser import settings
from instaparser.spiders.instapars import InstaparsSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaparsSpider)

    process.start()