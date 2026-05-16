import requests


def check_site(url):
    res = requests.get(url)
    res.raise_for_status()
    return {"status_code": res.status_code}
