import re
import time
import gzip

from seleniumwire import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from pymongo import MongoClient, UpdateOne

#  pip install blinker==1.7.0 "setuptools<81" pymongo webdriver-manager selenium selenium-wire beautifulsoup4

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["job_market_trends"]
db_jobbank = db["job_postings"]

FIRST_RUN = False


# parse first page and more page html
def parse_articles_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')
    jobs = []
    for art in articles:
        art.select_one("span.job-action").decompose()

        art_id = art.get('id')
        new_flag = bool(art.find(class_='new'))
        job_source = art.find(class_='job-source').get_text(strip=True) if art.find(class_='job-source') else None
        noctitle = art.find(class_='noctitle').get_text(strip=True) if art.find(class_='noctitle') else None
        date = art.find(class_='date').get_text(strip=True) if art.find(class_='date') else None
        business = art.find(class_='business').get_text(strip=True) if art.find(class_='business') else None
        location = "".join(art.find(class_='location').find_all(string=True, recursive=False)).strip() if art.find(
            class_='location') else None
        salary = art.find(class_='salary').get_text(strip=True) if art.find(class_='salary') else None
        salary = salary.replace("Salary:", "").replace("Salary", "").strip() if salary else None
        job_number = "".join(art.find(class_='source').find_all(string=True, recursive=False)).strip() if art.find(
            class_='source') else None
        raw_html = str(art)

        job = {
            'id': art_id,
            'new_flag': new_flag,
            'job_source': job_source,
            'noctitle': noctitle,
            'date': date,
            'business': business,
            'location': location,
            'salary': salary,
            'job_number': job_number,
            'raw_html': raw_html,
        }
        jobs.append(job)

    return jobs


def fetch_more_jobs(driver):
    print("---fetching more---")
    # driver.requests.clear()
    baseline = len(driver.requests)

    driver.execute_script("showmore();")
    time.sleep(3)
    # print(f"len(driver.requests): {len(driver.requests)}")
    for req in driver.requests[baseline:]:
        if "/jobsearch/job_search_loader.xhtml" in req.path:
            body = None
            try:
                body = gzip.decompress(req.response.body).decode('utf-8', errors='replace')
                more_jobs = parse_articles_html(body)
                # print(json.dumps(more_jobs[:1], ensure_ascii=False, indent=2))
                # print(req.response.date)
                print(f"---fetched {len(more_jobs)} more jobs---")
                return more_jobs
            except Exception as e:
                print(e)
                print(body)
                return None


def save_jobs(jobs):
    if jobs:
        ops = [UpdateOne({"id": job.get("id")}, {"$set": job}, upsert=True)
               for job in jobs]
        db_jobbank.bulk_write(ops)
    count = db_jobbank.count_documents({})
    print(f"---{len(jobs)} jobs wrote to mongodb, current total: {count}---")


def exist_any_in_db(jobs):
    more_ids = [job.get("id") for job in jobs]
    exist = db_jobbank.find_one({"id": {"$in": more_ids}})
    return bool(exist)


def save_first_page(driver):
    wait = WebDriverWait(driver, 15)

    # wait until div.results-jobs article loaded
    articles = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.results-jobs article")
    ))
    first_page_html = "".join([article.get_attribute("outerHTML")
                               for article in articles])

    first_page_jobs = parse_articles_html(first_page_html)
    save_jobs(first_page_jobs)
    return first_page_jobs


def save_prov_jobs(driver, prov):
    # sort by date posted
    url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=D&fprov={prov}"
    driver.get(url)  # sort by date posted

    first_page_jobs = save_first_page(driver)

    # first_run: always fetch_more,
    # other: fetch more when no any exist in db
    fetch_more = FIRST_RUN or not exist_any_in_db(first_page_jobs)

    while fetch_more:
        more_jobs = fetch_more_jobs(driver)
        save_jobs(more_jobs)
        if (len(more_jobs) == 0  # no more
                or (not FIRST_RUN and exist_any_in_db(more_jobs))):  # all new fetched
            fetch_more = False

def main():
    provs = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
    # provs = ["MB", "NB", "NL"]
    # provs += ["NS", "NT", "NU"]
    # provs += ["PE", "SK", "YT"]
    # print(provs)
    # provs = ["AB"]
    # provs = ["BC"]
    # provs = ["ON"]
    # provs = ["QC"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for prov in provs:
        print(f"---fetching {prov} jobs start")
        save_prov_jobs(driver, prov)
        print(f"---fetching {prov} jobs finish")

    driver.quit()

def foo():
    job_sources = db_jobbank.distinct("job_source", {"location": re.compile(r"\(ON\)")})
    print(job_sources)

if __name__ == "__main__":
    # foo()
    main()
    pass
