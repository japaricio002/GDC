# Model Context Protocol (MCP) Demo -- Desktop Explorer

This repo is a small, end-to-end example of **Model Context Protocol
(MCP)** in Python:

-   `main.py` -- an MCP server built with **FastMCP** that can list
    files on your Desktop.
-   `agenttest.py` -- an **OpenAI Agents SDK** example agent that talks
    to that MCP server over SSE.
-   `requirements.txt` -- the Python dependencies for both pieces.

## 1. What is MCP?

**Model Context Protocol (MCP)** is an open standard for connecting
language models to tools, data, and applications in a consistent way.

In this repo:

-   `main.py` is an **MCP server** that exposes one tool:
    `list_desktop_files`.
-   `agenttest.py` is an **MCP client** (via OpenAI Agents SDK) that
    calls that tool.

## 2. Why use MCP instead of embedding tools directly into agents?

Without MCP, tool versions can drift across agents, becoming
unmaintainable.

With MCP, tools are centralized on a shared server, providing:

-   Modularity & maintainability
-   Security & compliance
-   Reusability across agents

## 3. Project structure

    .
    ├── agenttest.py
    ├── main.py
    └── requirements.txt

## 4. Code overview

### 4.1 `main.py`: FastMCP server

Defines the MCP server and exposes a tool:

    @mcp.tool()
    def list_desktop_files(folder_name: str = "") -> str:
        """Lists files on the user's Desktop."""

Launched with:

    mcp.run(transport="sse")

### 4.2 `agenttest.py`: Agent using the MCP server

Creates an agent:

    agent = Agent(
        name="Assistant",
        instructions="You are an agent with access to my files...",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

## 5. Dependencies & environment

Install:

    pip install -r requirements.txt

Set environment variables:

    export OPENAI_API_KEY="sk-..."

## 6. Running the demo

Start server:

    python main.py

Run agent:

    python agenttest.py
This needs to be done on two different command terminals since the start server command needs to continue to run while you run the agent

