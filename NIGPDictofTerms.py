import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    terms = soup.find_all('h3')
    descriptions = soup.find_all('div', class_='description')

    data = []
    for term, description in zip(terms, descriptions):
        term_text = term.text.strip()
        if term_text:
            definition = description.text.strip()
            data.append((term_text, definition))

    return data

def write_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def scrape_all_pages(base_url, max_pages, output_file):
    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?page={page_num}"
        print(f"Scraping page {page_num}...")
        data = scrape_page(url)
        write_to_csv(data, output_file)
    print("Scraping complete.")

def main():
    base_url = "https://www.nigp.org/dictionary-of-terms"
    max_pages = 206
    output_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'nigp_dictionary.csv')

    # Write CSV header
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Term', 'Definition'])

    scrape_all_pages(base_url, max_pages, output_file)

if __name__ == "__main__":
    main()
