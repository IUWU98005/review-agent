import os
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from stratz import get_player_data

load_dotenv()

model = ChatOpenAI(
    model="glm-4-flash",
    openai_api_base = "https://open.bigmodel.cn/api/paas/v4",
    api_key=os.getenv("OPENAI_API_KEY"),
)

tools = [DuckDuckGoSearchRun(), get_player_data]


def manual_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    agent = create_react_agent(model, tools)
    resp = agent.invoke({"messages": [HumanMessage(content)]})
    return resp

# def review_agent(query: str, model: ChatOpenAI, tools: list[tool]):
#     model_with_tools = model.bind_tools(tools)
#     model_output = model_with_tools.invoke(query)
#     tool_resp = call_tool(model_output)
#     final_resp = model.invoke(
#         f'original query : {query} \n\n\n tool response : {tool_resp}')
#     return final_resp

# def call_tool(model_output, tools):
#     tools_map = {tool.name.lower(): tool for tool in tools}
#     tools_resp = {}
#     for tool in model_output.tool_calls:
#         tool_name = tool['name']
#         tool_args = tool['args']
#         tool_instance = tools_map[tool_name]
#         tool_resp = tool_instance.invoke(*tool_args.values())
#         tools_resp[tool_name] = tool_resp
#     return tools_resp

