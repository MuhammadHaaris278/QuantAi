# app.py
import streamlit as st
from agent import run_quantai_agent
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="QuantAI", layout="centered")
st.title("📊 QuantAI - AI Trading Assistant")

prompt = st.text_area(
    "💬 Ask something like:\n- Backtest RSI strategy for BTC or ETH\n- Live prices of BTC and ETH\n- Get RSI signal for BTC/ETH",
    height=150
)

if st.button("Run QuantAI"):
    with st.spinner("🔍 Llama analyzing your request..."):
        try:
            result = run_quantai_agent(prompt)
            st.success("✅ Result")
            st.markdown(f"```\n{result}\n```")

            chart_path = "charts/backtest_plot.png"
            if os.path.exists(chart_path):
                st.image(chart_path, caption="Backtest Performance")

        except Exception as e:
            st.error(f"❌ Error: {e}")
