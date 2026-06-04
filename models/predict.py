import os
import sys
import argparse
import pandas as pd
import joblib

def main():
    parser = argparse.ArgumentParser(description="Predict property prices using the trained Real Estate ML Pipeline.")
    
    # Required inputs
    parser.add_argument("--city", type=str, required=True, 
                        choices=["New York", "San Francisco", "Austin", "Chicago", "Miami"],
                        help="City where the property is located")
    parser.add_argument("--type", type=str, required=True, 
                        choices=["Apartment", "Villa", "Plot", "Commercial"],
                        help="Property type")
    parser.add_argument("--area", type=float, required=True, help="Property area in square feet")
    
    # Optional inputs (with intelligent defaults or validations based on type)
    parser.add_argument("--bedrooms", type=int, default=None, help="Number of bedrooms (defaults to 0 for Plot/Commercial)")
    parser.add_argument("--bathrooms", type=int, default=None, help="Number of bathrooms (defaults to 0 for Plot)")
    parser.add_argument("--age", type=float, default=10.0, help="Age of the property in years (defaults to 10)")
    parser.add_argument("--demand", type=int, default=5, choices=range(1, 11), help="Demand score from 1-10 (default: 5)")
    parser.add_argument("--rating", type=float, default=4.0, help="Customer rating from 1-5 (default: 4.0)")
    
    args = parser.parse_args()
    
    # Validation / defaults matching clean_data pipeline
    bedrooms = args.bedrooms
    bathrooms = args.bathrooms
    
    if args.type == "Plot":
        bedrooms = 0
        bathrooms = 0
        age = 0.0
    elif args.type == "Commercial":
        bedrooms = 0
        if bathrooms is None:
            bathrooms = 2
        age = args.age
    else: # Apartment / Villa
        if bedrooms is None:
            bedrooms = 3 if args.type == "Villa" else 2
        if bathrooms is None:
            bathrooms = 2
        age = args.age
        
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "price_predictor.joblib")
    
    if not os.path.exists(model_path):
        print(f"Error: Trained model file not found at '{model_path}'.", file=sys.stderr)
        print("Please run the notebook 'notebooks/02_price_prediction_model.ipynb' to train and save the model.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Loading trained prediction model from: {model_path}")
    try:
        model_data = joblib.load(model_path)
        # Check if it is a dictionary or direct model
        if isinstance(model_data, dict):
            model = model_data.get('model')
            feature_cols = model_data.get('features')
            print(f"Successfully loaded model. R2 Score on Validation set: {model_data.get('val_r2', 'N/A')}")
        else:
            model = model_data
            feature_cols = None
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Construct input dataframe
    # Features used: 'City', 'Property_Type', 'Area_SqFt', 'Bedrooms', 'Bathrooms', 'Property_Age', 'Demand_Score', 'Customer_Rating'
    input_data = pd.DataFrame([{
        'City': args.city,
        'Property_Type': args.type,
        'Area_SqFt': args.area,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Property_Age': age,
        'Demand_Score': args.demand,
        'Customer_Rating': args.rating
    }])
    
    print("\nProperty Features:")
    print(f"  - City: {args.city}")
    print(f"  - Locality / Type: {args.type}")
    print(f"  - Size: {args.area:,.2f} sqft")
    print(f"  - Bedrooms / Bathrooms: {bedrooms} / {bathrooms}")
    print(f"  - Age: {age} years")
    print(f"  - Market Demand Score: {args.demand}/10")
    print(f"  - Customer Rating: {args.rating}/5.0")
    
    # Predict
    try:
        predicted_price = model.predict(input_data)[0]
        price_per_sqft = predicted_price / args.area
        
        print("\n" + "="*40)
        print(f"PREDICTED VALUATION: ${predicted_price:,.2f}")
        print(f"Estimated Price/SqFt: ${price_per_sqft:,.2f}/sqft")
        print("="*40)
    except Exception as e:
        print(f"Prediction failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
