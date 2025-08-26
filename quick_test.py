#!/usr/bin/env python3
"""
快速测试 Stratz Tool
"""

from stratz import get_player_data


def main():
    print("🧪 快速测试 Stratz Tool")
    print("=" * 30)

    # 测试参数
    steam_id = 123456789
    match_id = 7891234567

    print(f"测试参数: steam_id={steam_id}, match_id={match_id}")
    print("-" * 30)

    # 调用 tool
    result = get_player_data(steam_id, match_id)

    print("-" * 30)
    print("📊 测试结果:")

    if result:
        print(f"结果类型: {type(result)}")
        if isinstance(result, dict):
            if "error" in result:
                print(f"❌ 错误: {result['error']}")
                if "details" in result:
                    print(f"详情: {result['details']}")
            else:
                print("✅ 成功获取数据")
                print("数据结构:")
                for key in result.keys():
                    print(f"  - {key}")
    else:
        print("❌ 返回 None")


if __name__ == "__main__":
    main()
