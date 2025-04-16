# 智能客服示例

这是一个基于MCP框架的智能客服系统示例项目，用于演示如何构建和部署智能客服应用。

## 功能特点

- 智能问答服务
- 人工客服转接
- 订单信息查询
- 产品知识库管理

## 系统要求

- Python >= 3.10
- MCP框架 >= 1.6.0

## 安装

1. 创建并激活虚拟环境（推荐）：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install .
```

## 使用方法

1. 使用inspector：
```bash
npx @modelcontextprotocol/inspector uv --directory /opt/apps/python_project/SmartCustomerSupportMCP run mcp-smart-customer-support
```

2. 使用Vscode或Claude等桌面应用
```json
{
  "mcpServers": {
    "SmartCustomerSupportMCP": {
    "command": "uv",
    "args": [
      "--directory", 
    "/opt/apps/python_project/SmartCustomerSupportMCP",
      "run",
      "mcp-smart-customer-support"
    ]}
  }
}
```

## 项目结构

```
src/mcp_smart_customer_support/
├── __init__.py          # 包初始化文件
├── mcp_server.py        # MCP服务器实现
├── human_customer_service.py  # 人工客服处理模块
├── order_operations.py  # 订单操作相关功能
└── product_knowledge.py # 产品知识库管理
```

## 作者

ggguo (ggguo@example.com)

## 许可证

本项目采用MIT许可证。