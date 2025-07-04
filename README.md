# 📊 QuantAI - AI Crypto Trading Assistant

QuantAI is an intelligent crypto trading assistant that works both online (OpenAI GPT-4.1) and offline (Ollama with CodeLLaMA). It allows users to interact via natural language and get backtesting results, live BTC/ETH prices, and RSI signals using technical indicators.

## 🚀 Features

- Natural language understanding for trading strategies
- RSI-based backtesting on BTC and ETH (2022–2025 historical data)
- Real-time crypto price fetching using CoinGecko API
- RSI signal generation using Binance OHLCV data
- Local support via Ollama + CodeLLaMA
- Optional GPT-4.1 API support
- Streamlit frontend interface
- Chart visualization of backtest results
- Modular tool-based architecture (LangChain Tools)

## 🧠 How It Works

QuantAI uses LangChain's ReAct-style agent to understand your prompt and automatically select the correct tool:

- Backtest Strategy Tool: Runs RSI backtest on BTC/ETH
- Live Crypto Price Tool: Fetches BTC/ETH prices from CoinGecko
- RSI Signal Generator: Fetches RSI signals from Binance data

## 📂 Project Structure

    .
    ├── app.py                  → Streamlit UI
    ├── agent.py                → LLM + LangChain agent logic
    ├── tools.py                → LangChain tools
    ├── strategy_engine.py      → Backtest logic
    ├── live_signal_engine.py   → RSI signal logic
    ├── realtime_fetcher.py     → CoinGecko price fetcher
    ├── data/                   → BTC and ETH CSV data
    ├── charts/                 → Backtest chart output
    └── .env                    → Environment variables

## 🛠️ Setup Instructions

### 1. Clone the Repository

    git clone https://github.com/yourusername/quantai.git
    cd quantai

### 2. Create and Activate Virtual Environment

    python -m venv venv
    source venv/bin/activate      # Windows: venv\Scripts\activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Prepare Environment Variables

Create a `.env` file in the root directory:

    OPENAI_API_KEY=your_openai_api_key

Skip this if you're using only Ollama locally.

### 5. Run Ollama (if using CodeLLaMA)

    ollama run codellama

### 6. Launch the App

    streamlit run app.py

## 💬 Example Prompts

- Backtest RSI strategy for BTC  
- Live prices of BTC and ETH  
- Get RSI signal for ETH  

## ✅ Status

- Backtesting working with chart outputs  
- Ollama-based function calling works locally  
- GPT-4.1 works via API  
- Unified prompt with auto-detection of intent  

## 🔐 Security & Safety

- Prevents hallucinated tool calls with iteration limits  
- Blocks irrelevant prompts that aren't related to trading  
- Hides sensitive credentials via `.env` file  

## 👤 Author

Built by Haaris  
AI Engineer Intern @ Kryptomind
