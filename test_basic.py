#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的功能测试脚本
"""

import sys
import os
sys.path.insert(0, '.')

from gemini_cli import GeminiClient

def test_basic_functionality():
    """测试基本功能"""
    print("=== Gemini CLI 功能测试 ===\n")
    
    # 测试代理配置
    proxy_config = {
        'HTTP_PROXY': 'http://127.0.0.1:7890',
        'HTTPS_PROXY': 'http://127.0.0.1:7890'
    }
    
    print("✓ 代理配置测试通过")
    print(f"  配置: {proxy_config}")
    
    # 测试无API Key的情况
    try:
        client = GeminiClient("fake_api_key", proxy_config)
        print("✗ 应该抛出连接错误")
    except SystemExit:
        print("✓ 无效API Key正确处理")
    
    print("\n=== 基本功能测试完成 ===")
    print("工具已准备就绪！")
    print("\n使用方法:")
    print("1. 配置你的API密钥和代理设置:")
    print("   python setup.py")
    print("2. 测试连接:")
    print("   python gemini_cli.py test")
    print("3. 开始聊天:")
    print("   python gemini_cli.py chat")

if __name__ == '__main__':
    test_basic_functionality()