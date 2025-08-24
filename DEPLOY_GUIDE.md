# 📤 GitHub 发布指南

## 🎯 发布步骤总览

### 步骤1️⃣: 在GitHub创建仓库

1. **访问GitHub**: https://github.com/new
2. **填写仓库信息**:
   ```
   Repository name: gemini-cli
   Description: 🤖 功能强大的Gemini API命令行工具，支持代理访问、智能上下文管理和多会话系统
   
   ✅ Public (推荐公开)
   ❌ Add a README file (不要勾选)
   ❌ Add .gitignore (不要勾选)
   ✅ Choose a license: MIT License (可选)
   ```
3. **点击 "Create repository"**

### 步骤2️⃣: 连接本地仓库到GitHub

在命令行中执行以下命令（替换 `YOUR_USERNAME` 为你的GitHub用户名）:

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/gemini-cli.git

# 确保在main分支
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

**或者运行自动化脚本**:
```bash
deploy_to_github.bat
```

### 步骤3️⃣: 验证发布

1. **访问仓库**: https://github.com/YOUR_USERNAME/gemini-cli
2. **检查文件**: 确认所有文件都已上传
3. **查看README**: 确认显示效果正常

### 步骤4️⃣: 创建Release版本

1. **进入Releases页面**: 点击仓库页面的 "Releases"
2. **创建新release**: 点击 "Create a new release"
3. **填写release信息**:
   ```
   Tag version: v1.0.0
   Release title: 🚀 Gemini CLI v1.0.0 - Initial Release
   
   描述:
   ## 🎉 首个正式版本发布！
   
   ### ✨ 核心功能
   - 🌐 代理支持 - 完美支持HTTP/HTTPS/SOCKS5代理访问
   - 🧠 智能上下文 - AI记忆对话历史，支持上下文关联
   - 📁 多会话管理 - 创建和管理多个独立的聊天会话
   - 🔍 历史搜索 - 永久保存对话，支持全文搜索
   - 📊 自动摘要 - 智能生成长对话的上下文摘要
   
   ### 🛡️ 安全特性
   - 环境变量配置管理
   - 敏感数据保护机制
   - 本地会话数据隐私保护
   
   ### 🎯 适用场景
   - 网络受限地区的Gemini API访问
   - 编程学习和技术咨询
   - 项目开发和问题解决
   - 知识管理和信息检索
   ```
4. **发布Release**: 点击 "Publish release"

## 🏷️ 推荐的GitHub设置

### 仓库主题标签 (Topics)
在仓库首页点击设置图标，添加以下标签：
```
gemini-api, cli-tool, python, ai-assistant, proxy-support, 
context-management, chatbot, command-line, artificial-intelligence,
conversation-ai, session-management, google-gemini
```

### 仓库描述优化
```
🤖 Powerful Gemini API CLI tool with proxy support, intelligent context management, and multi-session system for developers and AI enthusiasts
```

## 🚨 常见问题解决

### 推送失败 - 认证问题
```bash
# 如果使用HTTPS需要Personal Access Token
# 1. 去 GitHub Settings > Developer settings > Personal access tokens
# 2. 创建新token，勾选 repo 权限
# 3. 使用token作为密码

# 或者配置SSH (推荐)
ssh-keygen -t ed25519 -C "your_email@example.com"
# 将公钥添加到GitHub账户
```

### 推送失败 - 仓库冲突
```bash
# 如果远程仓库有冲突，强制推送 (谨慎使用)
git push --force-with-lease origin main
```

### 文件编码问题
```bash
# 设置Git处理换行符
git config --global core.autocrlf true
```

## ✅ 发布检查清单

- [ ] GitHub仓库已创建
- [ ] 本地代码已推送到远程
- [ ] README.md 显示正常  
- [ ] 所有文档文件都已上传
- [ ] .env 等敏感文件已被正确忽略
- [ ] License 文件已包含
- [ ] Release 版本已创建
- [ ] 仓库描述和主题已设置

完成所有步骤后，你的 Gemini CLI 项目就正式发布到GitHub了！🎉