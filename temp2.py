import csv
import requests
from bs4 import BeautifulSoup

# URL of the page
url = "https://www.houstonisd.org//site/UserControls/Minibase/MinibaseListWrapper.aspx?ModuleInstanceID=317531&PageModuleInstanceID=329255&&PageIndex=1"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the list item with class "sw-flex-item-group"
    list_item = soup.find("li", class_="sw-flex-item-group")

    # Extract data from various list items within the main list item
    vendor_name = list_item.find("div", class_="sw-minibase-list-number").get_text(strip=True)
    vendor_info_items = list_item.find_all("li", class_="sw-flex-item")

    # Create a dictionary to store the extracted data
    data = {
        "Vendor Name": vendor_name,
    }

    # Iterate through vendor_info_items and add data to the dictionary
    for item in vendor_info_items:
        label = item.find("label", class_="sw-flex-item-label").get_text(strip=True)
        value = item.get_text(strip=True, separator=' ')[len(label):]
        data[label[:-1]] = value

    # Specify the CSV file path
    csv_file_path = "C:/Users/Konstantinos/Desktop/vendor_data.csv"

    # Write the data to a CSV file
    with open(csv_file_path, mode="w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

    print(f"Data has been successfully extracted and written to {csv_file_path}")
else:
    print(f"Failed to retrieve data. Status Code: {response.status_code}")
