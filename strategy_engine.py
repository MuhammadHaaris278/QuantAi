# strategy_engine.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import ta  # For RSI

def extract_symbol(prompt: str) -> str:
    if "eth" in prompt.lower():
        return "eth"
    return "btc"

def get_csv_path(symbol: str) -> str:
    return f"data/{symbol}_2022_2025.csv"

def run_rsi_strategy(csv_path, rsi_buy=30, rsi_sell=70):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close']).rsi()

    df['Signal'] = 0
    df.loc[df['RSI'] < rsi_buy, 'Signal'] = 1   # Buy
    df.loc[df['RSI'] > rsi_sell, 'Signal'] = -1  # Sell

    df['Position'] = df['Signal'].replace(0, method='ffill')

    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Returns'] * df['Position'].shift()

    total_return = round(df['Strategy_Returns'].sum() * 100, 2)
    trades = df['Signal'].abs().sum()

    os.makedirs("charts", exist_ok=True)

    plt.figure(figsize=(10, 5))
    df['Close'].plot(label="Close Price", alpha=0.5)
    df[df['Signal'] == 1]['Close'].plot(marker='^', color='g', linestyle='', label='Buy Signal')
    df[df['Signal'] == -1]['Close'].plot(marker='v', color='r', linestyle='', label='Sell Signal')
    plt.title("RSI Strategy Backtest")
    plt.legend()
    plt.tight_layout()
    chart_path = "charts/backtest_plot.png"
    plt.savefig(chart_path)
    plt.close()

    return {
        "total_return": total_return,
        "trades": trades,
        "chart_path": chart_path
    }

def run_strategy_with_prompt(prompt: str) -> str:
    symbol = extract_symbol(prompt)
    csv_path = get_csv_path(symbol)

    if not os.path.exists(csv_path):
        return f"❌ Dataset for {symbol.upper()} not found."

    result = run_rsi_strategy(csv_path)
    return (
        f"📊 RSI Strategy Backtest on {symbol.upper()}:\n"
        f"🔁 Number of trades: {result['trades']}\n"
        f"💹 Total return: {result['total_return']}%\n"
        f"📈 Chart saved to: {result['chart_path']}"
    )
