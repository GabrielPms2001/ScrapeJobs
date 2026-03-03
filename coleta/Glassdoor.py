import csv
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

URL = "https://www.glassdoor.com.br/Vaga/serra-es-analista-de-bi-j%C3%BAnior-vagas-SRCH_IL.0,8_IC2457818_KO9,30.htm"

async def scrape_glassdoor_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,   # importante pro Glassdoor
            slow_mo=50        # navegação mais humana
        )
        page = await browser.new_page()

        await page.goto(URL, timeout=60000)
        await page.wait_for_timeout(5000)  # espera JS carregar

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jobs_data = []

    job_cards = soup.select('li[data-test="jobListing"]')

    for job in job_cards:
        title = job.select_one('a[data-test="job-link"]')
        company = job.select_one('div[data-test="companyName"]')
        location = job.select_one('div[data-test="location"]')
        salary = job.select_one('span[data-test="salary-snippet"]')

        jobs_data.append({
            "title": title.text.strip() if title else "",
            "company": company.text.strip() if company else "",
            "location": location.text.strip() if location else "",
            "salary": salary.text.strip() if salary else ""
        })

    with open("glassdoor_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["title", "company", "location", "salary"]
        )
        writer.writeheader()
        writer.writerows(jobs_data)

    print(f"✅ {len(jobs_data)} vagas salvas com sucesso!")

if __name__ == "__main__":
    asyncio.run(scrape_glassdoor_jobs())