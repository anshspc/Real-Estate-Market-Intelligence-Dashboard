# Power BI Dashboard Implementation Guide

This document describes how to construct the professional **Real Estate Market Intelligence Dashboard** in Power BI Desktop using the dataset generated in this repository.

---

## 1. Data Connection & ETL (Power Query)
1. Open Power BI Desktop.
2. Select **Get Data** -> **Text/CSV** and select `data/cleaned_properties.csv`.
3. In Power Query:
   - Ensure the column datatypes are parsed correctly:
     - `Property_ID`: Text
     - `Price_USD`: Fixed Decimal (Currency)
     - `Area_SqFt`: Decimal
     - `Bedrooms` & `Bathrooms`: Whole Number
     - `Year_Built`: Whole Number (or Text if represented as year categories)
     - `Listing_Date`: Date
     - `Demand_Score`: Whole Number
     - `Customer_Rating`: Decimal
     - `Property_Age`: Whole Number
     - `Investment_Score`: Decimal
   - Click **Close & Apply**.

### Create a Calendar Table (DAX)
To perform time-intelligence calculations (YoY Growth, YTD values), create a Date dimension table in Power BI by clicking **New Table** under Modeling:
```dax
Calendar = 
ADDCOLUMNS(
    CALENDAR(DATE(2024, 1, 1), DATE(2025, 12, 31)),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "MMMM"),
    "Month Short", FORMAT([Date], "MMM"),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "YearMonth", FORMAT([Date], "YYYY-MM")
)
```

---

## 2. Data Modeling & Relationships
1. Go to the **Model View** tab.
2. Establish a **1-to-many relationship** from the `Calendar` table to `cleaned_properties`:
   - Drag `Calendar[Date]` to `cleaned_properties[Listing_Date]`.
   - Cardinality: **1 to * (One-to-many)**.
   - Cross-filter direction: **Single** (Calendar filters properties).

---

## 3. Creating DAX Measures
Navigate to the **Data View** tab, select the table, and click **New Measure**. Copy the DAX code blocks from [dax_measures.dax](./dax_measures.dax) to create:
1. `Total Listings`
2. `Average Price`
3. `Average Price per SqFt`
4. `BI Investment Opportunity Score`
5. `City Average Price per SqFt`
6. `Locality Premium Index`
7. `YoY Revenue Growth %`
8. `Opportunity Color Alert` (for conditional formatting)

---

## 4. Visual Layout Design

### Theme & Styling (Modern Dark Glassmorphism)
Go to the **View** ribbon -> Themes -> Import Theme and paste the following JSON block for a curated color palette:
```json
{
  "name": "MarketIntelligenceDark",
  "dataColors": ["#00F2FE", "#4FACFE", "#00FF66", "#FFA500", "#FF3333", "#7F00FF", "#E100FF", "#B0B0B0"],
  "background": "#0F172A",
  "foreground": "#F8FAFC",
  "tableAccent": "#00F2FE"
}
```
* **Background Canvas**: Solid `#0F172A` (Slate Dark)
* **Visual Card Backgrounds**: `#1E293B` (Navy-Slate) with a 1px border of `#334155` and a 4px corner radius.
* **Typography**: *Inter* or *Segoe UI Semibold* for headers, *Segoe UI* for detail labels.

---

### Page 1: Executive Overview (For Executive Suite)
*Target: Market performance at a glance*

1. **Header Block**: Title: "Real Estate Market Intelligence Dashboard" | Subtitle: "Executive Portfolio & Investment Analysis"
2. **KPI Card Visuals** (Top Row):
   - Total Listings
   - Average Listing Price (Formatted as Currency `$`)
   - Average Price per SqFt (`$#/sqft`)
   - Avg Market Demand Score (Out of 10)
3. **Map Visual** (Center Left):
   - Location: `Locality` and `City`
   - Bubble Size: `Total Listings`
   - Tooltips: `Average Price`, `Investment_Score`
4. **Locality Opportunity Matrix** (Center Right - Table Visual):
   - Columns: `City`, `Locality`, `Total Listings`, `Average Price per SqFt`, `BI Investment Opportunity Score`
   - Conditional Formatting: Apply background color to `BI Investment Opportunity Score` using Field Value: `[Opportunity Color Alert]`.
5. **Filters / Slicers** (Side Panel):
   - City Slicer (Dropdown)
   - Property Type Slicer (Horizontal buttons or Tile)
   - Date Slicer (Year/Quarter slider)

---

### Page 2: Property Type & Demographics (For Brokerage & Sales Operations)
*Target: Property distribution and price elasticity*

1. **Donut Chart**: Property Types by Volume
   - Legend: `Property_Type`
   - Value: `Total Listings` (Show percentage and value)
2. **Scatter Plot**: Price vs. Area by Property Type
   - X-Axis: `Area_SqFt`
   - Y-Axis: `Price_USD`
   - Legend / Details: `Property_Type`
   - Trend Line: Enable linear trend line to show scaling factors.
3. **Stacked Bar Chart**: Status by City
   - X-Axis: `City`
   - Y-Axis: `Total Listings`
   - Legend: `Status` (Active, Pending, Sold)
4. **Waterfall Chart**: Average Price per SqFt progression across localities.

---

### Page 3: Trend & Cohort Analysis (For Investors)
*Target: Finding undervalued pockets*

1. **Line Chart**: Median Price per SqFt Monthly Trend
   - X-Axis: `Calendar[Date]` (aggregated to Year/Month)
   - Y-Axis: `Average Price per SqFt`
   - Legend: `City`
2. **Clustered Bar Chart**: Locality Premium Index
   - Y-Axis: `Locality`
   - X-Axis: `Locality Premium Index` (Formatted as Percentage)
   - *Interpretation*: Items extending right of 0% represent premium/expensive locations; items extending left are discounted/undervalued.
3. **Heatmap Table**: Property Age vs. Price Category
   - Categorize properties into groups (e.g. New <5 yrs, Mid-Age 5-15 yrs, Established >15 yrs).
   - Display a cross-matrix showing average demand scores.

---

## 5. Interaction Configuration
- Ensure all charts have **Edit Interactions** enabled.
- Clicking a locality on the Map should instantly cross-filter the Scatter Plot and update all KPI cards.
- Clicking a slice of the Donut Chart (e.g. Commercial) should update the map to show only commercial properties.
