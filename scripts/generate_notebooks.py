import os
import json

def create_notebooks():
    nb_dir = "/Users/babyshark/.gemini/antigravity/scratch/real-estate-market-intelligence-dashboard/notebooks"
    os.makedirs(nb_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # Notebook 1: Exploratory Data Analysis
    # -------------------------------------------------------------
    eda_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 01. Exploratory Data Analysis - Real Estate Market Trends\n",
                "**Real Estate Market Intelligence Dashboard**\n",
                "\n",
                "This notebook performs comprehensive Exploratory Data Analysis (EDA) on the cleaned properties dataset to extract actionable insights for executives and investors. We analyze price distributions, regional variations, feature correlations, and formulate the **Investment Opportunity Score**."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "# Set plot styling for a professional look\n",
                "sns.set_theme(style=\"whitegrid\")\n",
                "plt.rcParams[\"figure.figsize\"] = (12, 6)\n",
                "plt.rcParams[\"axes.titlesize\"] = 14\n",
                "plt.rcParams[\"axes.labelsize\"] = 12"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 1. Load Cleaned Dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "data_path = \"../data/cleaned_properties.csv\"\n",
                "df = pd.read_csv(data_path)\n",
                "print(f\"Loaded dataset with {df.shape[0]} listings and {df.shape[1]} features.\")\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2. General Data Overview"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df.info()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df.describe().T"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 3. Price Analysis by City & Property Type"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Distribution of Price per SqFt across different Cities\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.boxplot(data=df, x='City', y='Price_Per_SqFt', palette='viridis')\n",
                "plt.title('Property Valuation (Price per SqFt) distribution by City')\n",
                "plt.ylabel('Price per SqFt (USD)')\n",
                "plt.xlabel('City')\n",
                "plt.tight_layout()\n",
                "os.makedirs('../screenshots', exist_ok=True)\n",
                "plt.savefig('../screenshots/price_per_sqft_by_city.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Price distribution by Property Type\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.barplot(data=df, x='Property_Type', y='Price_USD', hue='City', estimator=np.median, palette='muted')\n",
                "plt.title('Median Listing Price by Property Type and City')\n",
                "plt.ylabel('Median Price USD (Log Scale)')\n",
                "plt.yscale('log')\n",
                "plt.xlabel('Property Type')\n",
                "plt.tight_layout()\n",
                "plt.savefig('../screenshots/median_price_by_type.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 4. Correlation Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Compute correlation matrix for numeric columns\n",
                "numeric_cols = ['Price_USD', 'Area_SqFt', 'Bedrooms', 'Bathrooms', 'Year_Built', 'Demand_Score', 'Customer_Rating', 'Property_Age', 'Investment_Score']\n",
                "corr_matrix = df[numeric_cols].corr()\n",
                "\n",
                "plt.figure(figsize=(10, 8))\n",
                "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, vmin=-1, vmax=1)\n",
                "plt.title('Correlation Heatmap of Real Estate Features')\n",
                "plt.tight_layout()\n",
                "plt.savefig('../screenshots/eda_correlation.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5. Deep Dive into Investment Opportunity Scores"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Show top 5 localities for each city with highest investment opportunities\n",
                "top_localities = df.groupby(['City', 'Locality'])['Investment_Score'].mean().reset_index()\n",
                "top_localities = top_localities.sort_values(by='Investment_Score', ascending=False)\n",
                "print(\"Top 10 overall localities with highest Investment Scores:\")\n",
                "print(top_localities.head(10).to_string(index=False))"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Visualizing Investment Scores by Property Type\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.violinplot(data=df, x='Property_Type', y='Investment_Score', inner='quartile', palette='Set2')\n",
                "plt.title('Distribution of Investment Scores by Property Type')\n",
                "plt.ylabel('Investment Score (1-10)')\n",
                "plt.xlabel('Property Type')\n",
                "plt.tight_layout()\n",
                "plt.savefig('../screenshots/investment_scores_by_type.png', dpi=300)\n",
                "plt.show()"
            ]
        }
    ]
    
    eda_nb = {
        "cells": eda_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(os.path.join(nb_dir, "01_eda_market_trends.ipynb"), "w") as f:
        json.dump(eda_nb, f, indent=1)
        
    # -------------------------------------------------------------
    # Notebook 2: Machine Learning Model
    # -------------------------------------------------------------
    ml_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 02. Machine Learning - Real Estate Price Prediction\n",
                "**Real Estate Market Intelligence Dashboard**\n",
                "\n",
                "This notebook focuses on training and validating a machine learning pipeline to predict listing prices based on geographic, physical, and market indicators. We compare multiple models, tune hyperparameters, and export a production-ready model pipeline."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.model_selection import train_test_split, GridSearchCV\n",
                "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n",
                "from sklearn.compose import ColumnTransformer\n",
                "from sklearn.pipeline import Pipeline\n",
                "from sklearn.linear_model import LinearRegression\n",
                "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n",
                "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n",
                "import joblib"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 1. Load Cleaned Dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = pd.read_csv(\"../data/cleaned_properties.csv\")\n",
                "# Split features and target\n",
                "# Target is listing price (Price_USD)\n",
                "features = ['City', 'Property_Type', 'Area_SqFt', 'Bedrooms', 'Bathrooms', 'Property_Age', 'Demand_Score', 'Customer_Rating']\n",
                "target = 'Price_USD'\n",
                "\n",
                "X = df[features]\n",
                "y = df[target]\n",
                "\n",
                "print(f\"X shape: {X.shape}, y shape: {y.shape}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2. Preprocessing & Feature Engineering Pipeline"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Define columns categories\n",
                "categorical_cols = ['City', 'Property_Type']\n",
                "numeric_cols = ['Area_SqFt', 'Bedrooms', 'Bathrooms', 'Property_Age', 'Demand_Score', 'Customer_Rating']\n",
                "\n",
                "# Create ColumnTransformer to scale numeric and one-hot encode categorical features\n",
                "preprocessor = ColumnTransformer(\n",
                "    transformers=[\n",
                "        ('num', StandardScaler(), numeric_cols),\n",
                "        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)\n",
                "    ]\n",
                ")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 3. Split Dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
                "print(f\"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 4. Train and Compare Regression Models"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "models = {\n",
                "    'Linear Regression': LinearRegression(),\n",
                "    'Random Forest': RandomForestRegressor(random_state=42),\n",
                "    'Gradient Boosting': GradientBoostingRegressor(random_state=42)\n",
                "}\n",
                "\n",
                "results = {}\n",
                "for name, model in models.items():\n",
                "    # Create complete ML pipeline\n",
                "    pipeline = Pipeline(steps=[\n",
                "        ('preprocessor', preprocessor),\n",
                "        ('regressor', model)\n",
                "    ])\n",
                "    \n",
                "    # Fit model\n",
                "    pipeline.fit(X_train, y_train)\n",
                "    \n",
                "    # Predict\n",
                "    y_pred = pipeline.predict(X_test)\n",
                "    \n",
                "    # Evaluate\n",
                "    mae = mean_absolute_error(y_test, y_pred)\n",
                "    rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n",
                "    r2 = r2_score(y_test, y_pred)\n",
                "    \n",
                "    results[name] = {'pipeline': pipeline, 'MAE': mae, 'RMSE': rmse, 'R2': r2}\n",
                "    print(f\"=== {name} ===\")\n",
                "    print(f\"MAE:  ${mae:,.2f}\")\n",
                "    print(f\"RMSE: ${rmse:,.2f}\")\n",
                "    print(f\"R2:   {r2:.4f}\\n\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5. Tuning Best Model (Random Forest Hyperparameter Tuning)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Hyperparameter tuning for Random Forest using Grid Search\n",
                "rf_pipeline = Pipeline(steps=[\n",
                "    ('preprocessor', preprocessor),\n",
                "    ('regressor', RandomForestRegressor(random_state=42))\n",
                "    ])\n",
                "\n",
                "param_grid = {\n",
                "    'regressor__n_estimators': [50, 100, 150],\n",
                "    'regressor__max_depth': [None, 10, 20],\n",
                "    'regressor__min_samples_split': [2, 5]\n",
                "}\n",
                "\n",
                "print(\"Tuning Random Forest Regressor...\")\n",
                "grid_search = GridSearchCV(rf_pipeline, param_grid, cv=3, scoring='r2', verbose=1)\n",
                "grid_search.fit(X_train, y_train)\n",
                "\n",
                "best_pipeline = grid_search.best_estimator_\n",
                "best_r2 = grid_search.best_score_\n",
                "\n",
                "print(f\"Best CV R2 Score: {best_r2:.4f}\")\n",
                "print(f\"Best Parameters: {grid_search.best_params_}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 6. Evaluate Tuned Model"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Final evaluations on the Holdout Test Set\n",
                "y_pred = best_pipeline.predict(X_test)\n",
                "final_mae = mean_absolute_error(y_test, y_pred)\n",
                "final_rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n",
                "final_r2 = r2_score(y_test, y_pred)\n",
                "\n",
                "print(f\"Final Model Metrics on Holdout Test Set:\")\n",
                "print(f\"  - Mean Absolute Error (MAE): ${final_mae:,.2f}\")\n",
                "print(f\"  - Root Mean Squared Error (RMSE): ${final_rmse:,.2f}\")\n",
                "print(f\"  - R-squared (R2): {final_r2:.4f}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Scatter plot of actual vs predicted prices\n",
                "plt.figure(figsize=(10, 6))\n",
                "sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, color='blue')\n",
                "# Plot ideal line\n",
                "ideal_line = np.linspace(y_test.min(), y_test.max(), 100)\n",
                "plt.plot(ideal_line, ideal_line, color='red', linestyle='--', label='Perfect Prediction')\n",
                "plt.title(f'Actual vs. Predicted Property Price (R2 = {final_r2:.4f})')\n",
                "plt.xlabel('Actual Price (USD)')\n",
                "plt.ylabel('Predicted Price (USD)')\n",
                "plt.legend()\n",
                "plt.tight_layout()\n",
                "plt.savefig('../screenshots/model_performance.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 7. Export Model Pipeline"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "model_export_path = \"../models/price_predictor.joblib\"\n",
                "os.makedirs(\"../models\", exist_ok=True)\n",
                "\n",
                "# Export model alongside feature columns list\n",
                "model_package = {\n",
                "    'model': best_pipeline,\n",
                "    'features': features,\n",
                "    'val_r2': final_r2\n",
                "}\n",
                "\n",
                "joblib.dump(model_package, model_export_path)\n",
                "print(f\"Saved final trained ML Pipeline to: {model_export_path}\")"
            ]
        }
    ]
    
    ml_nb = {
        "cells": ml_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(os.path.join(nb_dir, "02_price_prediction_model.ipynb"), "w") as f:
        json.dump(ml_nb, f, indent=1)
        
    print("Programmatically generated both notebooks successfully!")

if __name__ == "__main__":
    create_notebooks()
