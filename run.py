#!/usr/bin/env python3
"""
DOTA2 锐评小助手启动脚本
"""

import os
import sys
import subprocess


def check_requirements():
    """检查必要的依赖是否已安装"""
    try:
        import streamlit
        import langchain
        import dotenv

        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def check_env_file():
    """检查环境变量文件是否存在"""
    if not os.path.exists(".env"):
        print("❌ 未找到 .env 文件")
        print("请复制 .env.example 为 .env 并配置你的API密钥")
        return False

    from dotenv import load_dotenv

    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 未配置 OPENAI_API_KEY")
        return False

    if not os.getenv("STRATZ_API_KEY"):
        print("❌ 未配置 STRATZ_API_KEY")
        return False

    print("✅ 环境变量配置正确")
    return True


def main():
    """主函数"""
    print("🔥 DOTA2 锐评小助手启动中...")
    print("=" * 50)

    # 检查依赖
    if not check_requirements():
        sys.exit(1)

    # 检查环境变量
    if not check_env_file():
        sys.exit(1)

    print("🚀 启动Streamlit应用...")
    print("=" * 50)

    # 启动Streamlit应用
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "streamlit_app.py",
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
