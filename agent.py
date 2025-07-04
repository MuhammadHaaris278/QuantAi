from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from tools import tools

llm = Ollama(
    model="codellama",
    temperature=0,
)

SYSTEM_INSTRUCTIONS = """
You are QuantAI, an AI crypto trading assistant.
You MUST use tools to answer.
Do not repeat tool calls.
Stop after the first valid result.
"""

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    return_intermediate_steps=True  # ✅ Required to capture final observation manually
)


def run_quantai_agent(prompt: str) -> str:
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\nUser: {prompt}"
    try:
        result = agent.invoke({"input": full_prompt})

        # ✅ If final output exists, return that
        if isinstance(result, dict):
            if "output" in result and result["output"]:
                return result["output"]
            elif "intermediate_steps" in result:
                # 🔍 Return last observation as fallback
                steps = result["intermediate_steps"]
                if steps and isinstance(steps[-1], tuple):
                    return f"📍 Last observation:\n{steps[-1][1]}"
        return "⚠️ The agent didn't return a valid output."

    except Exception as e:
        return f"❌ Agent error: {e}"
