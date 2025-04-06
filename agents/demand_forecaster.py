from agents.base import BaseAgent
from llm.ollama_runner import run_ollama

class DemandForecasterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Demand Forecaster")

    def forecast(self, product_id: str, past_data_rows: list[dict], target_row: dict) -> str:
        context = "\n".join([
            f"{i+1}. Date: {r['Date']}, Sales Quantity: {r['Sales Quantity']}, Price: {r['Price']}, Promotions: {r['Promotions']}, "
            f"Seasonality: {r['Seasonality Factors']}, External: {r['External Factors']}, Trend: {r['Demand Trend']}, Segment: {r['Customer Segments']}"
            for i, r in enumerate(past_data_rows)
        ])

        target_context = (
            f"Store ID: {target_row['Store ID']}, Date: {target_row['Date']}, Price: {target_row['Price']}, "
            f"Promotions: {target_row['Promotions']}, Seasonality: {target_row['Seasonality Factors']}, "
            f"External Factors: {target_row['External Factors']}, Demand Trend: {target_row['Demand Trend']}, "
            f"Customer Segments: {target_row['Customer Segments']}"
        )

        prompt = (
            f"You are a demand forecasting expert.\n\n"
            f"📊 Here is the past 10 months' data for Product ID {product_id}:\n{context}\n\n"
            f"🧩 Based on the above, forecast the demand (sales quantity) for the following month with this information:\n{target_context}\n\n"
            f"📌 Output ONLY the forecast number, followed by a one-line reason without any text formatting."
        )

        return run_ollama(prompt)
