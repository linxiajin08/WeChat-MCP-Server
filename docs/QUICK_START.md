# 快速开始指南

## 5分钟快速部署WeChat MCP服务器

### 步骤1: 环境准备

1. **确保Python环境**
   ```bash
   python --version  # 需要Python 3.7+
   ```

2. **安装依赖包**
   ```bash
   cd WeChat-MCP-Server
   pip install -r requirements.txt
   ```

3. **启动微信并登录**
   - 打开微信客户端
   - 确保已登录
   - 保持微信窗口可见

### 步骤2: 测试MCP服务器

运行测试脚本验证功能：

```bash
cd examples
python mcp_client_example.py
```

如果看到类似输出，说明服务器工作正常：
```
MCP Server started
Initialize response: {'jsonrpc': '2.0', 'result': {...}, 'id': 1}
Tools list: {'jsonrpc': '2.0', 'result': {'tools': [...]}, 'id': 2}
```

### 步骤3: 配置AI助手

#### 对于Claude Desktop:

1. 打开Claude Desktop配置文件：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 添加MCP服务器配置：
   ```json
   {
     "mcpServers": {
       "wechat": {
         "command": "python",
         "args": ["C:/path/to/WeChat-MCP-Server/src/mcp_server.py"],
         "env": {}
       }
     }
   }
   ```

3. 重启Claude Desktop

#### 对于其他AI助手:

参考各自的MCP配置文档，使用相同的服务器路径和参数。

### 步骤4: 开始使用

在AI助手中尝试以下命令：

1. **发送简单消息**
   ```
   "帮我给文件传输助手发个消息：Hello from AI!"
   ```

2. **发送定时消息**
   ```
   "10秒后给文件传输助手发消息：这是一条定时消息"
   ```

3. **发送给特定联系人**
   ```
   "给张三发微信：明天的会议改到下午3点"
   ```

### 常见问题快速解决

#### 问题1: 找不到微信窗口
**解决方案:**
- 确保微信已启动
- 检查微信窗口是否可见
- 尝试点击微信窗口使其获得焦点

#### 问题2: 联系人找不到
**解决方案:**
- 确保联系人名称完全正确
- 先手动搜索一次该联系人
- 使用"文件传输助手"进行测试

#### 问题3: MCP连接失败
**解决方案:**
- 检查Python路径是否正确
- 验证依赖包是否安装完整
- 查看AI助手的错误日志

### 高级配置

#### 自定义快捷键
如果微信使用了不同的快捷键，可以修改 `wechat_controller.py` 中的快捷键设置。

#### 日志级别调整
在 `mcp_server.py` 中修改日志级别：
```python
logging.basicConfig(level=logging.DEBUG)  # 更详细的日志
```

#### 添加更多联系人
建议在微信中将常用联系人置顶，这样搜索会更快更准确。

### 下一步

- 阅读完整的 [README.md](../README.md) 了解更多功能
- 查看 [API文档](API.md) 了解所有可用工具
- 参考 [开发指南](DEVELOPMENT.md) 进行自定义开发

### 获得帮助

如果遇到问题：
1. 检查日志输出
2. 查看常见问题解答
3. 提交Issue到项目仓库