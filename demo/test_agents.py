from agents.demand_forecaster import DemandForecasterAgent
import pandas as pd

# Load dataset
df = pd.read_csv("data/demand_forecasting.csv")

# Ensure enough rows
if len(df) < 11:
    raise ValueError("Dataset must have at least 11 rows for multi-row forecasting.")

# Extract historical rows and target row
past_rows = [df.iloc[i].to_dict() for i in range(10)]
target_row = df.iloc[10].to_dict()
product_id = target_row["Product ID"]

# Show context to user
print("\n🗂️ Historical Data (Used for Forecast):")
for i, row in enumerate(past_rows, 1):
    print(f"{i}. Date: {row['Date']}, Sales Quantity: {row['Sales Quantity']}, Price: {row['Price']}, Promotions: {row['Promotions']}, "
          f"Seasonality: {row['Seasonality Factors']}, External: {row['External Factors']}, Trend: {row['Demand Trend']}, Segment: {row['Customer Segments']}")

print("\n🎯 Target Month Details (Prediction Target):")
print(f"Date: {target_row['Date']}, Store ID: {target_row['Store ID']}, Price: {target_row['Price']}, Promotions: {target_row['Promotions']}, "
      f"Seasonality: {target_row['Seasonality Factors']}, External: {target_row['External Factors']}, Demand Trend: {target_row['Demand Trend']}, "
      f"Customer Segments: {target_row['Customer Segments']}")

# Run agent
agent = DemandForecasterAgent()
forecast = agent.forecast(product_id, past_rows, target_row)

print("\n📈 Final Forecast:", forecast.strip())
