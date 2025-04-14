# import asyncio
# from typing import Optional
# from contextlib import AsyncExitStack

# from mcp.client.sse import sse_client
# from mcp import ClientSession, stdio_server
# from mcp import ClientSession, StdioServerParameters, types
# from mcp.client.stdio import stdio_client

# from langchain_core.messages import AIMessage, HumanMessage

# # from anthropic import Anthropic
# from dotenv import load_dotenv

# sse_client.py
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # SSE server URL
    server_url = "http://localhost:8080/sse"

    print(f"Connecting to SSE server at {server_url}...")

    # Create the connection via SSE transport
    async with sse_client(url=server_url) as streams:
        # Create the client session with the streams
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            response = await session.list_tools()
            print(f"\nAvailable tools: {[tool.name for tool in response.tools]}\n")

            # Call the greet tool
            result = await session.call_tool("remainder", {"a": "8", "b": "3"})
            print(f"\nremainder result: {result.content}\n")

            # Call the add tool
            result = await session.call_tool("multiply", {"a": 10, "b": 32})
            print(f"\nmultiply result: {result.content}\n")

            # List available prompts
            prompts = await session.list_prompts()
            print(f"\n{prompts}\n")
            # Get a prompt
            prompt = await session.get_prompt(
                "echo_prompt", arguments={"message": "MessageValue"}
            )
            print(f"\n{prompt}\n")

            # List available resources
            resources = await session.list_resources()
            print(f"\n{resources}\n")


if __name__ == "__main__":
    asyncio.run(main())
