import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from urllib.parse import urljoin

BASE_URL = 'https://reactjs.org'


def scrape_page(url):
    links = []
    print(f'Scraping {url}')
    page = fetch_page(url)
    if page:
        content = parse_content(page)
        save_content(content, 'reactdocs.txt')
        try:
            links = extract_links(page)
        except Exception as e:
            print(e)
        return links


def fetch_page(url):
    try:
        resp = requests.get(url)
        if resp.ok:
            return BeautifulSoup(resp.text, 'html.parser')
    except requests.RequestException as e:
        print(e)


def parse_content(page):
    content = ''
    for p in page.find_all('p'):
        content += clean_text(p.text) + '\n'
    return content


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def save_content(content, filename):
    with open(filename, 'a') as f:
        f.write(content)



def extract_links(page):

  links = set()

  for link in page.find_all('a'):

    path = link.get('href')
    
    if path.startswith('/'): # Must start with /

      links.add(path)

  return links

def main():
    to_crawl = {BASE_URL}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        while to_crawl:
            futures = [executor.submit(scrape_page, urljoin(
                BASE_URL, url)) for url in to_crawl]
            to_crawl = set()
            for future in concurrent.futures.as_completed(futures):

                try:
                    links = future.result()
                    if links:
                        to_crawl.update(links)
                except Exception as e:
                    print(e)
    print('Crawling complete')


if __name__ == '__main__':
    main()
