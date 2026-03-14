import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "Linkedin"
    allowed_domains = ["www.linkedin.com"]
    page_count = 1
    max_pages = 5

    vagas = { 
        "Analista de dados": "?keywords=analista%20de%20dados&geoId=106077525",
        "Analista de dados júnior": "?keywords=analista%20de%20dados%20j%C3%BAnior&geoId=106077525",
        "Analista de BI júnior": "?keywords=analista%20de%20bi%20j%C3%BAnior&geoId=106077525",
        "Estagio em Dados": "?keywords=est%C3%A1gio%20em%20dados&geoId=106077525",
        "Analista de Dados (Região Brasil)": "?keywords=analista%20de%20dados&geoId=106057199",
        "Estagio em Dados (Região Brasil)": "?keywords=est%C3%A1gio%20em%20dados&geoId=106057199",
        "Estagio de Engenharia de Dados": "?keywords=est%C3%A1gio%20de%20engenharia%20de%20dados&geoId=106057199",
    }

    def start_requests(self):
        for vaga_name, vaga_url in self.vagas.items():
            url = f"https://www.linkedin.com/jobs/search/{vaga_url}"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "Vaga_name": vaga_name,
                }
            ) # Fazemos a requisição para a URL da API, passando o nome da categoria no meta para usar depois na função parse

    def parse(self, response):
        products = response.css('div.base-card')
        Vaga_name = response.meta.get("Vaga_name")

        for product in products:
            image = (
            product.css('img::attr(src)').get()
            or product.css('img::attr(data-delayed-url)').get()
            or product.css('img::attr(data-ghost-url)').get()
            )
            
            yield {
                'vaga_name': Vaga_name,
                'title': product.css('h3.base-search-card__title::text').get(default='').strip(),
                'company': product.css('a.hidden-nested-link::text').get(default='').strip(),
                'location': product.css('span.job-search-card__location::text').get(default='').strip(),
                'date_posted': product.css('time::attr(datetime)').get(default='').strip(),
                'job_link': product.css('a.base-card__full-link::attr(href)').get(default='').strip(),
                'Logo_image': image.strip() if image else None
            }
        if self.page_count < self.max_pages:
            next_page = response.css('button[aria-label="Next"]::attr(aria-disabled)').get()
            if next_page:
                self.page_count += 1
        yield scrapy.Request(url=next_page, callback=self.parse)

