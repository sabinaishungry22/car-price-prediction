import os
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

link = 'https://www.carmudi.co.id/mobil-dijual/indonesia?'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_year(title):
    """Extracts year from title (e.g., '2022 Toyota...')"""
    match = re.search(r'\b(20\d{2})\b', title)
    return match.group(1) if match else 'N/A'

def scrape_pages(pages=5):
    all_data = []
    
    for page in range(1, pages+1):
        print(f"Scraping page {page}...")
        params = {'page_number': page, 'page_size': 50}
        
        try:
            req = requests.get(link, params=params, headers=headers, timeout=10)
            req.raise_for_status()
            soup = BeautifulSoup(req.text, 'html.parser')
            
            for item in soup.find_all('div', 'flex flex--row flex--wrap'):
                try:
                    title_element = item.find('a', 'ellipsize js-ellipsize-text')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    year = extract_year(title)
                    
                    price_element = item.find('div', 'listing__price delta weight--bold')
                    price = price_element.text.strip() if price_element else 'Price not available'

                    all_data.append({
                        'title': title,
                        'year': year,
                        'price': price
                    })
                    
                except Exception as e:
                    print(f"Error processing item on page {page}: {e}")
                    continue
                    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Clean price column
    df['price_clean'] = df['price'].str.replace(r'[^\d]', '', regex=True)
    df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')
    
    # Save to single CSV
    os.makedirs('result', exist_ok=True)
    df.to_csv('result/all_cars.csv', index=False)
    print(f"\nSuccess! Saved {len(df)} cars to result/all_cars.csv")

if __name__ == '__main__':
    scrape_pages(pages=5)  # Change this number if needed