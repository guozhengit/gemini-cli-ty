# 🔒 安全使用说明

## ⚠️ 重要安全提醒

### API 密钥保护
- **永远不要将真实的 API 密钥提交到代码仓库**
- 使用 `.env` 文件存储敏感信息（已在 `.gitignore` 中排除）
- 定期轮换 API 密钥以提高安全性

### 代理配置安全
- 避免在公开代码中暴露内网代理端口
- 使用通用的示例端口（如 7890, 1080）作为文档示例
- 实际使用时根据你的网络环境配置

### 会话数据隐私
- 本地会话数据存储在 `.gemini_data/` 目录
- 该目录已被 `.gitignore` 排除，不会同步到代码仓库
- 会话数据仅保存在本地，确保对话隐私

## 🛡️ 最佳实践

### 1. 环境配置
```bash
# 复制模板文件
cp .env.example .env

# 编辑配置文件，填入真实信息
# 注意：.env 文件不会被 Git 跟踪
```

### 2. API 密钥获取
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的 API 密钥
3. 将密钥填入 `.env` 文件中的 `GEMINI_API_KEY`

### 3. 代理配置
根据你的实际网络环境配置代理：
- HTTP/HTTPS 代理：`http://host:port`
- SOCKS5 代理：`socks5://host:port`
- 带认证的代理：`http://user:pass@host:port`

## 🚨 如果意外泄露

如果不小心将敏感信息提交到了代码仓库：

1. **立即更换 API 密钥**
2. **使用 git-filter-branch 清理历史记录**
3. **强制推送更新远程仓库**

```bash
# 示例：从历史记录中移除敏感文件
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
```

## 📋 检查清单

发布前请确认：
- [ ] `.env` 文件未被添加到 Git
- [ ] `.env.example` 中无真实敏感数据
- [ ] 代码中无硬编码的 API 密钥
- [ ] 文档中使用的是示例配置值
- [ ] `.gemini_data/` 目录已被忽略

## 🤝 贡献安全

如果发现安全问题，请：
1. 不要在公开 issue 中报告敏感信息
2. 发送邮件到项目维护者
3. 提供详细的问题描述和修复建议

感谢你为项目安全做出的贡献！