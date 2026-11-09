import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import json
import os
load_dotenv()

SERVERS = { 
    "SimpleCalculatorServer":{ # local mcp
        "transport":"stdio",
        "command":"/home/navsingh3211/anaconda3/bin/uv",
        "args":[
            "run",
            "fastmcp",
            "run",
            "/usr/local/src/myWork/AGENTIC_AI_STUDY/deploy-mcp-on-remote-server/main.py"
        ]
    },
    "expenseTrackerMcpServer":{ #remote deployed mcp 
        "transport":"streamable_http",
        "url":"https://navsingh3211-expense-tracker.fastmcp.app/mcp",
        "headers": {
            "Authorization": f"Bearer {os.getenv('FASTMCP_AUTH_TOKEN')}"
        }
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatOpenAI(model="gpt-5")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "Add expense - Rs 800 for movie ramayna on 4th nov"
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())