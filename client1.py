import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage

load_dotenv()

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
    # print(tools,"tools")

    named_tool={}
    for tool in tools:
        named_tool[tool.name]=tool
    # print(named_tool,"named_tool")

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    prompt = "Please calculate the sum of 5 and 10."
    response = await llm_with_tools.ainvoke(prompt)
    selected_tool_call = response.tool_calls[0]
    selected_tool = response.tool_calls[0]['name']
    selected_tool_args = response.tool_calls[0]['args']
    tool_call_id = selected_tool_call["id"]
    # print("Response from LLM with tools:",selected_tool ,selected_tool_args)

    tool_result = await named_tool[selected_tool].ainvoke(selected_tool_args)
    # print("Tool result:", tool_result)

    tool_message = ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call_id
    )
     # Step 6: Send tool result back to LLM
    final_response = await llm_with_tools.ainvoke([
        HumanMessage(content=prompt),
        response,
        tool_message
    ])
   
    print("Final response from LLM with tool result:", final_response.content)
    
if __name__ == "__main__":
    asyncio.run(main())