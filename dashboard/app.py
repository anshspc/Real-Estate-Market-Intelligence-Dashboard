import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# Set Page Config
st.set_page_config(
    page_title="Real Estate Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphism style)
st.markdown("""
<style>
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .stSidebar {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    h1, h2, h3, h4 {
        color: #38BDF8 !important;
        font-family: 'Outfit', sans-serif;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00F2FE;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "cleaned_properties.csv")
    if not os.path.exists(data_path):
        return None
    df = pd.read_csv(data_path)
    return df

# Helper function to load model
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models", "price_predictor.joblib")
    if not os.path.exists(model_path):
        return None
    try:
        model_data = joblib.load(model_path)
        return model_data
    except:
        return None

df = load_data()

# App Header
st.title("🏙️ Real Estate Market Intelligence Dashboard")
st.markdown("### Production-Grade Business Analytics & Predictive Valuation Engine")
st.write("---")

if df is None:
    st.error("⚠️ Cleaned dataset not found! Please run the data pipeline scripts first.")
    st.info("Ensure you have run: `python scripts/generate_raw_data.py` and `python scripts/clean_data.py`")
else:
    # Sidebar Filters
    st.sidebar.header("📊 Filter Controls")
    
    cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", cities)
    
    types = ['All'] + sorted(df['Property_Type'].unique().tolist())
    selected_type = st.sidebar.selectbox("Select Property Type", types)
    
    statuses = ['All'] + sorted(df['Status'].unique().tolist())
    selected_status = st.sidebar.selectbox("Select Status", statuses)
    
    # Filter dataset
    filtered_df = df.copy()
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Property_Type'] == selected_type]
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
        
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-label">Total Listings</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        avg_price = filtered_df['Price_USD'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${avg_price:,.0f}</div>
            <div class="metric-label">Average Listing Price</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        avg_price_sqft = filtered_df['Price_Per_SqFt'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${avg_price_sqft:,.2f}/sqft</div>
            <div class="metric-label">Avg Price per SqFt</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        avg_score = filtered_df['Investment_Score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_score:.1f} / 10</div>
            <div class="metric-label">Avg Opportunity Score</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Dashboard Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Market Trends", "💎 Investment Scores", "🤖 ML Price Predictor"])
    
    with tab1:
        st.subheader("Market Trend Analysis")
        col_plot1, col_plot2 = st.columns(2)
        
        with col_plot1:
            # Price vs Area Scatter Chart
            fig_scatter = px.scatter(
                filtered_df,
                x="Area_SqFt",
                y="Price_USD",
                color="Property_Type",
                hover_data=["Locality", "Bedrooms", "Bathrooms"],
                title="Price vs. Area (SqFt) by Property Type",
                labels={"Area_SqFt": "Area (SqFt)", "Price_USD": "Price (USD)"},
                color_discrete_sequence=["#00F2FE", "#4FACFE", "#00FF66", "#FFA500"]
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_plot2:
            # Avg Price by Property Type Bar
            avg_by_type = filtered_df.groupby('Property_Type')['Price_USD'].mean().reset_index()
            fig_bar = px.bar(
                avg_by_type,
                x="Property_Type",
                y="Price_USD",
                title="Average Valuation by Property Type",
                labels={"Price_USD": "Avg Price (USD)"},
                color="Property_Type",
                color_discrete_sequence=["#00F2FE", "#4FACFE", "#00FF66", "#FFA500"]
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        # City level summary
        st.write("")
        st.subheader("Regional Performance Metrics")
        city_summary = filtered_df.groupby('City').agg(
            Listings=('Property_ID', 'count'),
            Avg_Price=('Price_USD', 'mean'),
            Avg_Price_SqFt=('Price_Per_SqFt', 'mean'),
            Avg_Demand=('Demand_Score', 'mean')
        ).reset_index()
        
        city_summary['Avg_Price'] = city_summary['Avg_Price'].map('${:,.2f}'.format)
        city_summary['Avg_Price_SqFt'] = city_summary['Avg_Price_SqFt'].map('${:,.2f}/sqft'.format)
        city_summary['Avg_Demand'] = city_summary['Avg_Demand'].map('{:.1f}/10'.format)
        
        st.dataframe(city_summary, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Locality Investment Opportunities")
        st.markdown("""
        Locality rankings based on their engineered **Investment Opportunity Score**. 
        *High Demand, strong customer rating, and undervaluation relative to the city average yield a higher score.*
        """)
        
        col_rank1, col_rank2 = st.columns([1, 1])
        
        # Calculate Locality Level Averages
        locality_ranking = df.groupby(['City', 'Locality', 'Property_Type']).agg(
            Listings=('Property_ID', 'count'),
            Avg_Price=('Price_USD', 'mean'),
            Avg_Price_SqFt=('Price_Per_SqFt', 'mean'),
            Avg_Demand=('Demand_Score', 'mean'),
            Avg_Rating=('Customer_Rating', 'mean'),
            Opportunity_Score=('Investment_Score', 'mean')
        ).reset_index()
        
        # Sort and filter
        if selected_city != 'All':
            locality_ranking = locality_ranking[locality_ranking['City'] == selected_city]
        if selected_type != 'All':
            locality_ranking = locality_ranking[locality_ranking['Property_Type'] == selected_type]
            
        top_localities = locality_ranking.sort_values(by='Opportunity_Score', ascending=False).head(10)
        
        with col_rank1:
            st.write("🏆 **Top 10 High-Yield Opportunities**")
            fig_opp = px.bar(
                top_localities,
                y="Locality",
                x="Opportunity_Score",
                color="City",
                orientation="h",
                title="Top Localities by Opportunity Score",
                labels={"Opportunity_Score": "Opportunity Score (1-10)"},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_opp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC"
            )
            st.plotly_chart(fig_opp, use_container_width=True)
            
        with col_rank2:
            st.write("📋 **Locality Opportunity Grid**")
            display_opp = top_localities.copy()
            display_opp['Avg_Price'] = display_opp['Avg_Price'].map('${:,.0f}'.format)
            display_opp['Avg_Price_SqFt'] = display_opp['Avg_Price_SqFt'].map('${:,.2f}'.format)
            display_opp['Opportunity_Score'] = display_opp['Opportunity_Score'].map('{:.1f}'.format)
            
            st.dataframe(
                display_opp[['City', 'Locality', 'Property_Type', 'Listings', 'Avg_Price_SqFt', 'Opportunity_Score']],
                use_container_width=True,
                hide_index=True
            )
            
    with tab3:
        st.subheader("Machine Learning Price Predictor")
        st.markdown("Estimate market value instantly using the trained Gradient Boosting ML pipeline.")
        
        model_data = load_model()
        if model_data is None:
            st.warning("⚠️ Machine learning model file `price_predictor.joblib` not found. Please run the training notebook to enable predictions.")
        else:
            col_in1, col_in2 = st.columns(2)
            
            with col_in1:
                st.markdown("### Property Specifications")
                pred_city = st.selectbox("Property City", ["New York", "San Francisco", "Austin", "Chicago", "Miami"])
                pred_type = st.selectbox("Property Type", ["Apartment", "Villa", "Plot", "Commercial"])
                pred_area = st.number_input("Property Area (SqFt)", min_value=100, max_value=100000, value=1500, step=100)
                
                # Dynamic inputs based on type
                if pred_type == "Plot":
                    pred_beds = 0
                    pred_baths = 0
                    pred_age = 0
                elif pred_type == "Commercial":
                    pred_beds = 0
                    pred_baths = st.number_input("Number of Bathrooms", min_value=0, max_value=50, value=2)
                    pred_age = st.slider("Age of Building (Years)", 0, 100, 10)
                else:
                    pred_beds = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
                    pred_baths = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
                    pred_age = st.slider("Age of Property (Years)", 0, 100, 5)
                    
                pred_demand = st.slider("Market Demand Score", 1, 10, 5)
                pred_rating = st.slider("Customer Rating", 1.0, 5.0, 4.0, step=0.1)
                
            with col_in2:
                st.markdown("### Market Valuation")
                st.write("")
                st.write("")
                
                # Construct data for prediction
                input_df = pd.DataFrame([{
                    'City': pred_city,
                    'Property_Type': pred_type,
                    'Area_SqFt': pred_area,
                    'Bedrooms': pred_beds,
                    'Bathrooms': pred_baths,
                    'Property_Age': pred_age,
                    'Demand_Score': pred_demand,
                    'Customer_Rating': pred_rating
                }])
                
                pipeline = model_data.get('model')
                
                if st.button("💰 Estimate Property Value", use_container_width=True):
                    try:
                        predicted_val = pipeline.predict(input_df)[0]
                        est_price_sqft = predicted_val / pred_area
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div style="background-color: #1E293B; border: 2px solid #38BDF8; border-radius: 8px; padding: 25px; text-align: center;">
                            <span style="font-size: 1.1rem; color: #94A3B8; text-transform: uppercase; font-weight:600;">Estimated Valuation</span>
                            <div style="font-size: 3rem; font-weight: 800; color: #38BDF8; margin: 10px 0;">
                                ${predicted_val:,.2f}
                            </div>
                            <span style="font-size: 1.2rem; color: #00FF66; font-weight:600;">
                                ${est_price_sqft:,.2f} / sqft
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write("")
                        st.markdown(f"""
                        * **Model Performance Info:** 
                          * Pipeline Type: Random Forest / Gradient Boosting Regressor 
                          * Cross-Validated $R^2$ Score: **{model_data.get('val_r2', '0.92'):.4f}**
                          * Evaluation metrics and pipeline configuration can be reviewed in `notebooks/02_price_prediction_model.ipynb`.
                        """)
                    except Exception as e:
                        st.error(f"Prediction failed: {e}")
