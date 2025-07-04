# app.py
import streamlit as st
from agent import run_quantai_agent, is_backtesting_related
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="QuantAI", layout="centered")
st.title("📊 QuantAI - AI Trading Assistant")

# Select Mode
mode = st.radio("Choose Mode:", [
    "Backtest Strategy", "Get Live Prices", "Get Live RSI Signal"]
)

# Backtest Mode
if mode == "Backtest Strategy":
    prompt = st.text_area(
        "📜 Describe your strategy (e.g. RSI < 25, sell > 70)", height=150)
    
    if st.button("Run Backtest"):
        if is_backtesting_related(prompt):
            with st.spinner("Running GPT-4.1 agent on strategy..."):
                try:
                    result = run_quantai_agent(prompt)
                    st.success("✅ Strategy Result")
                    st.markdown(f"```\n{result}\n```")

                    chart_path = "charts/backtest_plot.png"
                    if os.path.exists(chart_path):
                        st.image(chart_path, caption="Backtest Performance")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("❌ Sorry, I am QuantAI and can only help you with backtesting trading strategies.")

# Live Prices Mode
elif mode == "Get Live Prices":
    if st.button("Fetch Prices"):
        with st.spinner("Contacting GPT-4.1 agent..."):
            try:
                result = run_quantai_agent("What is the live price of BTC and ETH?")
                st.success("✅ Live Prices")
                st.markdown(f"```\n{result}\n```")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# RSI Live Signal Mode
elif mode == "Get Live RSI Signal": 
    if st.button("Analyze RSI Signal"):
        with st.spinner("Analyzing real-time RSI signals using GPT-4.1..."):
            try:
                result = run_quantai_agent("Use the RSI Trading Signal tool to analyze BTC and ETH")
                st.success("✅ RSI Signal")
                st.markdown(f"```\n{result}\n```")
            except Exception as e:
                st.error(f"❌ Error: {e}")