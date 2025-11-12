# agent.py
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

#################################################################
# 1. Example tool the agent can call.
#################################################################
def get_current_time(city: str) -> dict:
    """
    Return the current timestamp for a given city.
    ADK tools are just plain Python callables that return JSON-serializable data.
    The LLM can decide when to call them.
    """
    # NOTE: we're not doing real timezone lookup here;
    # keep it simple for the demo.
    return {
        "status": "success",
        "city": city,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
    }

#################################################################
# 2. Define the model via LiteLLM.
#
# LiteLlm(model="openai/gpt-4o") tells ADK:
#   "Use LiteLLM as the client, ask for provider `openai` and model `gpt-4o`."
#
# LiteLLM will grab OPENAI_API_KEY from the environment.
#################################################################
openai_backed_model = LiteLlm(model="openai/gpt-4o")

#################################################################
# 3. Define the agent itself.
#
# LlmAgent (often imported/aliased as just Agent in ADK docs)
# is the core 'thinking' agent. You give it:
#   - name
#   - model (can be Gemini, OpenAI via LiteLLM, Claude via LiteLLM, etc.)
#   - instruction (system behavior / persona)
#   - optional tools the model is allowed to call
#
# ADK is designed so this agent object can later be orchestrated,
# traced, deployed, etc. :contentReference[oaicite:4]{index=4}
#################################################################
root_agent = LlmAgent(
    name="helpful_assistant",
    model=openai_backed_model,
    instruction=(
        "You are a crisp, helpful assistant. "
        "You can answer questions and, if it helps, call tools to get data. "
        "Only call a tool if it's actually useful."
    ),
    description=(
        "A tiny demo agent running on OpenAI (via LiteLLM) inside Google ADK. "
        "It can also tell the current time in a given city."
    ),
    tools=[get_current_time],
)
