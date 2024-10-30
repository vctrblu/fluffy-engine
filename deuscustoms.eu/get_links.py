import requests
from bs4 import BeautifulSoup
import csv
import re  # Import the regular expression module

# Base URL with a placeholder for the page number
base_url = 'https://deuscustoms.eu/collections/all?page={}'

# Output file to save product links (will be saved in the same folder as the script)
output_file = './deus_product_links.csv'  # ./ indicates the current directory

# Function to get the total number of pages from the pagination
def get_total_pages():
    response = requests.get(base_url.format(1))  # Start with page 1
    if response.status_code != 200:
        print(f"Failed to retrieve page 1 (status code: {response.status_code})")
        return 1  # Default to 1 page if we can't determine total pages

    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ol', class_='pagination')
    
    if pagination:
        # Get the second-to-last <li> in the pagination, which contains the last page number
        page_items = pagination.find_all('li')
        if len(page_items) > 1:
            max_page_text = page_items[-2].text.strip()  # Get the number from the second-to-last item
            
            # Extract only the number using regex
            max_page_match = re.search(r'\d+', max_page_text)
            if max_page_match:
                return int(max_page_match.group(0))
    return 1  # Default to 1 page if pagination is not found

# Get the total number of pages
total_pages = get_total_pages()
print(f"Total pages to scrape: {total_pages}")

# Initialize an empty list to store all product links
all_product_links = []

# Loop through each page up to the maximum page number
for page_number in range(1, total_pages + 1):
    url = base_url.format(page_number)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve {url} (status code: {response.status_code})")
        break
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <li class="results-grid__tile"> elements
    product_links = []
    for li in soup.find_all('li', class_='results-grid__tile'):
        product_card = li.find('div', class_='product-card__image')
        if product_card:
            a_tag = product_card.find('a', href=True)
            if a_tag:
                href = a_tag['href']
                # Append the full URL if it’s a relative link
                full_url = f"https://deuscustoms.eu{href}" if href.startswith('/') else href
                product_links.append(full_url)
    
    # Add the current page's product links to the main list
    all_product_links.extend(product_links)
    print(f"Scraped {len(product_links)} links from page {page_number}")

# Save all product links to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Link'])  # Header row
    for link in all_product_links:
        writer.writerow([link])

print(f"Scraped a total of {len(all_product_links)} product links across {total_pages} pages and saved to {output_file}")
