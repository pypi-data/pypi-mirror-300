import time
from fadex import get_meta_and_title, extract_links
from bs4 import BeautifulSoup
from lxml import html as lxml_html
import requests

def fetch_html(url):
    print(f"Fetching HTML content for {url}...")
    response = requests.get(url)
    print(f"Content fetched for {url}.")
    return response.text

def benchmark_fadex(html, iterations):
    total_time = 0
    print("Starting Fadex benchmark...")
    for i in range(iterations):
        if i % 100 == 0:
            print(f"Fadex iteration {i}/{iterations}")
        start = time.time()
        links = extract_links(html)
        total_time += time.time() - start
    print("Fadex benchmark complete.")
    return total_time / iterations

def benchmark_beautifulsoup(html, iterations):
    total_time = 0
    print("Starting BeautifulSoup benchmark...")
    for i in range(iterations):
        if i % 100 == 0:
            print(f"BeautifulSoup iteration {i}/{iterations}")
        start = time.time()
        soup = BeautifulSoup(html, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        total_time += time.time() - start
    print("BeautifulSoup benchmark complete.")
    return total_time / iterations

def benchmark_lxml(html, iterations):
    total_time = 0
    print("Starting lxml benchmark...")
    for i in range(iterations):
        if i % 100 == 0:
            print(f"lxml iteration {i}/{iterations}")
        start = time.time()
        tree = lxml_html.fromstring(html)
        links = tree.xpath('//a/@href')
        total_time += time.time() - start
    print("lxml benchmark complete.")
    return total_time / iterations

urls = [
    "https://www.godaddy.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://google.com",
    "https://youtube.com",
    "https://gmail.com"
]

iterations = 1000  # Number of iterations per URL
fadex_total_time = 0
beautifulsoup_total_time = 0
lxml_total_time = 0

for url in urls:
    html = fetch_html(url)
    print(f"Benchmarking Fadex for {url}...")
    fadex_total_time += benchmark_fadex(html, iterations)
    print(f"Benchmarking BeautifulSoup for {url}...")
    beautifulsoup_total_time += benchmark_beautifulsoup(html, iterations)
    
    print(f"Benchmarking lxml for {url}...")
    lxml_total_time += benchmark_lxml(html, iterations)

# Calculate average time across all URLs and iterations
fadex_avg_time = fadex_total_time / len(urls)
beautifulsoup_avg_time = beautifulsoup_total_time / len(urls)
lxml_avg_time = lxml_total_time / len(urls)

print("\n--- Benchmark Results ---")
print(f"Average Fadex Time: {fadex_avg_time} seconds")
print(f"Average BeautifulSoup Time: {beautifulsoup_avg_time} seconds")
print(f"Average lxml Time: {lxml_avg_time} seconds")

# Determine the winner
if fadex_avg_time < beautifulsoup_avg_time and fadex_avg_time < lxml_avg_time:
    print("Winner: Fadex")
elif beautifulsoup_avg_time < fadex_avg_time and beautifulsoup_avg_time < lxml_avg_time:
    print("Winner: BeautifulSoup")
else:
    print("Winner: lxml")
