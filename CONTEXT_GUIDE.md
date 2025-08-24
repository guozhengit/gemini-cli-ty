# Gemini CLI 上下文管理功能指南

## 🚀 新功能概览

你的 Gemini CLI 工具现在支持强大的**上下文关联**和**会话管理**功能！这意味着：

- ✅ **智能对话记忆** - AI能记住之前的对话内容
- ✅ **多会话管理** - 可以创建和切换不同的对话主题
- ✅ **历史记录搜索** - 快速找到之前讨论过的内容
- ✅ **自动上下文摘要** - 长对话的智能总结
- ✅ **会话持久化** - 对话历史永久保存

## 📋 核心功能详解

### 1. 智能聊天会话 (推荐使用)

#### 基础聊天
```bash
# 启动新的智能聊天会话
python gemini_cli.py chat

# 指定会话名称
python gemini_cli.py chat -n "Python学习"

# 使用指定模型
python gemini_cli.py chat -m models/gemini-2.0-flash -n "编程助手"
```

#### 会话恢复
```bash
# 继续之前的会话 (使用会话ID)
python gemini_cli.py chat -s a1b2c3d4

# 列出所有会话，找到要恢复的会话ID
python gemini_cli.py sessions
```

### 2. 上下文关联生成

#### 启用上下文的单次生成
```bash
# 启用上下文关联
python gemini_cli.py generate -c "继续之前的话题"

# 在指定会话中生成内容
python gemini_cli.py generate -c -s a1b2c3d4 "基于我们之前的讨论"

# 创建临时上下文会话
python gemini_cli.py generate -c "这是第一个问题"
# 然后使用返回的会话ID继续
python gemini_cli.py generate -c -s [会话ID] "基于刚才的回答"
```

### 3. 会话管理

#### 查看所有会话
```bash
python gemini_cli.py sessions
```
输出示例：
```
=== 会话列表 ===
ID         名称                 创建时间             消息数   Token数
a1b2c3d4   Python学习          2024-01-20 14:30:25    12      1450
e5f6g7h8   工作讨论            2024-01-20 15:45:10     8       980
```

#### 查看会话详情
```bash
python gemini_cli.py show a1b2c3d4
```

### 4. 历史记录搜索

```bash
# 搜索包含特定关键词的历史消息
python gemini_cli.py search "机器学习"
python gemini_cli.py search "Python函数"
python gemini_cli.py search "项目部署"
```

## 🎮 聊天会话中的高级命令

在聊天过程中，你可以使用以下命令：

| 命令 | 功能 | 示例 |
|------|------|------|
| `quit` / `q` | 退出聊天并保存 | `q` |
| `clear` | 清屏 | `clear` |
| `save` | 手动保存会话 | `save` |
| `summary` | 生成对话摘要 | `summary` |
| `history` | 显示最近消息 | `history` |
| `/search 关键词` | 搜索历史 | `/search 函数` |

## 🎯 实用场景示例

### 场景1：编程学习助手
```bash
# 创建专门的编程学习会话
python gemini_cli.py chat -n "Python编程学习"

# 会话中的对话：
你: 我想学习Python的面向对象编程
AI: [详细解释OOP概念]

你: 能给我一个类的例子吗？
AI: [基于之前的解释，给出相关例子]

你: 如何实现继承？
AI: [基于前面的类例子，解释继承]
```

### 场景2：项目开发讨论
```bash
# 开始项目讨论
python gemini_cli.py chat -n "Web项目开发"

你: 我要开发一个电商网站，需要什么技术栈？
AI: [推荐技术栈]

你: 数据库设计有什么建议？
AI: [基于电商场景的数据库建议]

# 第二天继续讨论 - 先找到会话ID
python gemini_cli.py sessions

# 恢复会话
python gemini_cli.py chat -s [项目会话ID]
你: 昨天讨论的支付模块怎么设计？
AI: [基于之前电商讨论的上下文回答]
```

### 场景3：跨会话内容关联
```bash
# 在一个会话中学习概念
python gemini_cli.py generate -c "什么是RESTful API？"

# 在另一个项目会话中应用
python gemini_cli.py generate -c -s [项目会话ID] "如何在我们的电商项目中实现RESTful API？"
```

## 📊 数据管理

### 存储位置
- 会话数据保存在 `.gemini_data/sessions/` 目录
- 每个会话一个JSON文件
- 包含完整的对话历史和元数据

### 数据结构
```json
{
  "id": "会话ID",
  "name": "会话名称", 
  "created_at": "创建时间",
  "messages": [对话消息],
  "context_summary": "上下文摘要",
  "total_tokens": "总Token数"
}
```

## 🎛️ 智能功能

### 自动上下文摘要
- 每10条消息自动生成摘要
- 帮助AI理解长对话的核心内容
- 手动触发：在聊天中输入 `summary`

### 上下文关联策略
- 使用最近3-5条消息作为直接上下文
- 结合会话摘要提供背景信息
- 智能筛选相关历史内容

### 性能优化
- 限制上下文长度避免Token超限
- 智能消息压缩和摘要
- 按需加载历史数据

## 💡 使用建议

### 1. **会话组织策略**
- 按主题创建不同会话（学习、工作、项目等）
- 使用描述性的会话名称
- 定期查看会话列表清理无用会话

### 2. **上下文优化**
- 重要讨论启用上下文关联
- 单次查询可以不启用上下文
- 长时间讨论后使用摘要功能

### 3. **搜索技巧**
- 使用关键词搜索历史内容
- 结合时间和会话ID定位信息
- 善用搜索功能回顾重要讨论

## 🔧 故障排除

### 会话加载失败
```bash
# 检查会话是否存在
python gemini_cli.py sessions

# 查看具体错误
python gemini_cli.py show [会话ID]
```

### 搜索无结果
- 检查关键词拼写
- 尝试使用同义词
- 确认该内容确实存在于历史中

### 上下文关联效果不佳
- 确保会话中有足够的历史消息
- 使用摘要功能整理长对话
- 考虑重新创建会话整理思路

## 🚀 快速开始

1. **测试连接**：`python gemini_cli.py test`
2. **开始智能聊天**：`python gemini_cli.py chat -n "我的第一个会话"`
3. **体验上下文关联**：在聊天中进行多轮对话
4. **查看会话历史**：`python gemini_cli.py sessions`
5. **搜索历史内容**：`python gemini_cli.py search "关键词"`

现在你的 Gemini CLI 工具拥有了企业级的对话管理能力！🎉