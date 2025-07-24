## 项目概述

本项目是一个基于 LangChain 框架开发的智能体系统，专门用于分析和评价 Dota2 玩家在特定比赛中的表现。系统通过调用 STRATZ API 获取玩家比赛数据，并利用大语言模型对玩家的游戏表现进行专业、犀利的分析和评价。

项目地址：<https://github.com/IUWU98005/dota2-player-review>

## 技术架构

### 核心技术栈

- LangChain : 智能体框架和工具链
- LangGraph : 用于创建 ReAct 智能体
- OpenAI API : 大语言模型服务（支持智谱 GLM-4-Flash）
- DeepSeek API : 用于生成玩家表现评价
- STRATZ API : Dota2 比赛数据源
- CloudScraper : 处理反爬虫机制

### 项目结构

```bash
dota2-player-review/
├── .gitignore          # Git 忽略文件配置
├── agent.py            # LangChain 智能体核心模块
├── analysis.py         # 玩家表现分析模块
└── stratz.py          # STRATZ API 数据获取工具
```

## 核心模块详解

### 1. 智能体模块 (agent.py)

`agent.py` 是项目的核心智能体模块，主要功能包括：

```python
import os
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from stratz import get_player_data

# 模型配置
model = ChatOpenAI(
    model="glm-4-flash",
    openai_api_base = "https://open.bigmodel.cn/api/paas/v4",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 工具集成
tools = [DuckDuckGoSearchRun(), get_player_data]

# 手动智能体函数
def manual_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    agent = create_react_agent(model, tools)
    resp = agent.invoke({"messages": [HumanMessage(content)]})
    return resp
```

特性：

- 集成智谱 GLM-4-Flash 模型
- 支持 DuckDuckGo 搜索工具
- 集成自定义的 Dota2 数据获取工具
- 使用 LangGraph 的 ReAct 智能体架构

### 2. 数据获取模块 (stratz.py)

`stratz.py` 负责从 STRATZ API 获取 Dota2 比赛数据：

```python
@tool
def get_player_data(steam_id: int, match_id: int):
    """
    获取玩家在指定比赛中的数据
    :param steam_id: 玩家的 steam id
    :param match_id: 比赛 id
    :return: 包含玩家数据的字典
    """
    # GraphQL 查询
    query = """
    query GetRecentMatches($id: Long!, $steamAccountId: Long!){
        match(id: $id) {
            durationSeconds
            players(steamAccountId: $steamAccountId) {
                playerSlot
                kills
                deaths
                assists
                networth
                numLastHits
                numDenies
                level
                heroDamage
                towerDamage
                heroHealing
            }
        }
    }
    """
```

功能特点：

- 使用 @tool 装饰器集成到 LangChain 工具链
- 通过 GraphQL 查询获取详细的比赛数据
- 使用 CloudScraper 绕过反爬虫机制
- 获取包括 KDA、经济、伤害等关键指标

### 3. 分析评价模块 (analysis.py)

`analysis.py` 实现玩家表现的智能分析：

```python
def review_player(steam_id: int, match_id: int):
    player_data = stratz.get_player_data(steam_id, match_id)
    
    # 构建分析提示词
    prompt = f"""
    请根据以下Dota2比赛数据, 专业、犀利地评价该玩家的表现, 指出优点和不足, 并给出改进建议：
    - 击杀: {player['kills']}
    - 死亡: {player['deaths']}
    - 助攻: {player['assists']}
    - 补刀: {player['numLastHits']}
    - 反补: {player['numDenies']}
    - 等级: {player['level']}
    - 净资产: {player['networth']}
    - 英雄伤害: {player['heroDamage']}
    - 建筑伤害: {player['towerDamage']}
    - 治疗量: {player['heroHealing']}
    - 比赛时长: {match['durationSeconds']//60}分{match['durationSeconds']%60}秒
    """
    
    # 调用 DeepSeek API 生成评价
    # ... API 调用逻辑
```

核心功能：

- 整合比赛数据生成结构化分析提示
- 调用 DeepSeek API 进行智能分析
- 提供专业的游戏表现评价和改进建议

## 数据指标体系

系统分析的核心数据指标包括：

### 战斗表现

- KDA : 击杀(kills)、死亡(deaths)、助攻(assists)
- 伤害输出 : 英雄伤害(heroDamage)、建筑伤害(towerDamage)
- 支援能力 : 治疗量(heroHealing)

### 经济发展

- 补刀效率 : 正补(numLastHits)、反补(numDenies)
- 经济状况 : 净资产(networth)、等级(level)

### 时间维度

- 比赛时长 : 用于计算效率指标
- 发育节奏 : 结合时长分析经济和等级发展

## 环境配置

### 必需的环境变量

```env
# .env 文件配置
OPENAI_API_KEY=your_zhipu_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
STRATZ_API_KEY=your_stratz_api_key
STEAM_ACCOUNT_ID=your_steam_id
MATCH_ID=target_match_id
```

依赖安装

```bash
pip install langchain langchain-openai langchain-community
pip install langgraph python-dotenv cloudscraper requests
```

## 使用方式

1. 直接分析模式

    ```python
    from analysis import review_player
    import os

    steam_id = int(os.getenv("STEAM_ACCOUNT_ID"))
    match_id = int(os.getenv("MATCH_ID"))
    review = review_player(steam_id, match_id)
    print("AI锐评:", review)
    ```

2. 智能体交互模式

    ```python
    from agent import manual_agent, model, tools

    query = "分析玩家 123456789 在比赛 7891234567 中的表现"
    response = manual_agent(query, model, tools)
    print(response)
    ```

## 技术亮点

### 1. 智能体架构设计

- 采用 LangGraph 的 ReAct 模式，支持推理-行动-观察循环
- 工具链集成，支持搜索和数据获取的组合使用
- 模块化设计，易于扩展新的分析工具

### 2. 多模型集成

- 智谱 GLM-4-Flash: 用于智能体推理和工具调用
- DeepSeek: 专门用于生成专业的游戏分析评价
- 模型选择针对不同任务进行优化

### 3. 数据获取优化

- 使用 CloudScraper 处理反爬虫机制
- GraphQL 查询精确获取所需数据字段
- 错误处理和数据验证机制

## 扩展方向

### 1. 功能扩展

- 支持多场比赛的综合分析
- 添加英雄特定的评价标准
- 集成更多游戏数据源（如 OpenDota）

### 2. 分析深度

- 引入机器学习模型进行表现预测
- 添加与职业选手的对比分析
- 实现团队配合度分析

### 3. 用户体验

- 开发 Web 界面
- 支持批量分析和报告生成
- 添加可视化图表展示

## 总结

本项目展示了如何使用 LangChain 框架构建专业的游戏数据分析智能体。通过整合多个 API 服务和大语言模型，实现了从数据获取到智能分析的完整流程。项目架构清晰，模块化程度高，为游戏数据分析领域的 AI 应用提供了良好的参考实现。

该系统不仅能够提供客观的数据分析，还能生成具有专业性和针对性的改进建议，为 Dota2 玩家的技能提升提供了有价值的工具支持。
