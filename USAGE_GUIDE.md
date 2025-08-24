# Gemini CLI 使用指南

## 🚀 快速开始

### 1. 配置工具
```bash
# 运行配置向导
python setup.py
```

配置向导会询问以下信息：
- **Gemini API Key** (必需): 你的 Google AI Studio API 密钥
- **代理设置** (可选): 如果你的网络需要代理
- **默认模型** (可选): 默认使用 gemini-pro

### 2. 常用代理设置

#### HTTP/HTTPS 代理 (如 Clash、V2rayN)
```
代理类型: 1 (HTTP/HTTPS)
代理主机: 127.0.0.1
代理端口: 7890  # 常见端口
```

#### SOCKS5 代理
```
代理类型: 2 (SOCKS5)
代理主机: 127.0.0.1
代理端口: 1080  # 常见端口
```

### 3. 测试连接
```bash
python gemini_cli.py test
```

## 📋 主要功能

### 聊天模式 (推荐)
```bash
# 启动交互式聊天
python gemini_cli.py chat

# 使用指定模型聊天
python gemini_cli.py chat -m gemini-pro
```

### 单次生成
```bash
# 交互式输入
python gemini_cli.py generate

# 直接提问
python gemini_cli.py generate "写一首关于科技的诗"

# 指定模型
python gemini_cli.py generate -m gemini-pro "解释机器学习原理"
```

### 查看可用模型
```bash
python gemini_cli.py models
```

## 🛠️ 手动配置 .env 文件

如果不想使用配置向导，可以手动创建 `.env` 文件：

```env
# Gemini API Key (必需)
GEMINI_API_KEY=你的实际API密钥

# HTTP/HTTPS 代理 (可选)
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

# SOCKS5 代理示例 (二选一)
# HTTP_PROXY=socks5://127.0.0.1:1080
# HTTPS_PROXY=socks5://127.0.0.1:1080

# 带认证的代理示例
# HTTP_PROXY=http://用户名:密码@代理地址:端口
# HTTPS_PROXY=http://用户名:密码@代理地址:端口

# 默认模型
GEMINI_MODEL=gemini-pro
```

## 🎯 使用场景示例

### 编程助手
```
You: 用Python写一个快速排序算法
Gemini: [提供详细的代码实现和解释]
```

### 学习助手
```
You: 解释量子计算的基本原理
Gemini: [详细解释量子计算概念]
```

### 翻译助手
```
You: 将这段中文翻译成英文：人工智能正在改变世界
Gemini: [提供准确的翻译]
```

### 创意写作
```
You: 写一个科幻短故事的开头
Gemini: [创作有趣的故事开头]
```

## 🔧 常见问题解决

### 连接问题
1. **代理连接失败**
   - 确认代理软件正在运行
   - 检查代理端口是否正确
   - 尝试不同的代理端口 (7890, 1080, 8080)

2. **API 连接超时**
   - 检查网络连接
   - 尝试更换代理服务器
   - 确认代理支持 HTTPS

### API Key 问题
1. **无效的 API Key**
   - 检查 API Key 是否正确复制
   - 确认 API Key 没有过期
   - 在 Google AI Studio 重新生成

2. **配额限制**
   - 检查 API 使用配额
   - 等待配额重置
   - 考虑升级 API 计划

### 代理设置问题
1. **SOCKS5 代理不工作**
   - 确保使用 `socks5://` 前缀
   - 检查代理软件是否支持 SOCKS5

2. **代理认证失败**
   - 确认用户名密码正确
   - 检查代理是否需要认证

## 🎮 快捷使用

### Windows 用户
使用批处理文件快速启动：
```cmd
# 复制配置文件
copy .env.example .env

# 使用快捷命令
gemini test
gemini chat
gemini models
```

### 常用命令别名
```bash
# 添加到你的 shell 配置文件
alias gm="python gemini_cli.py"
alias gmchat="python gemini_cli.py chat"
alias gmtest="python gemini_cli.py test"
```

## 📊 性能提示

1. **选择合适的模型**
   - `gemini-pro`: 平衡性能和质量
   - `gemini-pro-vision`: 支持图像输入

2. **优化提示词**
   - 使用清晰、具体的问题
   - 提供足够的上下文
   - 分解复杂问题

3. **网络优化**
   - 使用稳定的代理服务器
   - 选择延迟较低的代理节点

希望这个工具能帮助你更好地使用 Gemini AI！如有问题，请检查配置或重新运行设置向导。