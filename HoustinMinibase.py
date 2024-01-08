import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Define the base URL
base_url = "https://www.houstonisd.org//site/UserControls/Minibase/MinibaseListWrapper.aspx?ModuleInstanceID=317531&PageModuleInstanceID=329255&&PageIndex="
# Define the CSV file path on the desktop
desktop_path = Path.home() / "Desktop"
csv_file_path = desktop_path / "output.csv"

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the header row
    header = [
        "Name Search","Email","Phone","Location","Category","Title Search","Organizational Hierarchy Search"
    ]
    csv_writer.writerow(header)

    # Iterate through each page from 1 to 248
    for page_index in range(1, 5):
        # Construct the URL for the current page
        url = f"{base_url}{page_index}"

        # Send a GET request to the URL
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all sw-flex-item-group elements
        flex_item_groups = soup.find_all('li', class_='sw-flex-item-group')

        # Iterate through each sw-flex-item-group
        for flex_item_group in flex_item_groups:
            data = {}
            # Iterate through each sw-flex-item-list
            for flex_item in flex_item_group.find('ul', class_='sw-flex-item-list').find_all('li', class_='sw-flex-item'):
                label, value = map(str.strip, flex_item.text.split(':', 1))
                data[label] = value

            # Write the extracted information to the CSV file
            csv_writer.writerow([
                data.get('Name Search', ''),
                data.get('Email', ''),
                data.get('Phone', ''),
                data.get('Location', ''),
                data.get('Category', ''),
                data.get('Title Search', ''),
                data.get('Organizational Hierarchy Search', '')
            ])

print(f"CSV file saved to: {csv_file_path}")
