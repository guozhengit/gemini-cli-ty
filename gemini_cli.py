#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import click
import requests
from typing import Optional, Dict, Any, List, Tuple
from dotenv import load_dotenv
from colorama import init, Fore, Style
import google.generativeai as genai
from datetime import datetime
from pathlib import Path
import uuid

# 初始化colorama用于跨平台颜色输出
init()

class ContextManager:
    """上下文管理器，负责会话历史和上下文关联"""
    
    def __init__(self, data_dir: str = ".gemini_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id = None
        self.current_session = None
    
    def create_session(self, name: Optional[str] = None) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = name or f"chat_{timestamp}"
        
        session_data = {
            "id": session_id,
            "name": session_name,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "context_summary": "",
            "total_tokens": 0
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        self.current_session_id = session_id
        self.current_session = session_data
        return session_id
    
    def load_session(self, session_id: str) -> bool:
        """加载现有会话"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return False
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                self.current_session = json.load(f)
            self.current_session_id = session_id
            return True
        except Exception:
            return False
    
    def save_session(self):
        """保存当前会话"""
        if not self.current_session_id or not self.current_session:
            return
        
        session_file = self.sessions_dir / f"{self.current_session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, ensure_ascii=False, indent=2)
    
    def add_message(self, role: str, content: str, tokens: int = 0):
        """添加消息到当前会话"""
        if not self.current_session:
            return
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tokens": tokens
        }
        
        self.current_session["messages"].append(message)
        self.current_session["total_tokens"] += tokens
        self.save_session()
    
    def get_context_messages(self, limit: int = 10) -> List[Dict]:
        """获取上下文消息（最近的N条）"""
        if not self.current_session:
            return []
        
        messages = self.current_session["messages"]
        return messages[-limit:] if len(messages) > limit else messages
    
    def get_context_summary(self) -> str:
        """获取上下文摘要"""
        if not self.current_session:
            return ""
        return self.current_session.get("context_summary", "")
    
    def update_context_summary(self, summary: str):
        """更新上下文摘要"""
        if self.current_session:
            self.current_session["context_summary"] = summary
            self.save_session()
    
    def list_sessions(self) -> List[Dict]:
        """列出所有会话"""
        sessions = []
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    sessions.append({
                        "id": session["id"],
                        "name": session["name"],
                        "created_at": session["created_at"],
                        "message_count": len(session["messages"]),
                        "total_tokens": session.get("total_tokens", 0)
                    })
            except Exception:
                continue
        
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
    
    def search_messages(self, query: str) -> List[Tuple[str, Dict]]:
        """搜索消息"""
        results = []
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    for msg in session["messages"]:
                        if query.lower() in msg["content"].lower():
                            results.append((session["id"], msg))
            except Exception:
                continue
        return results


class GeminiClient:
    """Gemini API客户端，支持代理访问和上下文管理"""
    
    def __init__(self, api_key: str, proxy_config: Optional[Dict[str, str]] = None):
        self.api_key = api_key
        self.proxy_config = proxy_config or {}
        self.context_manager = ContextManager()
        self.setup_proxy()
        self.setup_client()
    
    def setup_proxy(self):
        """设置代理配置"""
        if self.proxy_config:
            # 设置环境变量代理
            for key, value in self.proxy_config.items():
                os.environ[key] = value
            
            print(f"{Fore.YELLOW}✓ 代理已配置: {self.proxy_config}{Style.RESET_ALL}")
    
    def setup_client(self):
        """初始化Gemini客户端"""
        try:
            genai.configure(api_key=self.api_key)  # type: ignore
            
            # 测试连接
            models = list(genai.list_models())  # type: ignore  # type: ignore
            if models:
                print(f"{Fore.GREEN}✓ Gemini API连接成功{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ 无法获取模型列表{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}✗ Gemini API连接失败: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def list_models(self):
        """列出可用的模型"""
        try:
            models = list(genai.list_models())  # type: ignore
            return [model.name for model in models if 'generateContent' in model.supported_generation_methods]
        except Exception as e:
            print(f"{Fore.RED}获取模型列表失败: {e}{Style.RESET_ALL}")
            return []
    
    def generate_content(self, prompt: str, model_name: str = "gemini-pro", use_context: bool = False) -> str:
        """生成内容，支持上下文关联"""
        try:
            model = genai.GenerativeModel(model_name)  # type: ignore
            
            # 如果启用上下文，构建完整的提示词
            if use_context and self.context_manager.current_session:
                context_messages = self.context_manager.get_context_messages(5)
                context_summary = self.context_manager.get_context_summary()
                
                # 构建上下文提示
                context_prompt = ""
                if context_summary:
                    context_prompt += f"上下文摘要: {context_summary}\n\n"
                
                if context_messages:
                    context_prompt += "最近的对话\n"
                    for msg in context_messages[-3:]:  # 只使用最近的3条
                        role = "用户" if msg["role"] == "user" else "AI"
                        context_prompt += f"{role}: {msg['content'][:100]}...\n"
                    context_prompt += "\n"
                
                full_prompt = f"{context_prompt}当前问题: {prompt}"
            else:
                full_prompt = prompt
            
            response = model.generate_content(full_prompt)
            
            # 保存到上下文
            if use_context and self.context_manager.current_session:
                self.context_manager.add_message("user", prompt)
                self.context_manager.add_message("assistant", response.text)
            
            return response.text
        except Exception as e:
            print(f"{Fore.RED}生成内容失败: {e}{Style.RESET_ALL}")
            return ""
    
    def chat_session(self, model_name: str = "gemini-pro", session_id: Optional[str] = None, session_name: Optional[str] = None):
        """启动增强型聊天会话，支持上下文管理"""
        try:
            # 加载或创建会话
            if session_id:
                if not self.context_manager.load_session(session_id):
                    print(f"{Fore.RED}会话 {session_id} 不存在，创建新会话{Style.RESET_ALL}")
                    session_id = self.context_manager.create_session(session_name)
                else:
                    print(f"{Fore.GREEN}加载会话: {self.context_manager.current_session['name'] if self.context_manager.current_session else 'Unknown'}{Style.RESET_ALL}")
            else:
                session_id = self.context_manager.create_session(session_name)
                print(f"{Fore.GREEN}创建新会话: {session_id}{Style.RESET_ALL}")
            
            model = genai.GenerativeModel(model_name)  # type: ignore
            chat = model.start_chat()
            
            # 恢复历史上下文
            context_messages = self.context_manager.get_context_messages()
            if context_messages:
                print(f"{Fore.CYAN}加载了 {len(context_messages)} 条历史消息{Style.RESET_ALL}")
                # 恢复上下文到聊天会话
                for msg in context_messages:
                    if msg["role"] == "user":
                        try:
                            chat.send_message(msg["content"])
                        except Exception:
                            pass  # 静默失败，不影响新对话
            
            print(f"{Fore.CYAN}=== Gemini 智能聊天会话 ==={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}会话 ID: {session_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}模型: {model_name}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}上下文: {'已启用' if context_messages else '新会话'}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}命令: 'quit'=退出, 'clear'=清空, 'save'=保存, 'summary'=摘要, 'history'=历史{Style.RESET_ALL}")
            print("-" * 60)
            
            message_count = 0
            
            while True:
                try:
                    user_input = input(f"\n{Fore.GREEN}[你]: {Style.RESET_ALL}")
                    
                    # 处理命令
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print(f"{Fore.YELLOW}再见！会话已保存。{Style.RESET_ALL}")
                        break
                    elif user_input.lower() == 'clear':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        continue
                    elif user_input.lower() == 'save':
                        self.context_manager.save_session()
                        print(f"{Fore.GREEN}会话已手动保存{Style.RESET_ALL}")
                        continue
                    elif user_input.lower() == 'summary':
                        self._generate_context_summary()
                        continue
                    elif user_input.lower() == 'history':
                        self._show_chat_history()
                        continue
                    elif user_input.lower().startswith('/search '):
                        query = user_input[8:]
                        self._search_history(query)
                        continue
                    
                    if not user_input.strip():
                        continue
                    
                    # 发送消息
                    print(f"{Fore.BLUE}[Gemini]: {Style.RESET_ALL}", end="", flush=True)
                    response = chat.send_message(user_input)
                    print(response.text)
                    
                    # 保存对话
                    self.context_manager.add_message("user", user_input)
                    self.context_manager.add_message("assistant", response.text)
                    
                    message_count += 1
                    
                    # 每10条消息自动生成摘要
                    if message_count % 10 == 0:
                        print(f"{Fore.CYAN}📝 自动生成上下文摘要...{Style.RESET_ALL}")
                        self._generate_context_summary(auto=True)
                    
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}聊天已中断，会话已保存{Style.RESET_ALL}")
                    break
                except Exception as e:
                    print(f"{Fore.RED}发送消息失败: {e}{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}启动聊天会话失败: {e}{Style.RESET_ALL}")
    
    def _generate_context_summary(self, auto: bool = False):
        """生成上下文摘要"""
        messages = self.context_manager.get_context_messages(20)
        if len(messages) < 5:
            if not auto:
                print(f"{Fore.YELLOW}消息太少，无法生成摘要{Style.RESET_ALL}")
            return
        
        # 构建摘要提示
        conversation_text = "\n".join([
            f"用户 if msg['role'] == 'user' else 'AI': {msg['content'][:200]}"
            for msg in messages[-10:]  # 只用最近的10条
        ])
        
        summary_prompt = f"""请为以下对话生成一个简洁的上下文摘要（100字以内），包括主要话题和关键信息：

{conversation_text}

摘要：
"""
        
        try:
            if not auto:
                print(f"{Fore.YELLOW}正在生成上下文摘要...{Style.RESET_ALL}")
            summary = self.generate_content(summary_prompt, use_context=False)
            if summary:
                self.context_manager.update_context_summary(summary)
                if not auto:
                    print(f"{Fore.CYAN}上下文摘要: {summary}{Style.RESET_ALL}")
        except Exception as e:
            if not auto:
                print(f"{Fore.RED}生成摘要失败: {e}{Style.RESET_ALL}")
    
    def _show_chat_history(self):
        """显示聊天历史"""
        messages = self.context_manager.get_context_messages(10)
        if not messages:
            print(f"{Fore.YELLOW}暂无历史消息{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}=== 最近 {len(messages)} 条消息 ==={Style.RESET_ALL}")
        for i, msg in enumerate(messages, 1):
            role = "👤 你" if msg["role"] == "user" else "🤖 AI"
            timestamp = msg["timestamp"][:19].replace("T", " ")
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"{i:2d}. [{timestamp}] {role}: {content}")
        print("-" * 60)
    
    def _search_history(self, query: str):
        """搜索历史消息"""
        results = self.context_manager.search_messages(query)
        if not results:
            print(f"{Fore.YELLOW}未找到包含 '{query}' 的消息{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}=== 搜索结果: '{query}' ==={Style.RESET_ALL}")
        for i, (session_id, msg) in enumerate(results[:10], 1):
            role = "👤" if msg["role"] == "user" else "🤖"
            timestamp = msg["timestamp"][:19].replace("T", " ")
            content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
            print(f"{i:2d}. [{session_id[:8]}] [{timestamp}] {role}: {content}")
        print("-" * 60)


def load_config():
    """加载配置"""
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print(f"{Fore.RED}错误: 请设置GEMINI_API_KEY环境变量{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}你可以:")
        print(f"1. 复制 .env.example 为 .env 并填入你的API密钥")
        print(f"2. 或者设置环境变量: set GEMINI_API_KEY=your_key{Style.RESET_ALL}")
        sys.exit(1)
    
    # 代理配置
    proxy_config = {}
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')
    
    if http_proxy:
        proxy_config['HTTP_PROXY'] = http_proxy
    if https_proxy:
        proxy_config['HTTPS_PROXY'] = https_proxy
    
    model = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    return api_key, proxy_config, model


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Gemini CLI - 支持代理的Gemini命令行工具"""
    pass


@cli.command()
def models():
    """列出可用的模型"""
    api_key, proxy_config, _ = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    model_list = client.list_models()
    if model_list:
        print(f"{Fore.CYAN}可用模型:{Style.RESET_ALL}")
        for model in model_list:
            print(f"  • {model}")
    else:
        print(f"{Fore.RED}无法获取模型列表{Style.RESET_ALL}")


@cli.command()
@click.option('--model', '-m', default=None, help='指定模型名称')
@click.option('--context', '-c', is_flag=True, help='启用上下文关联')
@click.option('--session', '-s', default=None, help='指定会话 ID')
@click.argument('prompt', required=False)
def generate(model, context, session, prompt):
    """生成内容，支持上下文关联"""
    api_key, proxy_config, default_model = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    model_name = model or default_model
    
    # 加载指定会话
    if context and session:
        if not client.context_manager.load_session(session):
            print(f"{Fore.RED}会话 {session} 不存在{Style.RESET_ALL}")
            return
        if not client.context_manager.current_session:
            print(f"{Fore.RED}无法加载会话{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}加载会话: {client.context_manager.current_session['name']}{Style.RESET_ALL}")
    elif context:
        # 创建临时会话用于上下文
        client.context_manager.create_session("temp_generate")
    
    if not prompt:
        prompt = click.prompt('请输入提示词')
    
    context_info = f" (上下文关联: {'\u5df2\u542f\u7528' if context else '\u672a\u542f\u7528'})" if context else ""
    print(f"{Fore.YELLOW}正在生成内容{context_info}...{Style.RESET_ALL}")
    
    response = client.generate_content(prompt, model_name, use_context=context)
    
    if response:
        print(f"\n{Fore.CYAN}=== Gemini 响应 ==={Style.RESET_ALL}")
        print(response)
        
        # 显示会话信息
        if context and client.context_manager.current_session:
            session_id = client.context_manager.current_session_id
            print(f"\n{Fore.YELLOW}会话 ID: {session_id} (可用于继续对话){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}生成失败{Style.RESET_ALL}")


@cli.command()
@click.option('--model', '-m', default=None, help='指定模型名称')
@click.option('--session', '-s', default=None, help='加载指定会话 ID')
@click.option('--name', '-n', default=None, help='新会话名称')
def chat(model, session, name):
    """启动增强聊天会话，支持上下文管理"""
    api_key, proxy_config, default_model = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    model_name = model or default_model
    client.chat_session(model_name, session_id=session, session_name=name)


@cli.command()
def sessions():
    """列出所有会话"""
    api_key, proxy_config, _ = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    session_list = client.context_manager.list_sessions()
    if not session_list:
        print(f"{Fore.YELLOW}暂无保存的会话{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}=== 会话列表 ==={Style.RESET_ALL}")
    print(f"{'ID':<10} {'\u540d\u79f0':<20} {'\u521b\u5efa\u65f6\u95f4':<20} {'\u6d88\u606f\u6570':<8} {'Token\u6570':<8}")
    print("-" * 70)
    
    for session in session_list:
        created = session['created_at'][:19].replace('T', ' ')
        print(f"{session['id']:<10} {session['name']:<20} {created:<20} {session['message_count']:<8} {session['total_tokens']:<8}")


@cli.command()
@click.argument('query')
def search(query):
    """搜索历史消息"""
    api_key, proxy_config, _ = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    results = client.context_manager.search_messages(query)
    if not results:
        print(f"{Fore.YELLOW}未找到包含 '{query}' 的消息{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}=== 搜索结果: '{query}' ({len(results)} 条) ==={Style.RESET_ALL}")
    for i, (session_id, msg) in enumerate(results[:20], 1):
        role = "👤" if msg["role"] == "user" else "🤖"
        timestamp = msg["timestamp"][:19].replace("T", " ")
        content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
        print(f"{i:2d}. [{session_id[:8]}] [{timestamp}] {role}: {content}")


@cli.command()
@click.argument('session_id')
def show(session_id):
    """显示指定会话的详细信息"""
    api_key, proxy_config, _ = load_config()
    client = GeminiClient(api_key, proxy_config)
    
    if not client.context_manager.load_session(session_id):
        print(f"{Fore.RED}会话 {session_id} 不存在{Style.RESET_ALL}")
        return
    
    session = client.context_manager.current_session
    if not session:
        print(f"{Fore.RED}会话数据无效{Style.RESET_ALL}")
        return
        
    print(f"{Fore.CYAN}=== 会话详情: {session['name']} ==={Style.RESET_ALL}")
    print(f"ID: {session['id']}")
    print(f"创建时间: {session['created_at'][:19].replace('T', ' ')}")
    print(f"消息数量: {len(session['messages'])}")
    print(f"Token 统计: {session.get('total_tokens', 0)}")
    
    if session.get('context_summary'):
        print(f"\n上下文摘要: {session['context_summary']}")
    
    messages = session['messages']
    if messages:
        print(f"\n{Fore.CYAN}=== 最近 10 条消息 ==={Style.RESET_ALL}")
        for msg in messages[-10:]:
            role = "👤 你" if msg["role"] == "user" else "🤖 AI"
            timestamp = msg["timestamp"][:19].replace("T", " ")
            content = msg["content"][:150] + "..." if len(msg["content"]) > 150 else msg["content"]


@cli.command()
def test():
    """测试连接"""
    api_key, proxy_config, model = load_config()
    
    print(f"{Fore.CYAN}=== 连接测试 ==={Style.RESET_ALL}")
    print(f"API Key: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else api_key}")
    print(f"代理配置: {proxy_config if proxy_config else '无'}")
    print(f"默认模型: {model}")
    
    client = GeminiClient(api_key, proxy_config)
    
    # 简单测试
    test_prompt = "Hello, please respond with 'Connection successful!'"
    print(f"\n{Fore.YELLOW}测试提示词: {test_prompt}{Style.RESET_ALL}")
    
    response = client.generate_content(test_prompt, model)
    if response:
        print(f"{Fore.GREEN}✓ 测试成功!{Style.RESET_ALL}")
        print(f"响应: {response}")
    else:
        print(f"{Fore.RED}✗ 测试失败{Style.RESET_ALL}")
    """测试连接"""
    api_key, proxy_config, model = load_config()
    
    print(f"{Fore.CYAN}=== 连接测试 ==={Style.RESET_ALL}")
    print(f"API Key: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else api_key}")
    print(f"代理配置: {proxy_config if proxy_config else '无'}")
    print(f"默认模型: {model}")
    
    client = GeminiClient(api_key, proxy_config)
    
    # 简单测试
    test_prompt = "Hello, please respond with 'Connection successful!'"
    print(f"\n{Fore.YELLOW}测试提示词: {test_prompt}{Style.RESET_ALL}")
    
    response = client.generate_content(test_prompt, model)
    if response:
        print(f"{Fore.GREEN}✓ 测试成功!{Style.RESET_ALL}")
        print(f"响应: {response}")
    else:
        print(f"{Fore.RED}✗ 测试失败{Style.RESET_ALL}")


if __name__ == '__main__':
    cli()