import scrapy


class GlassdoorSpider(scrapy.Spider):
    name = "Glassdoor"
    allowed_domains = ["www.glassdoor.com.br"]
    start_urls = ["https://www.glassdoor.com.br/Vaga/serra-esp%C3%ADrito-santo-brasil-analista-de-bi-j%C3%BAnior-vagas-SRCH_IL.0,27_IC2457818_KO28,49.htm"]

    def parse(self, response):
        pass
