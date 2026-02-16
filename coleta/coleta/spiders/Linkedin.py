import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "Linkedin"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["https://www.linkedin.com"]

    def parse(self, response):
        pass
