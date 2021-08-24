import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response):
        links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacansy_parse())

    def vacansy_parse(self, response: HtmlResponse):
        name_data = response.xpath("//h1/text()").extract_first()
        salary_data = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract_first()
        link_data = response.url
        url_data = 'https://superjob.ru'
        yield JobparserItem(name=name_data, link=link_data, pay=salary_data, site=url_data)
