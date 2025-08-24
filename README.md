# Gemini CLI - 支持代理和上下文管理的Gemini命令行工具

一个功能强大的Gemini API命令行工具，专为网络受限地区用户设计，支持代理访问和智能上下文管理。

## 🌟 核心特性

- ✅ **代理支持** - 完美支持HTTP/HTTPS/SOCKS5代理
- ✅ **智能对话** - AI能记住对话历史，支持上下文关联
- ✅ **多会话管理** - 创建和管理多个独立的聊天会话
- ✅ **历史记录** - 永久保存对话，支持搜索和回顾
- ✅ **自动摘要** - 智能生成长对话的上下文摘要
- ✅ **交互式聊天** - 支持多轮对话和实时交互
- ✅ **彩色输出** - 友好的命令行界面体验

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境配置文件：
```bash
copy .env.example .env
```

2. 编辑 `.env` 文件，填入你的配置：
```env
# Gemini API Key (必需)
GEMINI_API_KEY=your_gemini_api_key_here

# 代理设置 (可选)
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

# 或者使用 socks5 代理
# HTTP_PROXY=socks5://127.0.0.1:1080
# HTTPS_PROXY=socks5://127.0.0.1:1080

# 模型设置
GEMINI_MODEL=gemini-pro
```

## 🚀 使用方法

### 1. 智能聊天会话 (🎆 推荐)
```bash
# 启动新的智能聊天会话
python gemini_cli.py chat

# 创建具名会话
python gemini_cli.py chat -n "Python学习"

# 继续之前的会话
python gemini_cli.py chat -s a1b2c3d4

# 使用指定模型
python gemini_cli.py chat -m models/gemini-2.0-flash
```

### 2. 上下文关联生成
```bash
# 启用上下文关联的单次生成
python gemini_cli.py generate -c "继续之前的话题"

# 在指定会话中生成
python gemini_cli.py generate -c -s a1b2c3d4 "基于我们的讨论"

# 普通单次生成（无上下文）
python gemini_cli.py generate "写一首关于科技的诗"
```

### 3. 会话管理
```bash
# 查看所有会话
python gemini_cli.py sessions

# 查看会话详情
python gemini_cli.py show a1b2c3d4

# 搜索历史消息
python gemini_cli.py search "机器学习"
```

## 代理配置说明

### HTTP/HTTPS 代理
```env
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

### SOCKS5 代理
```env
HTTP_PROXY=socks5://127.0.0.1:1080
HTTPS_PROXY=socks5://127.0.0.1:1080
```

### 带认证的代理
```env
HTTP_PROXY=http://username:password@proxy.example.com:8080
HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

## 常见问题

### Q: 如何获取Gemini API Key？
A: 访问 [Google AI Studio](https://makersuite.google.com/app/apikey) 创建API密钥。

### Q: 代理设置不生效？
A: 请确认：
1. 代理服务正在运行
2. 代理地址和端口正确
3. 如果是SOCKS5代理，确保使用了 `socks5://` 前缀

### Q: 连接超时怎么办？
A: 尝试：
1. 检查代理设置
2. 更换代理服务器
3. 检查网络连接

### Q: API Key 错误？
A: 请确认：
1. API Key 正确复制
2. API Key 没有过期
3. API Key 有足够的配额

## 📝 支持的命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `test` | 测试连接和配置 | `python gemini_cli.py test` |
| `models` | 列出可用模型 | `python gemini_cli.py models` |
| `chat` | 智能聊天会话 | `python gemini_cli.py chat -n "学习"` |
| `generate` | 生成内容 | `python gemini_cli.py generate -c "问题"` |
| `sessions` | 会话管理 | `python gemini_cli.py sessions` |
| `show` | 显示会话详情 | `python gemini_cli.py show a1b2c3d4` |
| `search` | 搜索历史 | `python gemini_cli.py search "关键词"` |
| `--help` | 显示帮助 | `python gemini_cli.py --help` |

### 🎆 新增功能

- **上下文关联**: 使用 `-c` 参数启用智能上下文
- **会话管理**: 创建、恢复和管理多个聊天会话
- **历史搜索**: 快速找到之前讨论的内容
- **自动摘要**: 长对话的智能总结

> 📚 **详细指南**: 查看 [CONTEXT_GUIDE.md](CONTEXT_GUIDE.md) 获取完整的上下文管理功能指南

## 示例会话

```
$ python gemini_cli.py chat
✓ 代理已配置: {'HTTP_PROXY': 'http://127.0.0.1:7890', 'HTTPS_PROXY': 'http://127.0.0.1:7890'}
✓ Gemini API连接成功
=== Gemini 聊天会话 ===
模型: gemini-pro
输入 'quit', 'exit' 或 'q' 退出聊天
--------------------------------------------------

You: 你好
Gemini: 你好！很高兴与你交流。有什么我可以帮助你的吗？

You: 解释一下机器学习
Gemini: 机器学习是人工智能的一个分支...

You: q
再见！
```

## 许可证

MIT License