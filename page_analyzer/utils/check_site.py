import requests
from bs4 import BeautifulSoup


def check_site(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    h1 = soup.h1.get_text(strip=True) if soup.h1 else None
    title = soup.title.get_text(strip=True) if soup.title else None
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"] if description_tag else None

    return {
        "status_code": res.status_code,
        "h1": h1,
        "title": title,
        "description": description,
    }
