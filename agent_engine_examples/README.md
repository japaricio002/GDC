# Google Agent Engine Workshop 

Welcome!\
This repo introduces you to **Google's Agent Engine**, a fully
managed platform for deploying production-ready AI agents. You'll learn
what an agent is, how the Agent Engine works, and how to run two example
agents---one powered by **Gemini** and the other by **ChatGPT (via
LiteLLM)**.

------------------------------------------------------------------------

# What Is an AI Agent?

A **large language model (LLM)** responds to instructions.

An **agent**, however, goes further:

> **An agent is an AI system that takes your goal, plans what steps are
> needed, and then uses tools to accomplish the task---autonomously.**

Example:\
A normal LLM cannot read your "Downloads" folder.\
An agent *can*---if you give it a **tool** that accesses that folder.

An agent: - Decides whether tools are needed\
- Chooses the correct tools\
- Executes them\
- Returns the final result

This autonomy is what makes agentic systems so powerful.

------------------------------------------------------------------------

# What Is Google's Agent Engine?
https://docs.cloud.google.com/agent-builder/agent-engine/overview

Google's **Agent Engine** is a **fully managed, production-grade
platform** for running your agents without worrying about
infrastructure.

### ☁️ It handles:

-   Hosting\
-   Scaling\
-   Networking\
-   Security\
-   Observability\
-   Context management\
-   Logging + tracing

### Framework-agnostic

![Agent Engine](https://docs.cloud.google.com/static/agent-builder/agent-engine/images/agent-engine.png)

###  Model-agnostic

Works with **Gemini**, **OpenAI**, and others.

------------------------------------------------------------------------

#  Pricing

Google offers a generous free tier:

  Resource   Free Monthly Quota
  ---------- --------------------------
  **vCPU**   **180,000 vCPU-seconds**
  **RAM**    **360,000 GiB-seconds**

Beyond that, pricing is **usage-based**---you only pay when compute is
used.

------------------------------------------------------------------------

#  Project Structure

```
agent_engine_examples
├── book_recommendation_agent
│   └── agent.py
├── weather_agent
│   └── agent.py
├── .env
├── deploy.py
├── interact.py
└── requirements.txt
```

------------------------------------------------------------------------

#  Dependencies

From `requirements.txt`:

    google-adk
    litellm
    dotenv

Install:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

#  Environment Variables

Create `.env`:

    OPENAI_API_KEY=
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=
    GOOGLE_CLOUD_LOCATION=
    GOOGLE_CLOUD_STAGING_BUCKET=


------------------------------------------------------------------------

# 🛠 Prerequisites

1.  Google Account\
2.  Create Project + enable Vertex AI API\
3.  Create Storage Bucket\
4.  Install Google CLI\
5.  Authenticate:\

``` bash
gcloud auth application-default login
gcloud init
```

------------------------------------------------------------------------

#  The Two Example Agents

##  Gemini Weather Outfit Agent

Tools: - `get_lat_long(city)` - `get_temp(lat, long)`

Steps: 1. Get coordinates\
2. Get temperature\
3. Suggest outfit

##  ChatGPT Book Recommendation Agent (via LiteLLM)

Uses: - `get_book_by_theme(theme)`

------------------------------------------------------------------------

#  Local Development

Run:

``` bash
adk web
```

Select your agent and interact with it via UI.

------------------------------------------------------------------------

# Deploying to Agent Engine

Once you've defined your agent, you can deploy it to Agent Engine with:

``` bash
python deploy.py
```

------------------------------------------------------------------------

## 1. Ensure your project structure

Your repo should look like this (one folder per agent, each with an
`agent.py` exposing `root_agent`):

    agent_engine_examples
    ├── book_recommendation_agent
    │   └── agent.py
    ├── weather_agent
    │   └── agent.py
    ├── .env
    ├── deploy.py
    ├── interact.py
    └── requirements.txt

> Replace `book_recommendation_agent` / `weather_agent` with your own
> agent folders as needed.

------------------------------------------------------------------------

## 2. Configure `deploy.py`

Below is an example `deploy.py`:

``` python
import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

# 1) Load environment variables from .env
load_dotenv()

# 2) Import the correct root_agent for the agent you want to deploy
# For the book recommendation agent:
from book_recommendation_agent.agent import root_agent
# For the weather agent, you would instead use:
# from weather_agent.agent import root_agent

# 3) Python dependencies required by your agent
requirements = [
    "requests",
    "google-adk",
    "litellm",
    # add any other libraries your agent code needs
]

# 4) Environment variables your agent will need at runtime
agent_env_vars = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    # add any other keys your agent code expects
    # "ANOTHER_API_KEY": os.getenv("ANOTHER_API_KEY"),
}

# 5) Vertex AI / GCP configuration
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

# 6) Create (deploy) the remote agent
remote_agent = agent_engines.create(
    display_name="book_recommendation_agent",  # update this per agent
    agent_engine=root_agent,                   # the imported root_agent
    requirements=requirements,                 # runtime Python deps
    extra_packages=["./book_recommendation_agent"],  # path to your agent package
    env_vars=agent_env_vars,                   # runtime environment variables
)

print(f"Deployment successful! Agent resource name: {remote_agent.resource_name}")
```

------------------------------------------------------------------------

## 3. Things you *must* update

### Update the import

``` python
from book_recommendation_agent.agent import root_agent
```

Change `book_recommendation_agent` to match the folder containing your
`agent.py`.

Example for the weather agent:

``` python
from weather_agent.agent import root_agent
```

------------------------------------------------------------------------

### Update `display_name`

``` python
display_name="book_recommendation_agent",
```

Set this to something meaningful for your specific agent, e.g.:

-   `"weather_agent"`
-   `"support_ticket_triage_agent"`

------------------------------------------------------------------------

### Update `extra_packages`

``` python
extra_packages=["./book_recommendation_agent"],
```

This must point to the directory that contains the agent's code.

Example for the weather agent:

``` python
extra_packages=["./weather_agent"],
```

------------------------------------------------------------------------

### Update `requirements`

Add all Python libraries your agent needs at runtime:

``` python
requirements = [
    "requests",
    "google-adk",
    "litellm",
    "pydantic",
    "pandas",
    # etc...
]
```

If it's imported by your agent, it should be here (unless it's in the
standard library).

------------------------------------------------------------------------

### Update `agent_env_vars`

Add all environment variables your agent depends on:

``` python
agent_env_vars = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "BOOKS_API_KEY": os.getenv("BOOKS_API_KEY"),
    "WEATHER_API_KEY": os.getenv("WEATHER_API_KEY"),
}
```

Ensure these are present in your `.env` file or environment.

------------------------------------------------------------------------

## 4. Running the deployment

From the project root (`agent_engine_examples`):

``` bash
python deploy.py
```

On success, you should see:

    Deployment successful! Agent resource name: ...

------------------------------------------------------------------------

## 5. Deployment time & monitoring

-   Deployment may take **up to 10 minutes**.
-   Monitor progress using **Cloud Logging / Log Explorer** in the
    Google Cloud Console.


------------------------------------------------------------------------

# Interacting With Deployed Agent

The script below shows how to load your deployed Agent Engine and send
it a message from Python. All configuration is done **inside the
script**

``` python
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

from vertexai.preview import reasoning_engines

# Load environment variables from .env if you want to use them
load_dotenv()

# 1. Initialize Vertex AI
# Fill in your actual PROJECT_ID and LOCATION.
vertexai.init(
    project="<YOUR_PROJECT_ID>",          # e.g. "my-gcp-project"
    location="<YOUR_LOCATION>",           # e.g. "us-central1"
)

# 2. Define the resource name of your deployed agent
# This value can be found in the Agent Engines section in GCP.
# It is shown in the column named "Resource name".
AGENT_RESOURCE_NAME = "<YOUR_AGENT_RESOURCE_NAME>"  # e.g. "projects/.../locations/.../agentEngines/..."

# 3. Load the deployed agent resource
try:
    loaded_agent = agent_engines.AgentEngine(AGENT_RESOURCE_NAME)
    print(f"Successfully loaded agent: {loaded_agent.display_name}")
except Exception as e:
    print(f"Error loading agent: {e}")
    exit()

# 4. Create a new session with an arbitrary user ID
# user_id is arbitrary and does not matter; it just groups messages into a session.
session = loaded_agent.create_session(user_id="example-user")
SESSION_ID = session["id"]


def send_message(resource_id: str, user_id: str, session_id: str, text: str):
    """Send a text message directly to the deployed agent."""
    remote_app = agent_engines.get(resource_id)

    print("\n--- Sending message ---")
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
    user_id = "example-user"   # arbitrary; can be any string
    session_id = SESSION_ID

    # 5. This text is the ask to the agent
    send_message(
        resource_id=resource_id,
        user_id=user_id,
        session_id=session_id,
        text="Recommend a fantasy book.",
    )
```

## What you need to fill in

### **Project and Location**

Update inside:

``` python
vertexai.init(
    project="<YOUR_PROJECT_ID>",
    location="<YOUR_LOCATION>",
)
```

-   `project` → your Google Cloud Project ID\
-   `location` → region where you deployed the agent (example:
    `us-central1`)

------------------------------------------------------------------------

### **Agent Resource Name**

Found in **Google Cloud Console → Vertex AI → Agent Engines**\
Use the value in the **"Resource name"** column.

``` python
AGENT_RESOURCE_NAME = "projects/.../agentEngines/..."
```

------------------------------------------------------------------------

### **user_id**

Any arbitrary string:

``` python
user_id = "example-user"
```

This only groups messages into a session---your agent behavior does not
depend on it.

------------------------------------------------------------------------

### **Text**

Set this to whatever you want to ask the agent:

``` python
text="Recommend a fantasy book."
```

------------------------------------------------------------------------

