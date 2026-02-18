import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "Linkedin"
    allowed_domains = ["www.linkedin.com"]

    vagas = { 
        "Analista de dados": "?keywords=analista%20de%20dados&geoId=106077525",
        "Analista de dados júnior": "?keywords=analista%20de%20dados%20j%C3%BAnior&geoId=106077525",
        "Analista de BI júnior": "?keywords=analista%20de%20bi%20j%C3%BAnior&geoId=106077525"
    }

    def start_requests(self):
        for vaga_name, vaga_url in self.vagas.items():
            url = f"https://www.linkedin.com/jobs/search/{vaga_url}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('div.base-card')

        for product in products:
            
            yield {
                'title': product.css('h3.base-search-card__title::text').get(),
                'company': product.css('h4.base-search-card__subtitle::text').get(),
                'location': product.css('span.job-search-card__location::text').get(),
                'date_posted': product.css('time::attr(datetime)').get(),
                'job_link': product.css('a.base-card__full-link::attr(href)').get(),
                'media': product.css('img.base-search-card__image::attr(src)').get(),
            }
