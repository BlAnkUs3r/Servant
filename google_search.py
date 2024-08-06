# google_search.py

import requests
from bs4 import BeautifulSoup

def google_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    print(f"Google search response status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text if g.find('h3') else 'No title'
            search_results.append(f"{title}: {link}")
    print(f"Parsed search results: {search_results}")
    return search_results
