import pandas as pd
import os
from datetime import datetime

df = pd.read_csv(r"C:\Users\USER\python\car-price-prediction\result\all_cars.csv")

df['price_clean'] = df['price'].str.replace(r'[^\d]', '', regex=True)
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

if 'year' not in df.columns:
    df['year'] = df['title'].str.extract(r'(\d{4})')[0]

current_year = datetime.now().year
df['age'] = current_year - pd.to_numeric(df['year'])

os.makedirs('processed_data', exist_ok=True)
df.to_csv('processed_data/cleaned_cars.csv', index=False)
print("Data cleaned and saved!")

