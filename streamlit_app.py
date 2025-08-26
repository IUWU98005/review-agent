import streamlit as st
from dotenv import load_dotenv
from agent import agent, model, tools, praise_agent, roast_agent

load_dotenv()

st.set_page_config(
    page_title="DOTA2 锐评小助手",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 简洁的消息样式 */
    .user-message {
        background-color: #f0f0f0;
        color: #333;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.9rem;
        line-height: 1.4;
        border: 1px solid #e0e0e0;
    }
    
    .ai-message {
        background-color: #ffffff;
        color: #333;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 0.9rem;
        line-height: 1.5;
        border: 1px solid #e0e0e0;
    }
    
    .message-container {
        margin: 12px 0;
        display: flex;
        flex-direction: column;
    }
    
    .user-container {
        align-items: flex-end;
    }
    
    .ai-container {
        align-items: flex-start;
    }
    
    /* 暗色模式 */
    [data-theme="dark"] .user-message {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border-color: #404040;
    }
    
    [data-theme="dark"] .ai-message {
        background-color: #1a1a1a;
        color: #e0e0e0;
        border-color: #404040;
    }
    
    /* 简化按钮样式 */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #d0d0d0;
        background-color: #ffffff;
        color: #333;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #f5f5f5;
        border-color: #b0b0b0;
    }
    
    /* 主按钮样式 */
    .stButton > button[kind="primary"] {
        background-color: #007acc;
        color: white;
        border-color: #007acc;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #005a9e;
        border-color: #005a9e;
    }
    
    /* 输入框简化 */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #d0d0d0;
        padding: 8px 12px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 6px;
        border: 1px solid #d0d0d0;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("DOTA2 锐评小助手")
st.caption("专业分析玩家表现，支持多种评价风格")

# ========== 简化的会话状态管理 ==========
# 初始化简单的消息历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 快速分析区域 ==========
with st.expander("快速分析", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        player_id = st.text_input("玩家Steam ID", placeholder="123456789")

    with col2:
        match_id = st.text_input("比赛ID", placeholder="7891234567")

    analysis_mode = st.selectbox(
        "分析模式", ["综合分析", "彩虹屁模式", "毒舌模式"], index=0
    )

    if st.button("开始分析", type="primary"):
        if player_id and match_id:
            if analysis_mode == "综合分析":
                query = f"分析玩家{player_id}在比赛{match_id}中的表现"
            elif analysis_mode == "彩虹屁模式":
                query = (
                    f"夸奖玩家{player_id}在比赛{match_id}中的亮眼表现，用网络用语吹爆他"
                )
            else:
                query = (
                    f"批评玩家{player_id}在比赛{match_id}中的表现，用网络用语狠狠吐槽"
                )

            st.session_state.quick_query = query
            st.rerun()
        else:
            st.error("请输入玩家ID和比赛ID")

# 清除对话按钮
if st.session_state.messages:
    if st.button("清除对话"):
        st.session_state.messages = []
        st.rerun()


# ========== 主对话区域 ==========

# 处理快速查询
if hasattr(st.session_state, "quick_query"):
    user_input = st.session_state.quick_query
    delattr(st.session_state, "quick_query")

    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 确定使用哪个agent
    if "夸奖" in user_input or "吹爆" in user_input:
        agent_func = praise_agent
    elif "批评" in user_input or "吐槽" in user_input:
        agent_func = roast_agent
    else:
        agent_func = agent

    # AI 处理
    with st.spinner("正在分析中..."):
        try:
            response = agent_func(user_input, model, tools)
            ai_response = response["messages"][-1].content

            # 添加AI回复
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )

        except Exception as e:
            error_msg = f"抱歉，处理您的请求时出现错误：{str(e)}"
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )

    st.rerun()

# 如果没有对话历史，显示简单说明
if not st.session_state.messages:
    st.info("💡 输入问题开始对话，或使用上方的快速分析功能")

    with st.expander("使用示例"):
        st.markdown(
            """
        **综合分析：** 分析玩家123456789在比赛7891234567中的表现
        
        **彩虹屁模式：** 夸夸玩家123456789的神仙操作
        
        **毒舌模式：** 吐槽玩家123456789的菜鸡表现
        """
        )

# 显示对话历史
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="message-container user-container"><div class="user-message">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="message-container ai-container"><div class="ai-message">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# 输入框
user_input = st.chat_input("输入你的问题...")

if user_input:
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 智能判断使用哪个agent
    if any(
        keyword in user_input for keyword in ["夸", "吹", "彩虹屁", "厉害", "牛", "强"]
    ):
        agent_func = praise_agent
    elif any(
        keyword in user_input for keyword in ["批评", "吐槽", "菜", "差", "垃圾", "坑"]
    ):
        agent_func = roast_agent
    else:
        agent_func = agent

    # AI 处理
    with st.spinner("正在分析中..."):
        try:
            response = agent_func(user_input, model, tools)
            ai_response = response["messages"][-1].content

            # 添加AI回复
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )

        except Exception as e:
            error_msg = f"抱歉，处理您的请求时出现错误：{str(e)}"
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )

    st.rerun()
