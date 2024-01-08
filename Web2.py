import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

# URL of the website
url = "https://www.houstonisd.org/Page/154804"

# Function to scrape the content using requests and BeautifulSoup
def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract and print the content
    content = soup.find('div', class_='content')
    return content.text.strip()

# Function to interact with the submit button using Selenium
def interact_with_submit_button(url):
    # Set up Chrome options to run headless (without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Create a Chrome webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL in the webdriver
    driver.get(url)

    # Find the submit button by its ID (you need to inspect the HTML to find the correct ID)
    submit_button = driver.find_element(By.ID, 'minibaseSubmit327729')

    # Click the submit button
    submit_button.click()

    # Wait for a few seconds to let the page load (you may need to adjust this based on the page)
    driver.implicitly_wait(5)

    # Extract and print the content after submitting

    # Extract and print all elements with the class 'accordionButton'
    content1_elements = [element.text.strip() for element in driver.find_elements(By.CSS_SELECTOR, '.accordionButton')]

    # Extract and print all elements with the class 'accordionContent'
    content2_elements = [element.text.strip() for element in driver.find_elements(By.CSS_SELECTOR, '.accordionContent')]

    # Extract and print content from each page using pagination
    page_data = extract_content_from_each_page(driver)

    # Close the webdriver
    driver.quit()

    # Get the user's desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Write data to CSV on the desktop
    write_to_csv(content1_elements, content2_elements, page_data, os.path.join(desktop_path, 'scrapedata.csv'))

def extract_content_from_each_page(driver):
    # Find the pagination container
    pagination_container = driver.find_element(By.CLASS_NAME, 'ui-paging-container')

    # Find all elements with the class 'ui-pagination-list' within the container
    pagination_elements = pagination_container.find_elements(By.CLASS_NAME, 'ui-pagination-list')

    # Store data for each page
    page_data = {}

    # Loop through each pagination element and click to navigate through pages
    for pagination_element in pagination_elements:
        # Click the pagination element to navigate to the next page
        pagination_element.click()

        # Wait for a few seconds to let the page load (you may need to adjust this based on the page)
        driver.implicitly_wait(5)

        # Extract and store the content after navigating to the next page
        content1_elements = [element.text.strip() for element in driver.find_elements(By.CSS_SELECTOR, '.accordionButton')]
        content2_elements = [element.text.strip() for element in driver.find_elements(By.CSS_SELECTOR, '.accordionContent')]

        # Store data for each page
        page_data[pagination_element.text.strip()] = {'Content1': content1_elements, 'Content2': content2_elements}

    return page_data

def write_to_csv(content1_elements, content2_elements, page_data, file_path):
    # Writing data to CSV
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Content1', 'Content2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data from the initial page
        for content1, content2 in zip(content1_elements, content2_elements):
            writer.writerow({'Content1': content1, 'Content2': content2})

        # Write data from each page
        for page, data in page_data.items():
            for content1, content2 in zip(data['Content1'], data['Content2']):
                writer.writerow({'Content1': content1, 'Content2': content2})

# Uncomment the function you want to use
# scrape_content(url)
interact_with_submit_button(url)
