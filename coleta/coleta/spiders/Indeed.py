import scrapy


class IndeedSpider(scrapy.Spider):
    name = "Indeed"
    allowed_domains = ["br.indeed.com"]

    vagas = {
        "Analista de Dados" : "",
        "Analista de Dados Júnior" : "",
        "Analista de BI Júnior" : ""
    }
    start_urls = ["https://br.indeed.com"]

    def parse(self, response):
        pass
