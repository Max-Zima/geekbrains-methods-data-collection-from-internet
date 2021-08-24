import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&items_on_page=20&text=python']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacansy_parse())

    def vacansy_parse(self, response:HtmlResponse):
        name_data = response.xpath("//h1/text()").extract_first()
        salary_data = response.xpath("//p[@class='vacancy-salary']/span/text()").extract_first()
        link_data = response.url
        url_data = 'https://hh.ru'
        yield JobparserItem(name=name_data, link=link_data, pay=salary_data, site=url_data)
