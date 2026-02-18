import scrapy


class GlassdoorSpider(scrapy.Spider):
    name = "Glassdoor"
    allowed_domains = ["www.glassdoor.com.br"]
    start_urls = ["https://www.glassdoor.com.br"]

    def parse(self, response):
        pass
