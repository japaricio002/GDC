import vertexai
import os
from vertexai import agent_engines
from book_recommendation_agent.agent import root_agent # make sure to update to correct agent directory
from dotenv import load_dotenv
load_dotenv()

requirements = [
    "requests",
    "google-adk", 
    "litellm"   
]
agent_env_vars = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
}

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET") 
print(PROJECT_ID)
print(LOCATION)
print(STAGING_BUCKET)
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

remote_agent = agent_engines.create(
    display_name="book_recommendation_agent",
    agent_engine=root_agent,
    requirements=requirements,
    extra_packages=["./book_recommendation_agent"],
    env_vars=agent_env_vars,
)

print(f"Deployment successful! Agent resource name: {remote_agent.resource_name}")
