import streamlit as st
from dotenv import load_dotenv
from agent import agent, model, tools

load_dotenv()

st.set_page_config(
    page_title="锐评小助手",
)

# ========== 对话历史功能 - 暂时注释 ==========
# # 对话数据文件路径
# CHATS_FILE = "chats_history.json"

# def load_chats():
#     """加载所有对话历史"""
#     if os.path.exists(CHATS_FILE):
#         try:
#             with open(CHATS_FILE, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         except:
#             return {}
#     return {}

# def save_chats(chats):
#     """保存所有对话历史"""
#     with open(CHATS_FILE, 'w', encoding='utf-8') as f:
#         json.dump(chats, f, ensure_ascii=False, indent=2)

# def create_new_chat():
#     """创建新对话"""
#     chat_id = str(uuid.uuid4())
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
#     return {
#         "id": chat_id,
#         "title": f"新对话 {timestamp}",
#         "created_at": timestamp,
#         "messages": []
#     }

# def get_chat_title(messages):
#     """根据第一条消息生成对话标题"""
#     if messages:
#         first_message = messages[0]["content"]
#         # 取前20个字符作为标题
#         title = first_message[:20]
#         if len(first_message) > 20:
#             title += "..."
#         return title
#     return "新对话"
# ========== 对话历史功能结束 ==========

st.markdown(
    """
<style>
    /* 主标题样式 - 适配暗色模式 */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 用户消息样式 - 暗色模式适配 */
    .user-message {
        background-color: var(--user-message-bg);
        color: var(--user-message-text);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        margin-left: auto;
        margin-right: 0;
        text-align: left;
        float: right;
        clear: both;
        word-wrap: break-word;
        border: 1px solid var(--border-color);
    }
    
    /* AI消息样式 - 暗色模式适配 */
    .ai-message {
        background-color: var(--ai-message-bg);
        color: var(--ai-message-text);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        margin-left: 0;
        margin-right: auto;
        border: 1px solid var(--border-color);
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    
    .message-container {
        width: 100%;
        overflow: hidden;
        margin: 8px 0;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #666;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        margin: 4px 0;
    }
    
    .stButton > button:hover {
        background-color: #555;
    }
    
    /* 亮色模式变量 */
    :root {
        --text-color: #333;
        --user-message-bg: #e3f2fd;
        --user-message-text: #1565c0;
        --ai-message-bg: #f5f5f5;
        --ai-message-text: #333;
        --border-color: #ddd;
    }
    
    /* 暗色模式变量 */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #e0e0e0;
            --user-message-bg: #1e3a8a;
            --user-message-text: #bfdbfe;
            --ai-message-bg: #374151;
            --ai-message-text: #f3f4f6;
            --border-color: #4b5563;
        }
    }
    
    /* Streamlit暗色模式检测 */
    [data-theme="dark"] {
        --text-color: #e0e0e0;
        --user-message-bg: #1e3a8a;
        --user-message-text: #bfdbfe;
        --ai-message-bg: #374151;
        --ai-message-text: #f3f4f6;
        --border-color: #4b5563;
    }
    
    /* 强制暗色模式样式（针对Streamlit特殊情况） */
    .stApp[data-theme="dark"] .main-header,
    .stApp[data-theme="dark"] .user-message,
    .stApp[data-theme="dark"] .ai-message {
        color: var(--text-color) !important;
    }
    
    .stApp[data-theme="dark"] .user-message {
        background-color: var(--user-message-bg) !important;
        color: var(--user-message-text) !important;
        border-color: var(--border-color) !important;
    }
    
    .stApp[data-theme="dark"] .ai-message {
        background-color: var(--ai-message-bg) !important;
        color: var(--ai-message-text) !important;
        border-color: var(--border-color) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-header">Dota2 锐评小助手</h1>', unsafe_allow_html=True)

# ========== 简化的会话状态管理 ==========
# 初始化简单的消息历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 侧边栏 - 简化功能 ==========
with st.sidebar:
    st.markdown("### 设置")

    # 清除对话按钮
    if st.button("清除对话"):
        st.session_state.messages = []
        st.rerun()

# ========== 对话历史功能 - 暂时注释 ==========
# # 初始化会话状态
# if 'chats' not in st.session_state:
#     st.session_state.chats = load_chats()

# if 'current_chat_id' not in st.session_state:
#     # 如果没有对话，创建一个新的
#     if not st.session_state.chats:
#         new_chat = create_new_chat()
#         st.session_state.chats[new_chat["id"]] = new_chat
#         st.session_state.current_chat_id = new_chat["id"]
#     else:
#         # 选择最新的对话
#         latest_chat_id = max(st.session_state.chats.keys(),
#                            key=lambda x: st.session_state.chats[x]["created_at"])
#         st.session_state.current_chat_id = latest_chat_id

# # 侧边栏 - 对话管理
# with st.sidebar:
#     st.markdown("### 对话管理")

#     # 新建对话按钮
#     if st.button("新建对话"):
#         new_chat = create_new_chat()
#         st.session_state.chats[new_chat["id"]] = new_chat
#         st.session_state.current_chat_id = new_chat["id"]
#         save_chats(st.session_state.chats)
#         st.rerun()

#     st.markdown("### 对话历史")

#     # 显示所有对话
#     if st.session_state.chats:
#         # 按创建时间排序
#         sorted_chats = sorted(st.session_state.chats.items(),
#                             key=lambda x: x[1]["created_at"], reverse=True)

#         for chat_id, chat_data in sorted_chats:
#             # 生成对话标题
#             if chat_data["messages"]:
#                 title = get_chat_title(chat_data["messages"])
#                 chat_data["title"] = title

#             # 对话项
#             if st.button(chat_data["title"], key=f"chat_{chat_id}",
#                         help=f"创建时间: {chat_data['created_at']}"
#                         ):
#                 st.session_state.current_chat_id = chat_id
#                 st.rerun()
# ========== 对话历史功能结束 ==========

# ========== 主对话区域 - 简化版本 ==========

# 显示对话历史
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="message-container"><div class="user-message">User: {message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="message-container"><div class="ai-message">Chat: {message["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# 输入框
user_input = st.chat_input(
    "请输入您的问题, 例如: 分析玩家123456789在比赛7891234567中的表现"
)

if user_input:
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 显示用户消息
    st.markdown(
        f'<div class="message-container"><div class="user-message">{user_input}</div></div>',
        unsafe_allow_html=True,
    )

    # AI 处理
    with st.spinner("正在分析中..."):
        try:
            response = agent(user_input, model, tools)
            ai_response = response["messages"][-1].content

            # 添加AI回复
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )

            # 显示AI回复
            st.markdown(
                f'<div class="message-container"><div class="ai-message">🤖 {ai_response}</div></div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            error_msg = f"抱歉，处理您的请求时出现错误：{str(e)}"
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )
            st.markdown(
                f'<div class="message-container"><div class="ai-message">🤖 {error_msg}</div></div>',
                unsafe_allow_html=True,
            )

    st.rerun()

# ========== 原对话历史功能的主对话区域 - 暂时注释 ==========
# # 主对话区域
# current_chat = st.session_state.chats.get(st.session_state.current_chat_id, {})

# if current_chat:
#     # 显示当前对话标题
#     # st.markdown(f"### {current_chat.get('title', '新对话')}")
#     # st.markdown(f"*创建时间: {current_chat.get('created_at', '')}*")

#     # 显示对话历史
#     for message in current_chat.get("messages", []):
#         if message["role"] == "user":
#             st.markdown(f'<div class="message-container"><div class="user-message">User: {message["content"]}</div></div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="message-container"><div class="ai-message">Chat: {message["content"]}</div></div>', unsafe_allow_html=True)

#     # 输入框
#     user_input = st.chat_input("请输入您的问题, 例如: 分析玩家123456789在比赛7891234567中的表现")

#     if user_input:
#         # 添加用户消息到当前对话
#         current_chat["messages"].append({"role": "user", "content": user_input})

#         # 更新对话标题（如果是第一条消息）
#         if len(current_chat["messages"]) == 1:
#             current_chat["title"] = get_chat_title(current_chat["messages"])

#         # 显示用户消息
#         st.markdown(f'<div class="message-container"><div class="user-message">👤 {user_input}</div></div>', unsafe_allow_html=True)

#         # AI 处理
#         with st.spinner("🤖 AI正在分析中..."):
#             try:
#                 response = manual_agent(user_input, model, tools)
#                 ai_response = response['messages'][-1].content

#                 # 添加AI回复到当前对话
#                 current_chat["messages"].append({"role": "assistant", "content": ai_response})

#                 # 显示AI回复
#                 st.markdown(f'<div class="message-container"><div class="ai-message">🤖 {ai_response}</div></div>', unsafe_allow_html=True)

#             except Exception as e:
#                 error_msg = f"抱歉，处理您的请求时出现错误：{str(e)}"
#                 current_chat["messages"].append({"role": "assistant", "content": error_msg})
#                 st.markdown(f'<div class="message-container"><div class="ai-message">🤖 {error_msg}</div></div>', unsafe_allow_html=True)

#         # 保存对话历史
#         st.session_state.chats[st.session_state.current_chat_id] = current_chat
#         save_chats(st.session_state.chats)
#         st.rerun()

# else:
#     st.error("当前对话不存在，请创建新对话")
# ========== 原对话历史功能结束 ==========
