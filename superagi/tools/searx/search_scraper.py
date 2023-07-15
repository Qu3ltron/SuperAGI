import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List
from superagi.lib.logger import logger


class SearchResult(BaseModel):
    id: int
    title: str
    link: str
    description: str
    sources: List[str]

    def __str__(self):
        return f"{self.id}. {self.title} - {self.link}\n{self.description}"


def search(query: str, searx_url: str):
    res = httpx.get(
        searx_url + "/search", params={"q": query}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/114.0"}
    )
    if res.status_code != 200:
        logger.info(res.status_code, searx_url)
        raise Exception(f"Searx returned {res.status_code} status code")

    return res.text


def clean_whitespace(s: str):
    return " ".join(s.split())


def scrape_results(html):
    soup = BeautifulSoup(html, "html.parser")
    result_divs = soup.find_all(attrs={"class": "result"})
    
    result_list = []
    n = 1
    for result_div in result_divs:
        if result_div is None:
            continue

        header = result_div.find(["h4", "h3"])
        if header is None:
            continue
        link = header.find("a")["href"]
        title = header.text.strip()

        description = clean_whitespace(result_div.find("p").text)

        sources_container = result_div.find(attrs={"class": "pull-right"}) or result_div.find(attrs={"class": "engines"}) 
        source_spans = sources_container.find_all("span")
        sources = [s.text.strip() for s in source_spans]

        result = SearchResult(id=n, title=title, link=link, description=description, sources=sources)
        result_list.append(result)
        n += 1

    return result_list


def search_results(query: str, searx_url: str):
    return "\n\n".join(str(result) for result in scrape_results(search(query, searx_url)))
