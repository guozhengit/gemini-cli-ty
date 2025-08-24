@echo off
chcp 65001 > nul
echo.
echo 🚀 Gemini CLI - GitHub 发布脚本
echo ================================================
echo.

REM 检查是否已初始化Git
if not exist .git (
    echo ❌ 错误: 当前目录不是Git仓库
    echo 请先运行: git init
    pause
    exit /b 1
)

REM 检查是否有提交记录
git log --oneline -1 > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 没有找到Git提交记录
    echo 请先进行首次提交
    pause
    exit /b 1
)

echo 📋 当前Git状态:
git status --short
echo.

REM 获取用户GitHub信息
set /p GITHUB_USERNAME="请输入你的GitHub用户名: "
if "%GITHUB_USERNAME%"=="" (
    echo ❌ 错误: GitHub用户名不能为空
    pause
    exit /b 1
)

echo.
echo 📊 准备发布的内容:
echo ├── 🔹 仓库名称: gemini-cli
echo ├── 🔹 GitHub用户: %GITHUB_USERNAME%
echo ├── 🔹 远程URL: https://github.com/%GITHUB_USERNAME%/gemini-cli.git
echo └── 🔹 默认分支: main
echo.

echo ⚠️  请确保你已在GitHub上创建了名为 'gemini-cli' 的仓库
echo    访问: https://github.com/new
echo    仓库名: gemini-cli
echo    描述: 🤖 功能强大的Gemini API命令行工具，支持代理访问、智能上下文管理和多会话系统
echo    类型: Public
echo    不要勾选 README、.gitignore 和 License (我们已经有了)
echo.

set /p CONFIRM="确认继续? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo 🔄 操作已取消
    pause
    exit /b 0
)

echo.
echo 🔧 正在配置远程仓库...

REM 检查是否已存在远程仓库
git remote get-url origin > nul 2>&1
if not errorlevel 1 (
    echo 📝 移除现有的远程仓库配置...
    git remote remove origin
)

REM 添加GitHub远程仓库
echo 📝 添加GitHub远程仓库...
git remote add origin https://github.com/%GITHUB_USERNAME%/gemini-cli.git

REM 检查远程仓库连接
echo 📡 测试远程仓库连接...
git ls-remote origin > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 无法连接到远程仓库
    echo    请检查:
    echo    1. GitHub仓库是否已创建
    echo    2. 用户名是否正确
    echo    3. 网络连接是否正常
    echo    4. Git认证是否配置 (git config --global user.name/user.email)
    pause
    exit /b 1
)

REM 设置默认分支
echo 📝 设置主分支为 main...
git branch -M main

REM 推送代码到GitHub
echo 📤 推送代码到GitHub...
git push -u origin main

if errorlevel 1 (
    echo ❌ 推送失败!
    echo    可能的原因:
    echo    1. 认证问题 - 请配置GitHub访问令牌
    echo    2. 仓库已存在内容 - 使用 git push --force-with-lease origin main
    echo    3. 网络连接问题
    pause
    exit /b 1
)

echo.
echo ✅ 成功推送到GitHub!
echo 🌐 仓库地址: https://github.com/%GITHUB_USERNAME%/gemini-cli
echo.

echo 📋 接下来的步骤:
echo 1. 访问: https://github.com/%GITHUB_USERNAME%/gemini-cli
echo 2. 检查代码是否正确上传
echo 3. 创建Release版本 (可选)
echo 4. 添加项目主题标签和说明
echo.

echo 🏷️  建议的GitHub主题标签:
echo    gemini-api, cli-tool, python, ai-assistant, proxy-support, 
echo    context-management, chatbot, command-line, artificial-intelligence
echo.

pause
exit /b 0