import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVERS={
    "SimpleCalculatorServer":{
        "transport":"stdio",
        "command":"/home/navsingh3211/anaconda3/bin/uv",
        "args":[
            "run",
            "fastmcp",
            "run",
            "/usr/local/src/myWork/AGENTIC_AI_STUDY/deploy-mcp-on-remote-server/main.py"
        ]
    }
}

async def main():
    print("Starting MultiServerMCPClient...")
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    print(tools,"tools")

if __name__ == "__main__":
    asyncio.run(main())