# realtime_fetcher.py
import requests

def fetch_coingecko_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        prices = {
            "BTC": {"name": "Bitcoin", "price": data["bitcoin"]["usd"]},
            "ETH": {"name": "Ethereum", "price": data["ethereum"]["usd"]}
        }

        return prices

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    prices = fetch_coingecko_prices()

    if "error" in prices:
        print("❌ Error:", prices["error"])
    else:
        for sym, info in prices.items():
            print(f"{sym}: {info['name']} → ${info['price']:,}")
