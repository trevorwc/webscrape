"""
The purpose of this is to crawl the MIT subject listing site and,
for each page of courses, to extract the course title.
This model can be easily adapted to extract more information or edit functionality.
"""
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin, urlparse
import time

subjectListing = 'https://student.mit.edu/catalog/index.cgi'
subjectHTML = urllib.request.urlopen(subjectListing).read()

def extract_links(html_content, base_url):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).scheme in ['http', 'https'] and href.lower().startswith('m') and href.lower().endswith('.html'):
                links.add(full_url)
        return list(links)
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return []

def crawl(url, visited):
    if url in visited:
        return
    visited.add(url)
    print(f"Visiting: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        
        links = extract_links(html_content, url)
        
        for link in links:
            # Recursive call to crawl each link
            crawl(link, visited)
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

def links(start_url):
    visited = set()
    crawl(start_url, visited)
    return visited

def main(v_links):
    all_titles = []
    for link in v_links:
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('h3')
            for title in titles:
                all_titles.append(title.get_text())
        except requests.RequestException as e:
            print(f"Error fetching {link}: {e}")
    return all_titles

if __name__ == "__main__":
    start_url = 'https://student.mit.edu/catalog/index.cgi'
    visited_links = links(start_url)
    course_titles = main(visited_links)
    print(f"Visited {len(visited_links)} links.")
    print(course_titles)
