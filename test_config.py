#!/usr/bin/env python3
"""
配置测试脚本 - 验证API连接和配置是否正确
"""

import os
from dotenv import load_dotenv


def test_env_config():
    """测试环境变量配置"""
    print("🔧 测试环境变量配置...")

    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    stratz_key = os.getenv("STRATZ_API_KEY")

    if not openai_key:
        print("❌ OPENAI_API_KEY 未配置")
        return False
    else:
        print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...")

    if not stratz_key:
        print("❌ STRATZ_API_KEY 未配置")
        return False
    else:
        print(f"✅ STRATZ_API_KEY: {stratz_key[:10]}...")

    return True


def test_openai_connection():
    """测试OpenAI API连接"""
    print("\n🤖 测试OpenAI API连接...")

    try:
        from langchain_openai import ChatOpenAI

        model = ChatOpenAI(
            model="glm-4-flash",
            openai_api_base="https://open.bigmodel.cn/api/paas/v4",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        response = model.invoke("测试连接")
        print("✅ OpenAI API连接成功")
        print(f"响应: {response.content[:50]}...")
        return True

    except Exception as e:
        print(f"❌ OpenAI API连接失败: {e}")
        return False


def test_stratz_connection():
    """测试Stratz API连接"""
    print("\n📊 测试Stratz API连接...")

    try:
        from stratz import get_player_data

        # 使用一个示例ID进行测试（这个可能会失败，但能测试API连接）
        result = get_player_data(123456789, 7891234567)

        if result is None:
            print("⚠️  Stratz API连接成功，但示例数据未找到（这是正常的）")
        else:
            print("✅ Stratz API连接成功并获取到数据")

        return True

    except Exception as e:
        print(f"❌ Stratz API连接失败: {e}")
        return False


def test_imports():
    """测试必要的包导入"""
    print("\n📦 测试包导入...")

    packages = [
        "streamlit",
        "langchain",
        "langchain_openai",
        "langchain_community",
        "langgraph",
        "dotenv",
        "cloudscraper",
        "requests",
    ]

    success = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 请运行: pip install {package}")
            success = False

    return success


def main():
    """主测试函数"""
    print("🔥 DOTA2 锐评小助手 - 配置测试")
    print("=" * 50)

    all_tests_passed = True

    # 测试包导入
    if not test_imports():
        all_tests_passed = False

    # 测试环境变量
    if not test_env_config():
        all_tests_passed = False

    # 测试API连接
    if not test_openai_connection():
        all_tests_passed = False

    if not test_stratz_connection():
        all_tests_passed = False

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 所有测试通过！可以启动应用了")
        print("运行命令: python run.py 或 streamlit run streamlit_app.py")
    else:
        print("❌ 部分测试失败，请检查配置")

    return all_tests_passed


if __name__ == "__main__":
    main()
