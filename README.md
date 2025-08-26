# 🔥 DOTA2 锐评小助手 🎮

一个基于AI的DOTA2赛后表现分析工具，专业分析 · 犀利点评 · 网络用语拉满！

## ✨ 功能特色

### 🎯 三种锐评模式
- **综合分析模式**: 客观专业的数据分析，指出优缺点和改进建议
- **彩虹屁模式**: 疯狂夸奖玩家表现，网络用语拉满，让你感觉自己就是电竞天才
- **毒舌模式**: 犀利吐槽玩家表现，幽默风趣不过分，让人笑出声

### 📊 数据分析
- 获取详细的比赛数据（击杀、死亡、助攻、经济、补刀等）
- 智能分析玩家表现和操作亮点
- 对比队友和对手数据
- 提供专业的改进建议

### 🎨 用户体验
- 现代化的Streamlit界面
- 响应式设计，支持暗色模式
- 快速分析功能，一键生成锐评
- 智能对话，自动识别分析模式

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit
- 相关依赖包

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd dota2-review-assistant
```

2. 安装依赖
```bash
pip install streamlit langchain langchain-openai langchain-community
pip install langgraph python-dotenv cloudscraper requests
```

3. 配置环境变量
创建 `.env` 文件并添加：
```
OPENAI_API_KEY=your_openai_api_key
STRATZ_API_KEY=your_stratz_api_key
```

4. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的API密钥
# OPENAI_API_KEY=your_openai_api_key
# STRATZ_API_KEY=your_stratz_api_key
```

5. 测试配置（可选）
```bash
# 完整配置测试
python test_config.py

# 快速测试 Stratz Tool
python quick_test.py

# 详细的 Tool 验证
python test_stratz_tool.py
```

6. 运行应用
```bash
# 方式1: 使用启动脚本（推荐）
python run.py

# 方式2: 直接运行Streamlit
streamlit run streamlit_app.py
```

## 📖 使用说明

### 快速分析
1. 在侧边栏输入玩家Steam ID
2. 输入比赛ID
3. 选择锐评模式（综合分析/彩虹屁模式/毒舌模式）
4. 点击"开始锐评"

### 对话分析
直接在聊天框输入问题，AI会智能识别你的意图：
- 包含"夸"、"吹"、"厉害"等词汇 → 自动切换到彩虹屁模式
- 包含"批评"、"吐槽"、"菜"等词汇 → 自动切换到毒舌模式
- 其他情况 → 使用综合分析模式

### 示例输入
```
分析玩家123456789在比赛7891234567中的表现
夸夸玩家123456789在比赛7891234567中的神仙操作
吐槽一下玩家123456789在比赛7891234567中的菜鸡操作
```

## 🛠️ 技术架构

### 核心组件
- **streamlit_app.py**: 前端界面和用户交互
- **agent.py**: AI分析引擎，包含三种不同的分析模式
- **stratz.py**: DOTA2数据获取工具，调用Stratz API

### AI模型
- 使用GLM-4-Flash模型进行自然语言处理
- 基于LangChain框架构建智能代理
- 支持工具调用和多轮对话

### 数据来源
- Stratz API: 获取详细的比赛和玩家数据
- 支持实时数据查询和历史数据分析

## 🎨 界面预览

- 🌈 现代化的渐变色设计
- 💬 类似聊天软件的对话界面
- 📱 响应式布局，支持移动端
- 🌙 自动适配暗色模式

## 🔧 配置说明

### API密钥配置
需要获取以下API密钥：
1. **OpenAI API Key**: 用于AI模型调用（支持智谱GLM-4-Flash）
2. **Stratz API Key**: 用于获取DOTA2数据

### 环境变量
在 `.env` 文件中配置：
```
OPENAI_API_KEY=your_openai_api_key
STRATZ_API_KEY=your_stratz_api_key
```

## 🎯 核心功能详解

### 数据获取模块 (stratz.py)
```python
@tool
def get_player_data(steam_id: int, match_id: int):
    """获取玩家在指定比赛中的详细数据"""
    # 通过GraphQL查询获取比赛数据
    # 包括KDA、经济、伤害、英雄信息等
```

### AI分析引擎 (agent.py)
```python
# 三种不同的分析模式
def agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    """综合分析模式 - 客观专业"""

def praise_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    """彩虹屁模式 - 疯狂夸奖"""

def roast_agent(content: str, model: ChatOpenAI, tools: list[tool]) -> dict:
    """毒舌模式 - 犀利吐槽"""
```

### 数据指标体系
- **战斗表现**: KDA、伤害输出、支援能力
- **经济发展**: 补刀效率、净资产、等级
- **英雄信息**: 英雄选择、装备搭配
- **时间维度**: 比赛时长、发育节奏

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License

## 🎯 未来计划

- [ ] 支持更多游戏数据源
- [ ] 添加数据可视化图表
- [ ] 支持批量分析多场比赛
- [ ] 添加玩家历史表现趋势分析
- [ ] 支持自定义锐评风格
- [ ] 添加语音播报功能
- [ ] 支持团队分析和对比
- [ ] 添加英雄特定的评价标准

## 🔧 故障排除

### 常见问题

**Q: 出现 "create_react_agent() got an unexpected keyword argument" 错误**
A: 这是LangChain版本兼容性问题，已在最新代码中修复。请确保使用最新版本的代码。

**Q: API连接失败**
A: 
1. 检查 `.env` 文件是否正确配置
2. 确认API密钥有效且有足够的配额
3. 运行 `python test_config.py` 进行诊断

**Q: Stratz API返回空数据**
A: 
1. 确认玩家ID和比赛ID格式正确
2. 检查比赛是否存在且为公开比赛
3. 确认Stratz API密钥权限
4. 运行 `python quick_test.py` 查看详细错误信息

**Q: 如何验证 Tool 是否被正确调用**
A:
1. 运行 `python test_stratz_tool.py` 进行完整验证
2. 查看控制台输出中的 `[TOOL]` 标记
3. 使用 `python monitor_tool_calls.py` 实时监控调用

**Q: 界面显示异常**
A: 
1. 清除浏览器缓存
2. 尝试无痕模式
3. 检查Streamlit版本是否兼容

### 获取API密钥

**智谱AI (GLM-4-Flash)**
1. 访问 https://open.bigmodel.cn/
2. 注册账号并实名认证
3. 创建API密钥

**Stratz API**
1. 访问 https://stratz.com/
2. 注册账号
3. 在开发者页面申请API密钥

---

**让AI帮你分析DOTA2表现，专业锐评，网络用语拉满！** 🔥

## 🔥 锐评示例

### 彩虹屁模式示例
> "兄弟你这波操作简直绝绝子！15个击杀YYDS，这伤害打得对面怀疑人生，纯纯的carry全场！这就是传说中的电竞天才吧，我上我真不行！"

### 毒舌模式示例  
> "兄弟，这0-10-2的战绩是认真的吗？补刀被对面压了一倍，这经济差距我都不好意思说。不过没关系，菜是原罪，但菜得这么有特色也是一种天赋！"

### 综合分析示例
> "本场比赛表现中规中矩，KDA为8-3-12，参团率较高。补刀效率需要提升，建议加强对线期的基本功练习。团战定位不错，但需要注意走位避免不必要的死亡。"