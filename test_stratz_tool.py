#!/usr/bin/env python3
"""
Stratz Tool 验证脚本
用于测试 stratz.py 中的 get_player_data tool 是否正确工作
"""

import os
import json
from dotenv import load_dotenv
from stratz import get_player_data
from agent import agent, model, tools


def test_direct_tool_call():
    """直接测试 tool 调用"""
    print("🔧 测试直接调用 get_player_data tool...")

    # 使用示例数据进行测试
    test_steam_id = 123456789
    test_match_id = 7891234567

    try:
        result = get_player_data(test_steam_id, test_match_id)

        if result is None:
            print("❌ Tool 返回 None - 可能是API密钥问题或数据不存在")
            return False

        print("✅ Tool 调用成功!")
        print(f"返回数据类型: {type(result)}")

        if isinstance(result, dict):
            print("📊 返回数据结构:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500] + "...")

        return True

    except Exception as e:
        print(f"❌ Tool 调用失败: {e}")
        return False


def test_tool_in_agent():
    """测试 tool 在 agent 中的调用"""
    print("\n🤖 测试 tool 在 agent 中的调用...")

    test_query = "分析玩家123456789在比赛7891234567中的表现"

    try:
        # 启用详细日志
        import logging

        logging.basicConfig(level=logging.DEBUG)

        response = agent(test_query, model, tools)

        print("✅ Agent 调用成功!")
        print(f"响应消息数量: {len(response['messages'])}")

        # 检查是否有工具调用
        for i, message in enumerate(response["messages"]):
            print(f"\n消息 {i+1}:")
            print(f"类型: {type(message)}")

            # 检查是否有工具调用
            if hasattr(message, "tool_calls") and message.tool_calls:
                print(f"🔧 发现工具调用: {len(message.tool_calls)} 个")
                for j, tool_call in enumerate(message.tool_calls):
                    print(f"  工具 {j+1}: {tool_call}")

            # 显示消息内容
            if hasattr(message, "content") and message.content:
                content = (
                    message.content[:200] + "..."
                    if len(message.content) > 200
                    else message.content
                )
                print(f"内容: {content}")

        return True

    except Exception as e:
        print(f"❌ Agent 调用失败: {e}")
        return False


def test_api_connection():
    """测试 Stratz API 连接"""
    print("\n🌐 测试 Stratz API 连接...")

    load_dotenv()
    api_key = os.getenv("STRATZ_API_KEY")

    if not api_key:
        print("❌ 未找到 STRATZ_API_KEY 环境变量")
        return False

    print(f"✅ API Key 已配置: {api_key[:10]}...")

    import cloudscraper

    url = "https://api.stratz.com/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 简单的测试查询
    test_query = """
    query {
        __schema {
            types {
                name
            }
        }
    }
    """

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url=url, headers=headers, json={"query": test_query})

        if response.status_code == 200:
            print("✅ Stratz API 连接成功!")
            return True
        else:
            print(f"❌ API 响应错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False


def test_tool_registration():
    """测试 tool 是否正确注册到 agent"""
    print("\n📋 测试 tool 注册...")

    from agent import tools

    print(f"已注册的工具数量: {len(tools)}")

    for i, tool in enumerate(tools):
        print(f"工具 {i+1}:")
        print(f"  名称: {tool.name}")
        print(f"  描述: {tool.description}")
        print(f"  参数: {getattr(tool, 'args_schema', 'N/A')}")

    # 检查是否包含 get_player_data
    tool_names = [tool.name for tool in tools]
    if "get_player_data" in tool_names:
        print("✅ get_player_data tool 已正确注册")
        return True
    else:
        print("❌ get_player_data tool 未找到")
        print(f"可用工具: {tool_names}")
        return False


def main():
    """主测试函数"""
    print("🔥 Stratz Tool 验证测试")
    print("=" * 50)

    tests = [
        ("API连接测试", test_api_connection),
        ("Tool注册测试", test_tool_registration),
        ("直接Tool调用测试", test_direct_tool_call),
        ("Agent中Tool调用测试", test_tool_in_agent),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")

    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 所有测试通过! Stratz tool 工作正常")
    else:
        print("\n⚠️  部分测试失败，请检查配置和实现")

    return all_passed


if __name__ == "__main__":
    main()
