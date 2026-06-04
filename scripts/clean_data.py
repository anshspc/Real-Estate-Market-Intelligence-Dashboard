import os
import pandas as pd
import numpy as np
from datetime import datetime

def clean_real_estate_data():
    raw_path = "/Users/babyshark/.gemini/antigravity/scratch/real-estate-market-intelligence-dashboard/data/raw_properties.csv"
    cleaned_path = "/Users/babyshark/.gemini/antigravity/scratch/real-estate-market-intelligence-dashboard/data/cleaned_properties.csv"
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run generate_raw_data.py first.")
        
    print(f"Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)
    initial_shape = df.shape
    print(f"Initial shape: {initial_shape}")
    
    # 1. Drop exact duplicates
    df = df.drop_duplicates()
    print(f"Shape after dropping duplicates: {df.shape} (Removed {initial_shape[0] - df.shape[0]} rows)")
    
    # 2. Clean City Names
    city_map = {
        'new york': 'New York', 'new york': 'New York', 'new york': 'New York', 'ny': 'New York', 'n.y.': 'New York',
        'san francisco': 'San Francisco', 'sf': 'San Francisco',
        'austin': 'Austin', 'atx': 'Austin',
        'chicago': 'Chicago', 'chi': 'Chicago',
        'miami': 'Miami', 'mia': 'Miami'
    }
    # Standardize string cleaning
    df['City'] = df['City'].astype(str).str.strip().str.lower()
    df['City'] = df['City'].replace(city_map)
    # Capitalize remaining unrecognized values just in case
    df['City'] = df['City'].str.title()
    
    # 3. Clean Property Types
    type_map = {
        'apartment': 'Apartment', 'apt': 'Apartment',
        'villa': 'Villa',
        'plot': 'Plot', 'land': 'Plot',
        'commercial': 'Commercial', 'office': 'Commercial'
    }
    df['Property_Type'] = df['Property_Type'].astype(str).str.strip().str.lower()
    df['Property_Type'] = df['Property_Type'].replace(type_map)
    df['Property_Type'] = df['Property_Type'].str.title()
    
    # 4. Clean Area_SqFt
    def clean_area(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).lower().replace('sqft', '').replace('sq ft', '').replace(',', '').strip()
        try:
            area_num = float(val_str)
            # Handle negative and zero values
            if area_num <= 0:
                return np.nan
            return area_num
        except ValueError:
            return np.nan
            
    df['Area_SqFt'] = df['Area_SqFt'].apply(clean_area)
    
    # Impute missing Area_SqFt using median of (City, Property_Type)
    area_medians = df.groupby(['City', 'Property_Type'])['Area_SqFt'].transform('median')
    df['Area_SqFt'] = df['Area_SqFt'].fillna(area_medians)
    # If still NaN (rare), impute with overall property type median
    type_area_medians = df.groupby('Property_Type')['Area_SqFt'].transform('median')
    df['Area_SqFt'] = df['Area_SqFt'].fillna(type_area_medians)
    
    # 5. Clean Price_USD
    def clean_price(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).lower().replace('$', '').replace('usd', '').replace(',', '').strip()
        if 'contact' in val_str or 'agent' in val_str:
            return np.nan
        try:
            return float(val_str)
        except ValueError:
            return np.nan
            
    df['Price_USD'] = df['Price_USD'].apply(clean_price)
    
    # Calculate price per sqft for imputation reference
    # Using existing valid price and area
    df['Temp_Price_Per_SqFt'] = df['Price_USD'] / df['Area_SqFt']
    
    # Find median Price_Per_SqFt by City, Property_Type, Locality
    median_price_per_sqft_group = df.groupby(['City', 'Property_Type', 'Locality'])['Temp_Price_Per_SqFt'].transform('median')
    # Backup groups
    median_price_per_sqft_city_type = df.groupby(['City', 'Property_Type'])['Temp_Price_Per_SqFt'].transform('median')
    median_price_per_sqft_type = df.groupby('Property_Type')['Temp_Price_Per_SqFt'].transform('median')
    
    # Impute price per sqft
    imputed_price_per_sqft = df['Temp_Price_Per_SqFt'].fillna(median_price_per_sqft_group)
    imputed_price_per_sqft = imputed_price_per_sqft.fillna(median_price_per_sqft_city_type)
    imputed_price_per_sqft = imputed_price_per_sqft.fillna(median_price_per_sqft_type)
    
    # Fill missing prices
    df['Price_USD'] = df['Price_USD'].fillna(df['Area_SqFt'] * imputed_price_per_sqft)
    
    # Drop temp column
    df = df.drop(columns=['Temp_Price_Per_SqFt'])
    
    # 6. Clean Bedrooms & Bathrooms
    # Plots do not have bedrooms/bathrooms
    df.loc[df['Property_Type'] == 'Plot', 'Bedrooms'] = 0
    df.loc[df['Property_Type'] == 'Plot', 'Bathrooms'] = 0
    
    # Commercial properties do not have bedrooms
    df.loc[df['Property_Type'] == 'Commercial', 'Bedrooms'] = 0
    
    # Impute missing bedrooms for Apartments/Villas
    bed_medians = df.groupby(['Property_Type', 'City'])['Bedrooms'].transform('median')
    df['Bedrooms'] = df['Bedrooms'].fillna(bed_medians)
    df['Bedrooms'] = df['Bedrooms'].fillna(2) # Default fallback
    df['Bedrooms'] = df['Bedrooms'].round().astype(int)
    
    # Impute missing bathrooms
    bath_medians = df.groupby(['Property_Type', 'City'])['Bathrooms'].transform('median')
    df['Bathrooms'] = df['Bathrooms'].fillna(bath_medians)
    df['Bathrooms'] = df['Bathrooms'].fillna(1) # Default fallback
    df['Bathrooms'] = df['Bathrooms'].round().astype(int)
    
    # 7. Clean Year_Built
    # Plots do not have Year_Built
    df.loc[df['Property_Type'] == 'Plot', 'Year_Built'] = np.nan
    
    # Impute missing Year_Built
    year_medians = df.groupby(['City', 'Locality'])['Year_Built'].transform('median')
    backup_year_medians = df.groupby('City')['Year_Built'].transform('median')
    df['Year_Built'] = df['Year_Built'].fillna(year_medians)
    df['Year_Built'] = df['Year_Built'].fillna(backup_year_medians)
    df['Year_Built'] = df['Year_Built'].fillna(1990) # Default fallback
    
    # For non-plots, convert to integer
    df.loc[df['Property_Type'] != 'Plot', 'Year_Built'] = df.loc[df['Property_Type'] != 'Plot', 'Year_Built'].round().astype(int)
    
    # 8. Clean Listing_Date
    def parse_date(val):
        if pd.isna(val):
            return pd.NaT
        val_str = str(val).strip()
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
            try:
                return pd.to_datetime(val_str, format=fmt)
            except ValueError:
                continue
        try:
            return pd.to_datetime(val_str)
        except ValueError:
            return pd.NaT
            
    df['Listing_Date'] = df['Listing_Date'].apply(parse_date)
    # Fill missing dates with median date
    if df['Listing_Date'].isnull().any():
        median_date = df['Listing_Date'].median()
        df['Listing_Date'] = df['Listing_Date'].fillna(median_date)
    df['Listing_Date'] = df['Listing_Date'].dt.strftime('%Y-%m-%d')
    
    # 9. Clean Rating and Scores
    df['Demand_Score'] = df['Demand_Score'].fillna(5).clip(1, 10).astype(int)
    
    rating_medians = df.groupby('City')['Customer_Rating'].transform('median')
    df['Customer_Rating'] = df['Customer_Rating'].fillna(rating_medians)
    df['Customer_Rating'] = df['Customer_Rating'].fillna(4.0).clip(1.0, 5.0).round(1)
    
    # 10. Outlier Removal using IQR on Price per SqFt per City/Type
    df['Price_Per_SqFt'] = df['Price_USD'] / df['Area_SqFt']
    
    cleaned_dfs = []
    for (city, p_type), group in df.groupby(['City', 'Property_Type']):
        if len(group) < 10:
            # Too small to compute IQR outliers, keep as is
            cleaned_dfs.append(group)
            continue
            
        q1 = group['Price_Per_SqFt'].quantile(0.25)
        q3 = group['Price_Per_SqFt'].quantile(0.75)
        iqr = q3 - q1
        
        # Define bounds (3 * IQR to catch extreme outliers, keeping normal premium properties)
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        
        # Filter outliers
        filtered_group = group[(group['Price_Per_SqFt'] >= lower_bound) & (group['Price_Per_SqFt'] <= upper_bound)]
        cleaned_dfs.append(filtered_group)
        
    df = pd.concat(cleaned_dfs).reset_index(drop=True)
    print(f"Shape after outlier removal: {df.shape} (Removed outliers)")
    
    # 11. Feature Engineering
    # Recalculate Price_Per_SqFt to ensure precision
    df['Price_Per_SqFt'] = (df['Price_USD'] / df['Area_SqFt']).round(2)
    df['Price_USD'] = df['Price_USD'].round(2)
    
    # Property Age
    current_year = 2026
    df['Property_Age'] = df['Year_Built'].apply(lambda x: current_year - x if not pd.isna(x) else np.nan)
    
    # Locality average price per sqft for Investment Score
    locality_avg = df.groupby(['City', 'Locality', 'Property_Type'])['Price_Per_SqFt'].transform('mean')
    # If a locality has only 1 property, it will match mean exactly, ratio is 1.0
    df['Locality_Price_Ratio'] = df['Price_Per_SqFt'] / locality_avg
    
    # Investment Opportunity Score (Scale: 1-10)
    # Higher demand is good (0.4 weight)
    # Higher customer rating is good (0.3 weight)
    # Lower price ratio than locality average is good (0.3 weight) -> cheaper than average is better value
    # Score = Demand_Score*0.4 + (Rating*2)*0.3 + (2 - Price_Ratio)*5*0.3
    # Cap between 1 and 10
    raw_score = (df['Demand_Score'] * 0.4) + \
                ((df['Customer_Rating'] * 2) * 0.3) + \
                ((2 - df['Locality_Price_Ratio']).clip(0, 2) * 5 * 0.3)
    df['Investment_Score'] = raw_score.clip(1, 10).round(1)
    
    # Drop temp column
    df = df.drop(columns=['Locality_Price_Ratio'])
    
    # Sort by property ID
    df = df.sort_values('Property_ID').reset_index(drop=True)
    
    # Save output
    df.to_csv(cleaned_path, index=False)
    print(f"Successfully cleaned and saved dataset to: {cleaned_path}")
    print(f"Final dataset shape: {df.shape}")
    print(df.head(2))

if __name__ == "__main__":
    clean_real_estate_data()
