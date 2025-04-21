import asyncio

from src.mcp_smart_customer_support.mcp_server  import run_stdio, run_sse

if __name__ == "__main__":
    import sys

    # 根据命令行参数选择启动模式
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # 标准输入输出模式
        asyncio.run(run_stdio())
    else:
        # 默认 SSE 模式
        run_sse()