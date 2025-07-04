# agent.py
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools  # Now tools is a list

import os

llm = ChatOpenAI(
    temperature=0,
    model="openai/gpt-4.1",
    base_url="https://models.github.ai/inference",
    api_key=os.getenv("GITHUB_TOKEN")
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def is_backtesting_related(prompt: str) -> bool:
    keywords = [
        "rsi", "ema", "macd", "moving average", "bollinger", "backtest",
        "buy", "sell", "entry", "exit", "strategy", "trading", "signal", "BTC", "ETH", "analyze", "analysis", "live", "prices"
    ]
    return any(word in prompt.lower() for word in keywords)


def run_quantai_agent(prompt: str) -> str:
    if not is_backtesting_related(prompt):
        return "❌ Sorry, I am QuantAI and can only help you with backtesting trading strategies."

    return agent.run(prompt)
