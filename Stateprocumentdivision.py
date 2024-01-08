import requests
from bs4 import BeautifulSoup
import csv
import os

# Set the URL of the website
url = "https://www.houstontx.gov/bizwithhou/EEDirectory.html"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find left and right side elements
    left_side_elements = soup.select('.col-md-6 .col-md-12')  # Assuming left side is in a div with class 'col-md-6'
    right_side_elements = soup.select('.col-md-6 .col-md-12:nth-of-type(2)')  # Assuming right side is the second div in 'col-md-6'

    # Create a list to store the extracted data
    data_list = []

    # Extract the data from left and right side elements
    for left, right in zip(left_side_elements, right_side_elements):
        title = left.find('strong').text.strip()
        email = left.find('a', href=lambda href: href and "mailto:" in href).text.strip()
        phone = right.get_text(strip=True)  # Extract plain text from the right side element

        # Append the data to the list
        data_list.append([title, email, phone])

    # Define the path for the CSV file on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    csv_file_path = os.path.join(desktop_path, "output.csv")

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header
        csv_writer.writerow(['Title', 'Email', 'Phone Number'])
        
        # Write data rows
        csv_writer.writerows(data_list)

    print(f"Scraping successful. Data has been saved to {csv_file_path}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
