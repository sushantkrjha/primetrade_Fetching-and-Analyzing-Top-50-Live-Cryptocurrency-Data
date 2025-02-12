import requests
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe

sa = gspread.service_account(filename="/home/sushant/old/sushant/project/assignment/primtrade/crendential.json")

# API URL and parameters
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": "false"
}

# Excel file path
EXCEL_FILE = "crypto_data.xlsx"

def fetch_crypto_data():
    """Fetch live cryptocurrency data from CoinGecko API."""
    response = requests.get(API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_excel():
    """Fetch new data and save it to the Excel file."""
    data = fetch_crypto_data()
    if data:
        df = pd.DataFrame(data)
        df = df[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]
        df.columns = ["Cryptocurrency", "Symbol", "Current Price (USD)", "Market Capitalization", "24h Volume", "24h Change (%)"]

        # Save to Excel
        sh = sa.open("crypto_data")
        sheet = sh.worksheet("Sheet1")
        set_with_dataframe(sheet, df)

# Run once
if __name__ == "__main__":
    save_to_excel()
