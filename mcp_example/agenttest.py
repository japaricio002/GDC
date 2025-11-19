import asyncio

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="You are an agent with access to my files, answer question I have on them.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Do I have an MCPTest folder on my Desktop?"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)



async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        client_session_timeout_seconds=300,
        params={"url": "http://localhost:8000/sse",
        "timeout": 30,           # 30-second handshake
        "sse_read_timeout": 900  # 15-minute idle-read window
 
                            },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="SSE Example", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
            )
            await run(server)


if __name__ == "__main__":
    
    asyncio.run(main())
