import csv
from playwright.asinc_api import async_playwright
from lxml.html import fromstring

async def scrape_glassdoor_jobs():
    #setup the playwright browser with proxy to avoid detection
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={
                "server": '', "username": '', "password": ''}
        )
        page = await browser.new_page()
        await page.goto('' timeout=60000)

        #Retrieve the page content and close the browser
        content =  await page.content()
        await browser.close()

        #Parse the HTML content using lxml
        parser = fromstring(content)
        job_posting_elements = parser.xpath('//li[@data-test="jobListing"]')

        #Extract data for each job listing
        jobs_data = []
        for job in job_posting_elements:
            title = job.xpath('.//a[@data-test="job-link"]/text()')
            company = job.xpath('.//div[@data-test="companyName"]/text()')
            location = job.xpath('.//div[@data-test="location"]/text()')
            salary = job.xpath('.//span[@data-test="salary-snippet"]/text()')

            job_data = {
                'title': title[0].strip() if title else '',
                'company': company[0].strip() if company else '',
                'location': location[0].strip() if location else '',
                'salary': salary[0].strip() if salary else ''
            }
            jobs_data.append(job_data)

        # Save the data to a CSV file
        with open('glassdoor_jobs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'company', 'location', 'salary'])
            writer.writeheader()
            writer.writerows(jobs_data)

# Run the Scraping function
import asyncio
asyncio.run(scrape_glassdoor_jobs())
            