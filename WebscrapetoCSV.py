import requests
from bs4 import BeautifulSoup
import csv
import os

# Specify the URL of the webpage you want to scrape
url = 'https://www.houstonisd.org/Page/154804'

# Send an HTTP request to the URL and get the page content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the collapsed buttons
    collapsed_buttons = soup.find_all('button', {'class': 'btn btn-link', 'data-toggle': 'collapse'})

    # Create a list to store the scraped data
    data = []

    for button in collapsed_buttons:
        button_text = button.get_text(strip=True)
        parent_div = button.find_parent('div', {'class': 'card'})
        card_body = parent_div.find('div', {'class': 'card-body'})
        links = card_body.find_all('a')
        paragraphs = card_body.find_all('p')

        for i in range(len(links)):
            hyperlink_text = links[i].text.strip()
            hyperlink_url = links[i].get('href')
            
            if i < len(paragraphs):
                paragraph_text = paragraphs[i].text.strip()
            else:
                paragraph_text = ""

            data.append([button_text, hyperlink_text, hyperlink_url, paragraph_text])

    # Define the path to the CSV file on the desktop
    desktop_path = os.path.expanduser("~/Desktop")
    csv_file_path = os.path.join(desktop_path, 'scraped_data.csv')

    # Write the data to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Button Text', 'Hyperlink Text', 'Hyperlink URL', 'Paragraph Text'])
        csv_writer.writerows(data)

    print(f'Scraped data has been saved to {csv_file_path}.')
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
