import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL of the collection page
url = "https://www.lakai.com/collections/shoes"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the product grid items
    product_list = soup.find('ul', class_='products-grid-items')
    products = product_list.find_all('li')  # Each product is in an <li> tag

    # Open a CSV file to write data
    with open('lakai_links.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writerow(['Link', 'Scraped Date'])

        # Extract product links
        for product in products:
            # Try to find the link by different classes
            link_tag = product.find('a', class_='products-grid-item-link')
            if not link_tag:
                link_tag = product.find('a')  # Fallback to any <a> tag

            if link_tag and link_tag.get('href'):  # Ensure the link tag is found and has href
                link = link_tag['href']
                full_link = "https://www.lakai.com" + link  # Make link absolute
                
                # Write the link and current date to the CSV
                writer.writerow([full_link, datetime.now().strftime('%Y-%m-%d')])
            else:
                print("No link found for a product.")

    print("Product links scraped and saved to lakai_links.csv")
else:
    print("Failed to retrieve the webpage")
