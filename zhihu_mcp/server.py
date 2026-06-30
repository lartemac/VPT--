"""
知乎搜索 MCP 服务器（stdio 模式）
封装知乎搜索和全网搜索 REST API，动态注入 X-Request-Timestamp
"""

import sys
import io
import json
import time
import urllib.request
import urllib.parse
import ssl

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")

ACCESS_SECRET = "YOUR_ZHIHU_ACCESS_SECRET"
ZHIHU_SEARCH_URL = "https://developer.zhihu.com/api/v1/content/zhihu_search"
GLOBAL_SEARCH_URL = "https://developer.zhihu.com/api/v1/content/global_search"

TOOLS = [
    {
        "name": "zhihu_search",
        "description": "在知乎站内搜索内容（回答、文章等）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词（2-100个字符）",
                },
                "count": {
                    "type": "integer",
                    "description": "返回条数（1-10，默认10）",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "global_search",
        "description": "通过知乎全网搜索，获取全平台内容（不仅限知乎站内）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词（2-100个字符）",
                },
                "count": {
                    "type": "integer",
                    "description": "返回条数（1-20，默认10）",
                },
            },
            "required": ["query"],
        },
    },
]


def write_response(obj):
    out = json.dumps(obj, ensure_ascii=False) + "\n"
    sys.stdout.buffer.write(out.encode("utf-8"))
    sys.stdout.buffer.flush()


def api_get(url, query, count):
    headers = {
        "Authorization": f"Bearer {ACCESS_SECRET}",
        "Content-Type": "application/json",
        "X-Request-Timestamp": str(int(time.time())),
    }
    params = urllib.parse.urlencode({"Query": query, "Count": count})
    full_url = f"{url}?{params}"
    req = urllib.request.Request(full_url, headers=headers)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        raw = resp.read()
        return raw.decode("utf-8", errors="replace")


def handle_request(req):
    method = req.get("method", "")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "zhihu-search", "version": "1.0.0"},
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        query = arguments.get("query", "")
        count = arguments.get("count", 10)

        try:
            if tool_name == "zhihu_search":
                result = api_get(ZHIHU_SEARCH_URL, query, min(count, 10))
            elif tool_name == "global_search":
                result = api_get(GLOBAL_SEARCH_URL, query, min(count, 20))
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"未知工具: {tool_name}"},
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": result}]},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"请求失败: {e}"}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"未知方法: {method}"},
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                write_response(response)
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()
