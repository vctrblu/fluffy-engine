import csv
import requests
from bs4 import BeautifulSoup

# Input file containing the product links
input_file = './deus_product_links.csv'
# Output file to save the scraped data
output_file = './deus_product_data.csv'

# Function to scrape data from a single product link
def scrape_product_data(product_link):
    response = requests.get(product_link)
    if response.status_code != 200:
        print(f"Failed to retrieve {product_link} (status code: {response.status_code})")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the product title
    title_div = soup.find('h1', class_='h2 product__title')
    title = title_div.text.strip() if title_div else 'N/A'
    
    # Extract the product price
    price_span = soup.find('span', class_='product__price')
    price = price_span.text.strip() if price_span else 'N/A'
    
    # Extract the product description
    description_div = soup.find('div', class_='product__description rte')
    description_paragraphs = description_div.find_all('p') if description_div else []
    description = ' '.join([p.text.strip() for p in description_paragraphs]) if description_paragraphs else 'N/A'
    
    return {
        'Link': product_link,
        'Title': title,
        'Price': price,
        'Description': description
    }

# Initialize a list to hold all product data
all_product_data = []

# Read the product links from the input CSV file
with open(input_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_link = row['Product Link']
        print(f"Scraping data from {product_link}")
        product_data = scrape_product_data(product_link)
        if product_data:
            all_product_data.append(product_data)

# Save the scraped product data to a new CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Link', 'Title', 'Price', 'Description']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row
    for data in all_product_data:
        writer.writerow(data)

print(f"Scraped data for {len(all_product_data)} products and saved to {output_file}")
