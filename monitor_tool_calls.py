#!/usr/bin/env python3
"""
实时监控 Tool 调用
用于在 Streamlit 应用运行时监控 tool 的调用情况
"""

import sys
import time
from datetime import datetime


class ToolCallMonitor:
    def __init__(self):
        self.call_count = 0
        self.start_time = datetime.now()

    def log_call(self, tool_name, args, result):
        self.call_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n🔧 [{timestamp}] Tool 调用 #{self.call_count}")
        print(f"工具名称: {tool_name}")
        print(f"参数: {args}")
        print(f"结果类型: {type(result)}")

        if isinstance(result, dict):
            if "error" in result:
                print(f"❌ 错误: {result['error']}")
            else:
                print("✅ 成功")
        elif result is None:
            print("⚠️  返回 None")
        else:
            print("✅ 返回数据")

        print("-" * 50)


# 全局监控器实例
monitor = ToolCallMonitor()


def patch_get_player_data():
    """给 get_player_data 添加监控"""
    from stratz import get_player_data

    original_func = get_player_data.func

    def monitored_func(steam_id: int, match_id: int):
        args = {"steam_id": steam_id, "match_id": match_id}
        result = original_func(steam_id, match_id)
        monitor.log_call("get_player_data", args, result)
        return result

    # 替换原函数
    get_player_data.func = monitored_func

    print("✅ Tool 监控已启用")


def main():
    print("🔍 Tool 调用监控器")
    print("=" * 50)
    print("监控 get_player_data tool 的调用情况")
    print("按 Ctrl+C 停止监控")
    print("=" * 50)

    # 启用监控
    patch_get_player_data()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        duration = datetime.now() - monitor.start_time
        print(f"\n\n📊 监控统计:")
        print(f"监控时长: {duration}")
        print(f"总调用次数: {monitor.call_count}")
        print("监控已停止")


if __name__ == "__main__":
    main()
