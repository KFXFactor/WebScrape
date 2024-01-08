import requests
from bs4 import BeautifulSoup

# Specify the URL of the webpage you want to scrape
url = 'https://compliancenews.com/get-certified'

# Send an HTTP request to the URL and get the page content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the collapsed buttons
    collapsed_buttons = soup.find_all('button', {'class': 'btn btn-link', 'data-toggle': 'collapse'})

    for button in collapsed_buttons:
        button_text = button.get_text(strip=True)
        parent_div = button.find_parent('div', {'class': 'card'})
        card_body = parent_div.find('div', {'class': 'card-body'})
        links = card_body.find_all('a')
        paragraphs = card_body.find_all('p')

        print(f'Button Text: {button_text}')
        
        for i in range(len(links)):
            hyperlink_text = links[i].text.strip()
            hyperlink_url = links[i].get('href')
            
            if i < len(paragraphs):
                paragraph_text = paragraphs[i].text.strip()
            else:
                paragraph_text = ""
            
            print(f'Hyperlink Text: {hyperlink_text}')
            print(f'Hyperlink URL: {hyperlink_url}')
            print(f'Paragraph Text: {paragraph_text}')
            print('---')

else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
