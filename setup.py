#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

def setup_wizard():
    """配置向导"""
    print("=== Gemini CLI 配置向导 ===\n")
    
    # 检查 .env 文件
    env_file = Path('.env')
    if env_file.exists():
        print("✓ 发现现有的 .env 配置文件")
        overwrite = input("是否重新配置? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("配置已取消")
            return
    
    print("请提供以下配置信息:\n")
    
    # API Key
    api_key = input("Gemini API Key: ").strip()
    if not api_key:
        print("错误: API Key 不能为空")
        return
    
    # 代理配置
    print("\n代理配置 (可选, 直接回车跳过):")
    use_proxy = input("是否使用代理? (y/N): ").lower().strip()
    
    proxy_config = ""
    if use_proxy == 'y':
        proxy_type = input("代理类型 (1: HTTP/HTTPS, 2: SOCKS5) [1]: ").strip()
        proxy_type = '1' if not proxy_type else proxy_type
        
        proxy_host = input("代理主机 [127.0.0.1]: ").strip()
        proxy_host = '127.0.0.1' if not proxy_host else proxy_host
        
        proxy_port = input("代理端口 [7890]: ").strip()
        proxy_port = '7890' if not proxy_port else proxy_port
        
        auth_needed = input("代理需要认证吗? (y/N): ").lower().strip()
        
        if auth_needed == 'y':
            username = input("用户名: ").strip()
            password = input("密码: ").strip()
            if proxy_type == '2':
                proxy_url = f"socks5://{username}:{password}@{proxy_host}:{proxy_port}"
            else:
                proxy_url = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
        else:
            if proxy_type == '2':
                proxy_url = f"socks5://{proxy_host}:{proxy_port}"
            else:
                proxy_url = f"http://{proxy_host}:{proxy_port}"
        
        proxy_config = f"""
# 代理设置
HTTP_PROXY={proxy_url}
HTTPS_PROXY={proxy_url}"""
    
    # 模型选择
    print("\n模型配置:")
    model = input("默认模型 [gemini-pro]: ").strip()
    model = 'gemini-pro' if not model else model
    
    # 生成配置文件
    config_content = f"""# Gemini API Key
GEMINI_API_KEY={api_key}{proxy_config}

# 模型设置
GEMINI_MODEL={model}
"""
    
    # 写入文件
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"\n✓ 配置文件已保存到 .env")
    print("\n你现在可以使用以下命令:")
    print("  python gemini_cli.py test      # 测试连接")
    print("  python gemini_cli.py models    # 查看可用模型")
    print("  python gemini_cli.py chat      # 启动聊天")
    print("  python gemini_cli.py generate  # 生成内容")
    print("\n或者使用快捷命令:")
    print("  gemini test")
    print("  gemini chat")

if __name__ == '__main__':
    try:
        setup_wizard()
    except KeyboardInterrupt:
        print("\n\n配置已取消")
    except Exception as e:
        print(f"\n配置失败: {e}")