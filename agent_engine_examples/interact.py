import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

from vertexai.preview import reasoning_engines


# 1. Initialize Vertex AI
vertexai.init(project="", location="us-")

# 2. Define the resource name
AGENT_RESOURCE_NAME = ""

# 3. Load the deployed agent resource
try:
    loaded_agent = agent_engines.AgentEngine(AGENT_RESOURCE_NAME)
    print(f"Successfully loaded agent: {loaded_agent.display_name}")
except Exception as e:
    print(f"Error loading agent: {e}")
    exit()

# Create a new session with an arbitrary user ID
session = loaded_agent.create_session(user_id="")
SESSION_ID = session['id']


def send_message(resource_id: str, user_id: str, session_id: str, text: str):
    """Send a text message directly."""
    remote_app = agent_engines.get(resource_id)

    print(f"\n--- Sending message ---")
    print(text)
    print("\n--- Response ---")

    for event in remote_app.stream_query(
        user_id=user_id,
        session_id=session_id,
        message=text,
    ):
        print(event)


if __name__ == "__main__":

    resource_id = AGENT_RESOURCE_NAME
    user_id = ""
    session_id = SESSION_ID

    send_message(
        resource_id=resource_id,
        user_id=user_id,
        session_id=session_id,
        text="",
    )
