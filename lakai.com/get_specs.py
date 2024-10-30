import requests
from bs4 import BeautifulSoup
import csv

# File containing product links
input_file = 'lakai_links.csv'
# Output file to save additional product data
output_file = 'lakai_product_data.csv'

# Open the input CSV file and read the links
with open(input_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header
    next(reader)

    # Open the output CSV file to write data
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write the header for additional data
        writer.writerow(['Product ID', 'Title', 'Price', 'Description'])

        # Loop through each link in the input file
        for row in reader:
            product_id, link = row  # Unpack product ID and link
            
            # Request the product page
            response = requests.get(link)
            if response.status_code == 200:
                # Parse the product page content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract product title from the correct div
                title = soup.find('div', class_='product-title').text.strip() if soup.find('div', class_='product-title') else 'N/A'
                
                # Extract product price from the correct div
                price = soup.find('div', class_='product-price current').text.strip() if soup.find('div', class_='product-price current') else 'N/A'
                
                # Extract product description from <p> under <div class='general-content'> under <div class='product-description-container'>
                description_container = soup.find('div', class_='product-description-container')
                description = (
                    description_container.find('div', class_='general-content').find('p').text.strip() 
                    if description_container and description_container.find('div', class_='general-content') and description_container.find('div', class_='general-content').find('p') 
                    else 'N/A'
                )

                # Log the extracted data
                print(f"Scraped data for Product ID: {product_id}")
                
                # Write the data to the output CSV
                writer.writerow([product_id, title, price, description])
            else:
                print(f"Failed to retrieve {link} (status code: {response.status_code})")

print("All product data scraped and saved to lakai_product_data.csv")
