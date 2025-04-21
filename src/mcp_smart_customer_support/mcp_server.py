import json
import logging
from typing import Any, Dict

import uvicorn
from mcp import types
from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.server.sse import SseServerTransport
from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from .human_customer_service import HumanCustomerService
from .order_operations import OrderOperations
from .product_knowledge import ProductKnowledgeBase

SYSTEM_PROMPT = """你是一个智能客服，能够通过 MCP 快速获取相关信息，回答客户关于产品的问题。对于复杂问题，能够自动转接给人工客服，并提供客户的基本信息和问题描述。"""

logger = logging.getLogger('mcp_server')
logger.info("Starting MCP Server")

server = Server("mcp-smart-customer-support")


async def main():
    # Register handlers
    logger.debug("Registering handlers")


async def init_prompts():
    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        logger.debug("Handling list_prompts request")
        return [
            types.Prompt(
                name="query_product_info",
                description="当用户询问产品详细信息时，可使用产品知识库资源来回答。引导用户表述‘查询产品信息：产品名称’",
                arguments=[
                    types.PromptArgument(
                        name="product_name",
                        description="要查询的产品名称，如产品A、产品B",
                        required=True,
                    )
                ],
            ),
            types.Prompt(
                name="check_order_status",
                description="若用户想了解订单状态，调用订单查询工具。引导用户表述‘查询订单状态：客户 ID’",
                arguments=[
                    types.PromptArgument(
                        name="customer_id",
                        description="客户的唯一标识 ID",
                        required=True,
                    )
                ],
            ),
            types.Prompt(
                name="handle_after_sales",
                description="遇到产品售后问题时，结合产品知识库和订单信息处理。引导用户表述‘售后问题：产品名称，问题描述’",
                arguments=[
                    types.PromptArgument(
                        name="product_name",
                        description="出现售后问题的产品名称",
                        required=True,
                    ),
                    types.PromptArgument(
                        name="issue_description",
                        description="对售后问题的详细描述",
                        required=True,
                    )
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: Dict[str, str] | None) -> types.GetPromptResult:
        logger.debug(f"Handling get_prompt request for {name} with args {arguments}")
        valid_prompts = [
            "query_product_info",
            "check_order_status",
            "handle_after_sales"
        ]
        if name not in valid_prompts:
            logger.error(f"Unknown prompt: {name}")
            raise ValueError(f"Unknown prompt: {name}")

        if name == "query_product_info":
            if not arguments or "product_name" not in arguments:
                logger.error("Missing required argument: product_name")
                raise ValueError("Missing required argument: product_name")
            product_name = arguments["product_name"]
            prompt = f"用户想了解产品 {product_name} 的详细信息，请使用产品知识库资源进行回答。"
            description = f"根据用户需求，查询 {product_name} 的详细信息"

        elif name == "check_order_status":
            if not arguments or "customer_id" not in arguments:
                logger.error("Missing required argument: customer_id")
                raise ValueError("Missing required argument: customer_id")
            customer_id = arguments["customer_id"]
            prompt = f"用户想了解客户 ID 为 {customer_id} 的订单状态，请调用订单查询工具进行查询。"
            description = f"查询客户 ID 为 {customer_id} 的订单状态"

        elif name == "handle_after_sales":
            if not arguments or "product_name" not in arguments or "issue_description" not in arguments:
                logger.error("Missing required arguments: product_name, issue_description")
                raise ValueError("Missing required arguments: product_name, issue_description")
            product_name = arguments["product_name"]
            issue_description = arguments["issue_description"]
            prompt = f"用户反馈产品 {product_name} 出现售后问题：{issue_description}，请结合产品知识库和订单信息进行处理。"
            description = f"处理产品 {product_name} 的售后问题：{issue_description}"

        logger.debug(f"Generated prompt template for topic: {name}")
        return types.GetPromptResult(
            description=description,
            messages=[
                types.PromptMessage(
                    role="assistant",
                    content=types.TextContent(type="text", text=prompt.strip()),
                )
            ],
        )


async def init_resources():
    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        logger.debug("Handling list_resources request")
        return [
            types.Resource(
                uri=AnyUrl("knowledge://product"),
                name="产品列表",
                description="产品知识库，包含产品特点、使用方法、技术参数、售后流程等产品相关信息",
                mimeType="application/json;charset=utf-8",
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        if uri.scheme != "knowledge":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        path = str(uri).replace("knowledge://", "")

        if path == "product":
            # 获取产品信息
            knowledge = ProductKnowledgeBase().get_all_product_info()
            return json.dumps(knowledge, ensure_ascii=False)
        else:
            logger.error(f"Unknown resource path: {path}")
            raise ValueError(f"Unknown resource path: {path}")


async def init_tools():
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="read_customer_orders",
                description="根据客户 ID 查询客户的订单信息，如购买产品、订单日期、订单状态等。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string",
                                        "description": "客户ID，需由客户提供或通过Oauth2登录获取"},
                    },
                    "required": ["customer_id"],
                },
            ),
            types.Tool(
                name="transfer_to_human",
                description="当遇到复杂问题或机器人无法完整解答时，触发人工转接流程，将客户 ID、订单详情、问题描述等信息传递给人工客服系统。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string",
                                        "description": "客户ID"},
                        "question": {"type": "string",
                                     "description": "客户问题"},
                        "order_info": {"type": "string",
                                       "description": "客户订单信息"}
                    },
                    "required": ["customer_id", "question", "order_info"],
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        try:
            """获取订单信息"""
            if name == "read_customer_orders":
                if not arguments["customer_id"].strip().upper():
                    raise ValueError("Only inline_article_url allowed for query")
                results = OrderOperations().get_customer_orders(arguments["customer_id"])
                return [types.TextContent(type="text", text=str(results))]
            """转人工服务"""
            if name == "transfer_to_human":
                customer_id = arguments["customer_id"]
                question = arguments["question"]
                order_info = arguments["order_info"]
                results = HumanCustomerService().handle_transfer(customer_id, question, order_info)
                return [types.TextContent(type="text", text=str(results))]

            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def run_stdio():
    """运行标准输入输出模式的服务器

    使用标准输入输出流(stdio)运行服务器，主要用于命令行交互模式

    Raises:
        Exception: 当服务器运行出错时抛出异常
    """
    from mcp.server.stdio import stdio_server
    await init_prompts()
    await init_resources()
    await init_tools()

    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server running with stdio transport")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp_smart_customer_support",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                )
            )
    except Exception as e:
        logger.error(f"服务器运行错误: {str(e)}")
        raise


def run_sse():
    """运行SSE(Server-Sent Events)模式的服务器

    启动一个支持SSE的Web服务器，允许客户端通过HTTP长连接接收服务器推送的消息
    服务器默认监听0.0.0.0:9000
    """

    async def startup():
        await init_tools()

    async def auth_middleware(request, call_next):
        """认证中间件

        验证请求中的认证信息，确保只有合法用户可以访问SSE服务
        """
        # 从请求头中获取认证token
        auth_token = request.headers.get('Authorization')

        # 验证token (这里需要根据实际需求实现token验证逻辑)
        if not verify_token(auth_token):
            return PlainTextResponse('Invalid token', status_code=401)

        response = await call_next(request)
        return response

    def verify_token(token: str) -> bool:
        """验证token的有效性

        Args:
            token: 待验证的token字符串

        Returns:
            bool: token是否有效
        """
        # 这里实现具体的token验证逻辑
        # 可以使用JWT、数据库验证等方式
        return True  # 临时返回True，需要替换为实际的验证逻辑

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        """处理SSE连接请求

        Args:
            request: HTTP请求对象
        """
        async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
            await server.run(
                streams[0],
                streams[1],
                InitializationOptions(
                    server_name="mcp_smart_customer_support",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                )
            )

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message)
        ],
        on_startup=[startup],
        middleware=[
            Middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
        ]
    )
    try:
        uvicorn.run(starlette_app, host="0.0.0.0", port=9000)
    except Exception as e:
        logger.error(f"SSE服务器运行错误: {str(e)}")
        raise
