import scrapy
from urllib.parse import quote


class IndeedSpider(scrapy.Spider):

    name = "indeed"
    allowed_domains = ["br.indeed.com"]

    # cargos que você quer buscar
    cargos = [
        "estagio em dados",
        "analista de dados",
        "cientista de dados",
        "engenheiro de dados",
        "business intelligence"
    ]

    cidade = "Serra, ES"

    max_pages = 3

    def start_requests(self):

        for cargo in self.cargos:

            cargo_url = quote(cargo)
            cidade_url = quote(self.cidade)

            base_url = f"https://br.indeed.com/jobs?q={cargo_url}&l={cidade_url}"

            for page in range(self.max_pages):

                start = page * 10

                url = f"{base_url}&start={start}"

                yield scrapy.Request(
                    url,
                    meta={
                        "playwright": True,
                        "cargo_busca": cargo
                    },
                    callback=self.parse
                )

    async def parse(self, response):

        cargo_busca = response.meta["cargo_busca"]

        jobs = response.css("div.job_seen_beacon")

        for job in jobs:

            yield {

                "cargo_busca": cargo_busca,

                "titulo": job.css("h2 a span::text").get(),

                "empresa": job.css(
                    'span[data-testid="company-name"]::text'
                ).get(),

                "local": job.css(
                    'div[data-testid="text-location"]::text'
                ).get(),

                "link": response.urljoin(
                    job.css("h2 a::attr(href)").get()
                )
            }