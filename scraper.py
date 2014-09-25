import re
import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

def scrape(start_date):
    proto = "http://"
    host = "en.wikipedia.org"

    scrape_date = start_date
    today = date.today()

    facts = []
    while scrape_date < today:
        date_str = scrape_date.strftime("%Y/%B")
        print(date_str)

        path = "/wiki/Wikipedia:Recent_additions/" + date_str

        url = proto + host + path
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            print(resp)
            print(resp.url)
            return

        soup = BeautifulSoup(resp.text)
        for li in soup.select("div#mw-content-text li"):
            fact = re.sub(r"\s+", " ", li.text.strip())
            if re.match(r"^\.\.\.", fact):
                obj = {}

                obj["fact"] = fact

                subject = None
                try:
                    subject = next(b.find("a") for b in li.find_all("b"))
                except:
                    try:
                        if not subject:
                            subject = next(a for a in li.find_all("a") if a.find("b"))
                    except:
                        print li.contents

                if not subject:
                    continue

                obj["subject"] = {
                    "title": subject["title"],
                    "href": subject["href"]
                }

                obj["links"] = []
                for a in li.find_all("a"):
                    if a["href"] != obj["subject"]["href"]:
                        obj["links"].append({
                            "title": a.get("title", ""),
                            "href": a["href"]
                        })

                facts.append(obj)

        scrape_date += relativedelta(months=1)
    return facts;

if __name__ == "__main__":
    # Archive from 2004
    facts = scrape(date(2004, 02, 1))

    with open("en_facts.json", "w") as f:
        json.dump(facts, f)
