import requests
from bs4 import BeautifulSoup
from bs4._typing import _QueryResults

SHAMELA_URL='https://shamela.ws/ajax/search'

def send_search_request(term: str) -> requests.Response:
    url = SHAMELA_URL
    payload = {"term": term}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url, data=payload, headers=headers)
    return requests.Response() if response.status_code != 200 else response


def get_anchors_from_response(response: requests.Response) -> _QueryResults:
    if not response.text : return None
    soup = BeautifulSoup(response.text, 'html.parser')
    anchors = soup.find_all('a', href=True)
    return anchors


def get_links_from_anchor(anchor: _QueryResults) -> str:
    link = anchor['href']
    return link


def get_title_from_anchor(anchor: _QueryResults) -> str:
    title_tag = anchor.find('span', class_='text-primaryy')
    title = title_tag.get_text(strip=True) if title_tag else anchor.get_text(strip=True)
    return title


def get_preview_from_anchor(anchor: _QueryResults) -> str:
    preview_tag = anchor.find_next('p')
    preview_text = preview_tag.get_text(strip=True) if preview_tag else anchor.get_text(strip=True)
    return preview_text


def get_results_aggregate(response: requests.Response) -> [str, str, str]:
    anchors = get_anchors_from_response(response)
    if not anchors : return None
    results = []
    for anchor in anchors:
        link = get_links_from_anchor(anchor)
        title = get_title_from_anchor(anchor)
        preview = get_preview_from_anchor(anchor)
        results.append([link, title, preview])
    return results


if __name__ == "__main__":
    term = input("Input a search term: ")
    response = send_search_request(term)
    results = get_results_aggregate(response)
    if results:
        print("Search results: ")
        for result in results:
            print(result)

