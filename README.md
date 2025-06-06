# 智能客服示例

这是一个基于MCP框架的智能客服系统示例项目，用于演示如何构建和部署智能客服应用。

文档：https://mp.weixin.qq.com/s/gz3ZL_3XD8sfxustNQvK2g

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
uv venv 
source .venv/bin/activate  # Linux/macOS
```

2. 安装依赖：
```bash
uv pip install .
```

## 使用方法
1. 运行
- 以stdio方式运行，需要以--stdio启动
```bash
uv --directory /opt/apps/python_project/SmartCustomerSupportMCP run mcp-smart-customer-support --stdio
```
or
```bash
 python start.py --stdio
 ```

- 以sse方式运行，直接启动即可,默认端口9000
```bash
uv --directory /opt/apps/python_project/SmartCustomerSupportMCP run mcp-smart-customer-support
```
or
```bash
 python start.py 
 ```

2. stdio方式使用inspector：
```bash
npx @modelcontextprotocol/inspector uv --directory /opt/apps/python_project/SmartCustomerSupportMCP run mcp-smart-customer-support --stdio
```
3. 使用Vscode或Claude等桌面应用
```json

{
  "mcpServers": {
      "SmartCustomerSupportMCP": {
        "command": "uv",
        "args": [
          "--directory",
          "/opt/apps/python_project/SmartCustomerSupportMCP", 
          "run",
          "mcp-smart-customer-support",
          "--stdio"
        ]
    }
  }
}    
```

**增加环境变量信息**
```json
{
  "mcpServers": {
      "SmartCustomerSupportMCP": {
        "command": "uv",
        "args": [
          "--directory",
          "/opt/apps/python_project/SmartCustomerSupportMCP", 
          "run",
          "mcp-smart-customer-support",
          "--stdio"
        ],
        "env": {
          "MYSQL_HOST": "192.168.xxx.xxx",
          "MYSQL_PORT": "3306",
          "MYSQL_USER": "root",
          "MYSQL_PASSWORD": "root",
          "MYSQL_DATABASE": "a_llm",
          "MYSQL_ROLE": "admin"
       }
    }
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

ggguo (admin@precariat.tech)

## 许可证

本项目采用MIT许可证。