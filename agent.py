import os
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from stratz import get_player_data

load_dotenv()

prompt = (
    "根据Dota2的比赛数据, 专业、犀利地评价该玩家的表现, 指出优点和不足, 并给出改进建议"
)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", prompt), ("human", "{new_message}")]
)

model = ChatOpenAI(
    model="glm-4-flash",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4",
    api_key=os.getenv("OPENAI_API_KEY"),
)

tools = [get_player_data]


def agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
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

# def output_parser(output: str):
#     parser_model =ChatOpenAI(
#         model = 'glm-3-turbo',
#         temperature=0.2,
#         openai_api_base = "https://open.bigmodel.cn/api/paas/v4",
#         api_key=os.getenv("OPENAI_API_KEY"),
#     )
#     message = f"你需要将传入的文本改写，尽可能自然。 这是你需要改写的文本：`{text}`"
#     return parser_model.invoke(message.format(text=output))
