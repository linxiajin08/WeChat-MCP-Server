"""
微信 MCP 服务器包
用于微信消息自动化的模型上下文协议服务器。
"""

from .mcp_server import MCPServer
from .wechat_controller import WeChatController

__version__ = "1.0.0"
__all__ = ["MCPServer", "WeChatController"]