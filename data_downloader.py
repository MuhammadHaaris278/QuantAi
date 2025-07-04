# data_downloader.py
import yfinance as yf

def download_assets():
    btc = yf.download("BTC-USD", start="2022-01-01", end="2025-05-31")
    btc.to_csv("data/btc_2022_2025.csv")

    eth = yf.download("ETH-USD", start="2022-01-01", end="2025-05-31")
    eth.to_csv("data/eth_2022_2025.csv")

    print("✅ BTC and ETH historical data downloaded.")

if __name__ == "__main__":
    download_assets()
