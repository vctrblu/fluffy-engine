import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the collection page
base_url = "https://www.lakai.com/collections/shoes?page={}"

# Open a CSV file to write data
with open('lakai_links.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header if the file is empty
    if csvfile.tell() == 0:
        writer.writerow(['Product ID', 'Link'])  # Header for product ID and link

    page_number = 1  # Start from the first page
    while True:
        # Construct the URL for the current page
        url = base_url.format(page_number)
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Exiting.")
            break  # Exit loop if no more pages are found

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the product grid items
        product_list = soup.find('ul', class_='products-grid-items')
        products = product_list.find_all('li')  # Each product is in an <li> tag

        # Log the number of <li> elements found
        print(f"Found {len(products)} products on page {page_number}.")

        # If no products are found, break the loop
        if len(products) == 0:
            print(f"No more products found on page {page_number}. Exiting.")
            break

        # Extract all product links and IDs
        for product in products:
            # Get the product ID
            product_id = product.get('data-product-id')
            print(f"Processing Product ID: {product_id}")  # Log the product ID
            
            # Find all <a> tags within the product item
            link_tags = product.find_all('a')

            # Extract href from each <a> tag
            for link_tag in link_tags:
                href = link_tag.get('href')
                if href:  # Ensure the href attribute is not None
                    full_link = "https://www.lakai.com" + href  # Make link absolute
                    
                    # Write the product ID and link to the CSV
                    writer.writerow([product_id, full_link])

        print(f"Scraped page {page_number} successfully.")
        page_number += 1  # Move to the next page

print("All product links and IDs scraped and saved to lakai_links.csv")
