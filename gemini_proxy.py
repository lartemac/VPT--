#!/usr/bin/env python3
"""
Anthropic-to-Gemini 代理服务器
将 Anthropic Messages API 格式转换为 Google Gemini 原生格式
Claude Code → 本代理(Anthropic格式) → Gemini(原生格式)

创建时间: 2026-04-15
创建系统: macOS
"""

import json
import os
import sys
import uuid
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path

# 读取配置
def load_config():
    config_path = Path(__file__).parent / "api_config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    raise RuntimeError("未找到 api_config.json")

CONFIG = load_config()
GEMINI_API_KEY = CONFIG["gemini"]["api_key"]
GEMINI_MODEL = CONFIG["gemini"].get("model", "gemini-2.5-flash")
PORT = CONFIG["gemini"].get("proxy_port", 4000)

# 配置 Gemini SDK
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class AnthropicProxyHandler(BaseHTTPRequestHandler):
    """将 Anthropic Messages API 请求转换为 Gemini 调用"""

    def log_message(self, format, *args):
        # 简化日志
        pass

    def do_POST(self):
        if self.path == '/v1/messages':
            self._handle_messages()
        elif self.path == '/health' or self.path == '/v1/health':
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_GET(self):
        if self.path == '/health' or self.path == '/v1/health':
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_messages(self):
        try:
            # 读取请求
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length))

            # 提取参数
            stream = body.get('stream', False)
            max_tokens = body.get('max_tokens', 8192)
            system = body.get('system', '')
            messages = body.get('messages', [])
            model_name = body.get('model', GEMINI_MODEL)

            # 统一模型名（去掉可能的 gemini/ 前缀）
            if '/' in model_name and model_name.startswith('gemini/'):
                model_name = model_name.split('/', 1)[1]
            if not model_name.startswith('gemini'):
                model_name = GEMINI_MODEL

            # 解析消息
            gemini_history, last_content = self._convert_messages(messages)

            # 创建模型
            gen_config = genai.GenerationConfig(max_output_tokens=max_tokens)
            model_kwargs = {}
            if system:
                if isinstance(system, list):
                    system = ' '.join(s.get('text', '') for s in system)
                model_kwargs['system_instruction'] = system

            model = genai.GenerativeModel(model_name, generation_config=gen_config, **model_kwargs)

            if stream:
                self._handle_stream(model, gemini_history, last_content, model_name)
            else:
                self._handle_sync(model, gemini_history, last_content, model_name)

        except Exception as e:
            self._send_json(500, {"error": {"type": "internal_error", "message": str(e)}})

    def _convert_messages(self, messages):
        """将 Anthropic 格式消息转为 Gemini 格式"""
        gemini_history = []
        for msg in messages[:-1]:
            role = 'user' if msg.get('role') == 'user' else 'model'
            content = msg.get('content', '')
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get('type') == 'text':
                            parts.append(block.get('text', ''))
                        elif block.get('type') == 'tool_result':
                            parts.append(str(block.get('content', '')))
                        elif block.get('type') == 'tool_use':
                            parts.append(f"[Tool: {block.get('name','')}] {json.dumps(block.get('input',{}))}")
                    else:
                        parts.append(str(block))
                content = '\n'.join(parts)
            gemini_history.append({'role': role, 'parts': [str(content)]})

        last_content = ''
        if messages:
            content = messages[-1].get('content', '')
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get('type') == 'text':
                            parts.append(block.get('text', ''))
                        elif block.get('type') == 'tool_result':
                            parts.append(str(block.get('content', '')))
                        elif block.get('type') == 'tool_use':
                            parts.append(f"[Tool: {block.get('name','')}] {json.dumps(block.get('input',{}))}")
                    else:
                        parts.append(str(block))
                last_content = '\n'.join(parts)
            else:
                last_content = str(content)

        return gemini_history, last_content

    def _handle_stream(self, model, gemini_history, last_content, model_name):
        """流式响应（SSE 格式）"""
        msg_id = f"msg_{uuid.uuid4().hex[:24]}"

        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

        # message_start
        self._send_sse('message_start', {
            "type": "message_start",
            "message": {
                "id": msg_id, "type": "message", "role": "assistant",
                "content": [], "model": model_name, "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 0, "output_tokens": 0}
            }
        })

        # content_block_start
        self._send_sse('content_block_start', {
            "type": "content_block_start", "index": 0,
            "content_block": {"type": "text", "text": ""}
        })

        # 流式内容
        try:
            if gemini_history:
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(last_content, stream=True)
            else:
                response = model.generate_content(last_content, stream=True)

            total_tokens = 0
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    total_tokens += len(chunk.text) // 4 + 1
                    self._send_sse('content_block_delta', {
                        "type": "content_block_delta", "index": 0,
                        "delta": {"type": "text_delta", "text": chunk.text}
                    })

            # content_block_stop
            self._send_sse('content_block_stop', {
                "type": "content_block_stop", "index": 0
            })

            # message_delta
            self._send_sse('message_delta', {
                "type": "message_delta",
                "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                "usage": {"output_tokens": total_tokens}
            })

        except Exception as e:
            self._send_sse('content_block_delta', {
                "type": "content_block_delta", "index": 0,
                "delta": {"type": "text_delta", "text": f"[代理错误: {str(e)}]"}
            })

        # message_stop
        self._send_sse('message_stop', {"type": "message_stop"})

        # 结束流
        try:
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except Exception:
            pass

    def _handle_sync(self, model, gemini_history, last_content, model_name):
        """非流式响应"""
        if gemini_history:
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(last_content)
        else:
            response = model.generate_content(last_content)

        text = response.text if hasattr(response, 'text') else str(response)

        self._send_json(200, {
            "id": f"msg_{uuid.uuid4().hex[:24]}",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": text}],
            "model": model_name,
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0}
        })

    def _send_sse(self, event, data):
        """发送 SSE 事件"""
        msg = f"event: {event}\ndata: {json.dumps(data)}\n\n"
        self.wfile.write(msg.encode('utf-8'))
        self.wfile.flush()

    def _send_json(self, code, data):
        """发送 JSON 响应"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def main():
    server = ThreadedHTTPServer(('127.0.0.1', PORT), AnthropicProxyHandler)

    def shutdown(sig, frame):
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    print(f"Gemini 代理已启动: http://127.0.0.1:{PORT}")
    print(f"模型: {GEMINI_MODEL}")
    server.serve_forever()


if __name__ == '__main__':
    main()
