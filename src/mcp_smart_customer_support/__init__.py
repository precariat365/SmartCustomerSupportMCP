import asyncio

from . import mcp_server


def main():
    """Main entry point for the package."""
    import sys
    print("start ……")
    # 根据命令行参数选择启动模式
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # 标准输入输出模式
        asyncio.run(mcp_server.run_stdio())
    else:
        # 默认 SSE 模式
        mcp_server.run_sse()


__all__ = ["main", "mcp_server"]
