#!/usr/bin/env python3
"""
微信 MCP 服务器测试脚本
快速测试以验证服务器功能。
"""

import asyncio
import json
import sys
import os

# 将 src 添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server import MCPServer


async def test_mcp_server():
    """测试 MCP 服务器功能。"""
    print("🚀 Starting WeChat MCP Server Test")
    print("=" * 50)
    
    server = MCPServer()
    
    # 测试 1：初始化
    print("\n📋 Test 1: Initialize Server")
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        },
        "id": 1
    }
    
    response = await server.handle_request(init_request)
    print(f"✅ Initialize Response: {response.get('result', {}).get('serverInfo', {})}")
    
    # 测试 2：列出工具
    print("\n🔧 Test 2: List Available Tools")
    tools_request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    
    response = await server.handle_request(tools_request)
    tools = response.get('result', {}).get('tools', [])
    print(f"✅ Available Tools: {len(tools)} tools found")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # 测试 3：测试微信状态（不实际发送）
    print("\n📱 Test 3: Check WeChat Status")
    try:
        from wechat_controller import WeChatController
        controller = WeChatController()
        status = controller.get_status()
        print(f"✅ WeChat Status: {status}")
    except Exception as e:
        print(f"⚠️  WeChat Status Check Failed: {e}")
    
    # 测试 4：模拟工具调用（试运行）
    print("\n💬 Test 4: Simulate Message Send (Dry Run)")
    call_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "send_wechat_message",
            "arguments": {
                "contact_name": "文件传输助手",
                "message": "Test message from MCP server"
            }
        },
        "id": 3
    }
    
    print("📤 Simulating message send...")
    print(f"   Contact: {call_request['params']['arguments']['contact_name']}")
    print(f"   Message: {call_request['params']['arguments']['message']}")
    
    # 取消注释下一行以实际发送消息
    # response = await server.handle_request(call_request)
    # print(f"✅ Send Result: {response}")
    
    print("⚠️  Actual sending skipped in test mode")
    print("   To enable real sending, uncomment the lines in test_server.py")
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server Test Completed!")
    print("\n📝 Next Steps:")
    print("1. Ensure WeChat is running and logged in")
    print("2. Configure your AI assistant with this MCP server")
    print("3. Try sending a real message through your AI assistant")
    
    print("\n🔧 Configuration example for Claude Desktop:")
    print(json.dumps({
        "mcpServers": {
            "wechat": {
                "command": "python",
                "args": [os.path.abspath("src/mcp_server.py")],
                "env": {}
            }
        }
    }, indent=2))


if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()