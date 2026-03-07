import scrapy


class IndeedSpider(scrapy.Spider):

    name = "indeed"

    def start_requests(self):

        url = "https://br.indeed.com/jobs?q=estagio+em+dados&l=Serra%2C+ES"

        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True
            },
            callback=self.parse
        )

    async def parse(self, response):

        jobs = response.css("div.job_seen_beacon")

        for job in jobs:

            yield {

                "titulo": job.css("h2 a span::text").get(),

                "empresa": job.css("div span.company-name::text").get(),

                "local": job.css("div div span div::text").get(),

                "link": response.urljoin(
                    job.css("h2 a::attr(href)").get()
                )
            }

        next_page = response.css("a[data-testid='pagination-page-next']::attr(href)").get()

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                meta={"playwright": True},
                callback=self.parse
            )