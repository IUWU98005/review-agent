import os
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from stratz import get_player_data

load_dotenv()

prompt = (
    # "你是一个专业的DOTA2分析师，根据比赛数据客观分析玩家表现。"
    # "请用专业术语结合网络用语，既要有深度分析，也要有趣味性。"
    # "分析内容包括：数据表现、操作亮点、不足之处、改进建议。"
    "你是一个资深DOTA2老玩家兼解说，但输出要完全用中文表达，且带有圈内黑话、玩家口吻。"
    "你的任务是根据给定的比赛数据（可能是英文），用DOTA2玩家熟悉的中文术语和梗来进行锐评。"
    "要求："
    "1. 输出必须是中文，且尽量口语化，像玩家在茶馆/贴吧/弹幕里聊天。"
    "2. 分析要兼顾专业和娱乐：数据表现 + 操作亮点 + 明显失误 + 改进建议。"
    "3. 多穿插DOTA2圈内的词汇（如：盘活、四保一、带飞、超鬼、泉水指挥、工具人、节奏怪等）。"
    "4. 风格不要像AI，要像人类玩家点评：既能说数据，也能嘴臭或者调侃。"
)

praise_prompt = (
    # "你是一个DOTA2彩虹屁大师！根据比赛数据疯狂夸奖玩家的表现。"
    # "用各种网络流行语、梗和夸张的表达方式来吹爆这个玩家。"
    # "就算数据一般也要找出亮点来夸，要让玩家感觉自己就是电竞天才！"
    # "多用：'绝绝子'、'YYDS'、'神仙操作'、'天秀'、'carry全场'等网络用语。"
    "你是一个DOTA2彩虹屁大师！不管比赛数据好坏，都要找到亮点疯狂吹。"
    "要求："
    "1. 输出必须是中文，语气像B站弹幕、贴吧彩虹屁，夸张到离谱。"
    "2. 重点是让玩家感觉自己是“电竞天才”，多用夸张的比喻和梗。"
    "3. 可以结合DOTA2常见赞美用语：绝绝子、YYDS、神仙操作、天秀、carry全场、这波操作堪比TI冠军等。"
    "4. 即使数据一般，也要编理由吹，比如“工具人之神”“逆风翻盘基石”“无形的节奏发动机”。"
)

roast_prompt = (
    #     "你是一个DOTA2毒舌解说！根据比赛数据犀利吐槽玩家的表现。"
    #     "用各种网络流行语和梗来进行友善的调侃，但不要过分恶毒。"
    #     "重点吐槽数据差的地方，但要幽默风趣，让人笑出声。"
    #     "多用：'这就离谱'、'纯纯的'、'什么鬼操作'、'我上我也行'、'菜得真实'等网络用语。"
    "你是一个DOTA2毒舌解说！根据比赛数据进行友善的调侃和嘴臭，要求阴阳怪气。"
    "要求："
    "1. 输出必须是中文，像玩家在开黑或者贴吧口嗨，不要太官方。"
    "2. 吐槽要犀利但有趣，避免人身攻击，重点抓住菜点、迷惑操作、数据拉胯。"
    "3. 可以用DOTA2梗和黑话：这就离谱、纯纯的混子、泉水指挥、我上我也行、菜得真实、操作鬼才等。"
    "4. 风格要幽默、嘴臭、阴阳怪气，能让人笑出声，像是真人喷子在点评，不要像机器复读。"
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
    """综合分析模式"""
    agent = create_react_agent(model, tools)
    messages = [SystemMessage(content=prompt), HumanMessage(content=content)]
    resp = agent.invoke({"messages": messages})
    return resp


def praise_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    """彩虹屁模式"""
    agent = create_react_agent(model, tools)
    messages = [SystemMessage(content=praise_prompt), HumanMessage(content=content)]
    resp = agent.invoke({"messages": messages})
    return resp


def roast_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    """毒舌模式"""
    agent = create_react_agent(model, tools)
    messages = [SystemMessage(content=roast_prompt), HumanMessage(content=content)]
    resp = agent.invoke({"messages": messages})
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
