# tools.py

from langchain.tools import Tool
from strategy_engine import run_strategy_with_prompt
from realtime_fetcher import fetch_coingecko_prices
from live_signal_engine import signal_tool

# Backtest Tool — now dynamically handles ETH or BTC


def run_backtest_tool(prompt: str) -> str:
    return run_strategy_with_prompt(prompt)

# Live Price Tool


def live_price_tool(_: str) -> str:
    prices = fetch_coingecko_prices()
    if not prices or "error" in prices:
        return f"❌ Failed to fetch live prices. Reason: {prices.get('error', 'Unknown')}"

    result = ""
    for symbol, data in prices.items():
        result += f"🔸 {data['name']} ({symbol.upper()}): ${data['price']:,}\n"
    return result.strip()


# Tool list
tools = [
    Tool(
        name="Backtest Strategy Tool",
        func=run_backtest_tool,
        description="Backtests an RSI-based trading strategy on BTC or ETH using historical data from 2022-2025. Input should mention RSI and specify BTC or ETH."
    ),
    Tool(
        name="Live Crypto Price Tool",
        func=live_price_tool,
        description="Returns real-time prices of BTC and ETH using CoinGecko. Input can be anything."
    ),
    signal_tool  # Already uses symbol extraction internally
]
