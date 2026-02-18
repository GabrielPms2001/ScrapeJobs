import requests
import json
import time

URL = "https://www.glassdoor.com.br/job-search-next/bff/jobSearchResultsQuery"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://www.glassdoor.com.br",
    "Referer": "https://www.glassdoor.com.br/",
})

# ⬇️ COLE AQUI OS COOKIES DO BROWSER
session.cookies.update({
    "cf_clearance": "ZyweTKhOMX0UOtA.0t2yqS4ki5sQMjcCG08vYSWI.pg-1771445528-1.2.1.1-KjV_QjGEHHb9Uy1qVvf1hdfviusZSveZZi645rlhE6CAb3htX21MfKwhwfabk6z5M0qPAX5H533prPWGkfxVJQbtNC9tTHPeYRHZ3JPTAtwCZ3IHqLXUgKzjO8vxEWaxYJDAQDnbI.o9YTkX8CjxAEBFcYLjguPviSklCxi5I4r_z4Zd7UQe3wvgLLQtDYLzvwm27QYsGlsc5r_PNskgW.OqvVWpwamWXBssb8KefZU",
    "__cf_bm": "M81j0wC0mfqNkxYHBiaP40LCotRpvMXTpWAcbDBlvho-1771445387-1.0.1.1-SGvF6mmJxe7f1thmK2pjzj3VRDhLPKqlNWL7Tk9o4oJgnwdbZG6rMTqYcfzVJn_OurGIvytKdoctgHakVrpfW.Zm6EjbLr0A84OoiRiFCw0",
    "gdId": "0d71ec13-6ddb-475e-9895-002c5a9eae1d",
    "JSESSIONID": "6A4E626EE50574100C79EAAFC919DAA6",
    "GSESSIONID": "6A4E626EE50574100C79EAAFC919DAA6",
})

# 1️⃣ visita inicial (cria contexto)
session.get("https://www.glassdoor.com.br")

payload = {
    "keyword": "analista de bi júnior",
    "locationId": 0,
    "numJobsToShow": 30,
    "pageNumber": 1,
    "pageCursor": None,
    "excludeJobListingIds": [],
    "filterParams": [],
    "includeIndeedJobAttributes": False
}

response = session.post(URL, json=payload)

print(response.status_code)
print(response.text[:500])
