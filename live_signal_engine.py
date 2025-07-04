# live_signal_engine.py
from langchain.tools import Tool
import requests
import pandas as pd
import ta  # For RSI calculation

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"


def fetch_ohlcv(symbol="BTCUSDT", interval="1h", limit=100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(BINANCE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Convert to float
        df[["open", "high", "low", "close", "volume"]] = df[[
            "open", "high", "low", "close", "volume"]].astype(float)

        return df[["open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"Error fetching OHLCV data: {e}")
        return None


def generate_rsi_signal(symbol="BTCUSDT", rsi_buy=30, rsi_sell=70, interval="1h"):
    df = fetch_ohlcv(symbol, interval)
    if df is None or df.empty:
        return f"❌ Failed to fetch data for {symbol}"

    df["RSI"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
    latest_rsi = df["RSI"].iloc[-1]
    latest_price = df["close"].iloc[-1]

    if latest_rsi < rsi_buy:
        signal = "✅ BUY (RSI is oversold)"
    elif latest_rsi > rsi_sell:
        signal = "🚨 SELL (RSI is overbought)"
    else:
        signal = "⏸️ HOLD (No signal)"

    return (
        f"🔹 {symbol} - RSI(14): {latest_rsi:.2f}\n"
        f"📈 Last Close: ${latest_price:,.2f}\n"
        f"📊 Signal: {signal}"
    )


# ✅ LangChain-compatible wrapper

def extract_symbol(user_input: str) -> str:
    if "eth" in user_input.lower():
        return "ETHUSDT"
    return "BTCUSDT"

def rsi_signal_tool(user_input: str) -> str:
    symbol = extract_symbol(user_input)
    return generate_rsi_signal(symbol)


signal_tool = Tool(
    name="RSI Signal Generator",
    func=rsi_signal_tool,
    description= "Use this tool to get a real-time RSI-based trading signal for BTC or ETH. "
        "The tool fetches live OHLCV data and returns BUY, SELL, or HOLD based on RSI levels. "
        "Mention BTC or ETH in your prompt."
)


if __name__ == "__main__":
    print(generate_rsi_signal("BTCUSDT"))
    print("\n")
    print(generate_rsi_signal("ETHUSDT"))
