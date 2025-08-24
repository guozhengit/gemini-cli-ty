@echo off
chcp 65001 > nul
echo Gemini CLI - 支持代理的Gemini命令行工具
echo.

if not exist .env (
    echo [警告] 未找到 .env 配置文件
    echo 请复制 .env.example 为 .env 并配置你的API密钥和代理设置
    echo.
    echo 复制配置文件命令:
    echo copy .env.example .env
    echo.
    pause
    exit /b 1
)

python gemini_cli.py %*