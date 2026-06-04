import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_messy_data(num_records=3500):
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    cities = {
        'New York': ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'],
        'San Francisco': ['Mission District', 'SOMA', 'Pacific Heights', 'Marina'],
        'Austin': ['Downtown', 'South Austin', 'East Austin', 'West Lake Hills'],
        'Chicago': ['Loop', 'Lincoln Park', 'Hyde Park', 'River North'],
        'Miami': ['South Beach', 'Brickell', 'Coral Gables', 'Little Havana']
    }
    
    prop_types = ['Apartment', 'Villa', 'Plot', 'Commercial']
    statuses = ['Active', 'Pending', 'Sold']
    
    # Text noise for city names to show cleaning skills
    city_variants = {
        'New York': ['New York', 'new york', 'NEW YORK', 'NY', 'N.Y.'],
        'San Francisco': ['San Francisco', 'san francisco', 'SAN FRANCISCO', 'SF'],
        'Austin': ['Austin', 'austin', 'AUSTIN', 'ATX'],
        'Chicago': ['Chicago', 'chicago', 'CHICAGO', 'CHI'],
        'Miami': ['Miami', 'miami', 'MIAMI', 'MIA']
    }
    
    # Text noise for property types
    type_variants = {
        'Apartment': ['Apartment', 'apartment', 'APT', 'Apt'],
        'Villa': ['Villa', 'villa', 'VILLA'],
        'Plot': ['Plot', 'plot', 'Land', 'land'],
        'Commercial': ['Commercial', 'commercial', 'COMMERCIAL', 'Office']
    }
    
    data = []
    
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        prop_id = f"PROP-{10000 + i}"
        
        # Select city and locality
        city = random.choice(list(cities.keys()))
        locality = random.choice(cities[city])
        
        # Choose noise variant for city
        city_name = random.choice(city_variants[city])
        
        # Property type and its variant
        p_type = random.choice(prop_types)
        prop_type_val = random.choice(type_variants[p_type])
        
        # Base price calculation based on city and type
        base_price_sqft = {
            'New York': 1200,
            'San Francisco': 1400,
            'Austin': 450,
            'Chicago': 350,
            'Miami': 600
        }[city]
        
        # Scale price based on locality
        locality_scale = 1.0
        if locality in ['Manhattan', 'Pacific Heights', 'West Lake Hills', 'Lincoln Park', 'Coral Gables']:
            locality_scale = 1.5
        elif locality in ['Bronx', 'Marina', 'East Austin', 'Hyde Park', 'Little Havana']:
            locality_scale = 0.8
            
        # Determine Area
        if p_type == 'Apartment':
            area = random.randint(500, 2500)
            bedrooms = random.randint(1, 4)
            bathrooms = random.randint(1, 3)
            year_built = random.randint(1920, 2023)
        elif p_type == 'Villa':
            area = random.randint(1800, 6000)
            bedrooms = random.randint(3, 6)
            bathrooms = random.randint(2, 5)
            year_built = random.randint(1980, 2024)
        elif p_type == 'Plot':
            area = random.randint(1000, 10000)
            bedrooms = np.nan # Land has no bedrooms
            bathrooms = np.nan
            year_built = np.nan
        else: # Commercial
            area = random.randint(1000, 25000)
            bedrooms = np.nan
            bathrooms = random.randint(2, 10)
            year_built = random.randint(1960, 2022)
            
        # Calculate price with some randomness
        price = area * base_price_sqft * locality_scale * random.uniform(0.85, 1.15)
        
        # Create descriptive title
        if p_type == 'Plot':
            title = f"Residential plot of {area} sqft in {locality}"
        elif p_type == 'Commercial':
            title = f"Commercial Space / Office in {locality}"
        else:
            title = f"{int(bedrooms) if not np.isnan(bedrooms) else 2} BHK {p_type} for sale in {locality}"
            
        # Format Listing Date (with some bad formats)
        days_offset = random.randint(0, 700)
        list_dt = start_date + timedelta(days=days_offset)
        
        date_format_choice = random.random()
        if date_format_choice < 0.8:
            date_str = list_dt.strftime('%Y-%m-%d')
        elif date_format_choice < 0.9:
            date_str = list_dt.strftime('%d/%m/%Y')
        else:
            date_str = list_dt.strftime('%Y/%m/%d')
            
        status = random.choice(statuses)
        demand_score = random.randint(1, 10)
        # SOMA / Manhattan might have higher demand
        if locality in ['Manhattan', 'SOMA', 'South Beach', 'Downtown']:
            demand_score = min(10, demand_score + 2)
            
        customer_rating = round(random.uniform(3.0, 5.0), 1)
        if demand_score > 8:
            customer_rating = round(random.uniform(4.0, 5.0), 1)
            
        # Mess up some prices to demonstrate cleaning
        price_val = price
        mess_price_choice = random.random()
        if mess_price_choice < 0.05: # Formatting issue
            price_val = f"${int(price):,}"
        elif mess_price_choice < 0.08: # String issue with text
            price_val = f"{int(price)} USD"
        elif mess_price_choice < 0.10: # Missing value
            price_val = np.nan
        elif mess_price_choice < 0.11: # Missing value string
            price_val = "Contact Agent"
            
        # Mess up area
        mess_area_choice = random.random()
        if mess_area_choice < 0.04:
            area_val = f"{area} sqft"
        elif mess_area_choice < 0.06:
            area_val = f"{area} SQFT"
        elif mess_area_choice < 0.07: # Negative value
            area_val = -area
        elif mess_area_choice < 0.08: # Zero area
            area_val = 0
        else:
            area_val = area
            
        # Inject other missing values
        if not np.isnan(bedrooms) and random.random() < 0.04:
            bedrooms = np.nan
            
        if not np.isnan(year_built) and random.random() < 0.05:
            year_built = np.nan
            
        # Inject rating missing values
        rating_val = customer_rating
        if random.random() < 0.05:
            rating_val = np.nan
            
        row = {
            'Property_ID': prop_id,
            'Title': title,
            'City': city_name,
            'Locality': locality,
            'Property_Type': prop_type_val,
            'Price_USD': price_val,
            'Area_SqFt': area_val,
            'Bedrooms': bedrooms,
            'Bathrooms': bathrooms,
            'Year_Built': year_built,
            'Listing_Date': date_str,
            'Status': status,
            'Demand_Score': demand_score,
            'Customer_Rating': rating_val
        }
        
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Introduce duplicates (around 2%)
    dup_indices = np.random.choice(df.index, size=int(num_records * 0.02), replace=False)
    df_dups = df.iloc[dup_indices].copy()
    
    # Concat and shuffle
    df = pd.concat([df, df_dups], ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Introduce extreme price outliers (0.2%)
    outlier_indices = np.random.choice(df.index, size=int(num_records * 0.002), replace=False)
    for idx in outlier_indices:
        df.at[idx, 'Price_USD'] = df.at[idx, 'Price_USD'] * 15 # Outlier: way too expensive
        
    return df

if __name__ == "__main__":
    print("Generating raw real estate dataset...")
    df = generate_messy_data(3500)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "raw_properties.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated raw dataset: {output_path} (Shape: {df.shape})")
