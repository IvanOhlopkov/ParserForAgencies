import requests
import time
import csv
import re
from bs4 import BeautifulSoup


def scrape(source_url, soup):
    agencies = soup.find_all("li", re.compile("fid"))
    for each_agency in agencies:
        name = each_agency.div.find("a").text.strip()
        telephone = each_agency.find("i").text.strip('"')
        country = get_text(each_agency.find("span")).partition(",")[0]
        city = get_text(each_agency.find("span")).partition(",")[2]
        write_to_csv([name, telephone, country, city])


def get_text(el) -> str:
    return el.get_text(strip=True) if el else ""


def write_to_csv(list_input):
    with open("all.csv", "a", newline="") as file_csv:
        csv_writer = csv.writer(file_csv, delimiter=";")
        csv_writer.writerow(list_input)


def browse_and_scrape(seed_url, page_number=0):
    url_pat = re.compile(r"(https://.*\.ru)")
    source_url = url_pat.search(seed_url).group(0)

    formatted_url = seed_url.format(str(page_number))

    try:
        html_text = requests.get(formatted_url).text
        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Now Scrapping - {formatted_url}")

        if soup.find("a", {"title": "Следующая"}) != None:
            scrape(source_url, soup)
            time.sleep(3)
            page_number += 1
            browse_and_scrape(seed_url, page_number)
        else:
            scrape(source_url, soup)
            return True
        return True
    except Exception as e:
        return e


if __name__ == "__main__":
    seed_url = "https://kanzoboz.ru/firms/?grp=11&page={}.html"
    print("Web scrapping has begun")
    result = browse_and_scrape(seed_url)
    if result == True:
        print("Web scraping is now complete!")
    else:
        print(f"Oops, That doens't seem right! - {result}")
