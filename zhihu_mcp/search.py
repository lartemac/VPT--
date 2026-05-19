"""知乎全网搜索命令行工具"""
import sys, io, json, time, urllib.request, urllib.parse, ssl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ACCESS_SECRET = "11d88bdc650f2bf0ad13bab266277fffc2a3383e"
API_URL = "https://developer.zhihu.com/api/v1/content/global_search"

def search(query, count=10):
    params = urllib.parse.urlencode({"Query": query, "Count": min(count, 20)})
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {ACCESS_SECRET}",
        "X-Request-Timestamp": str(int(time.time())),
        "Content-Type": "application/json",
    })
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "AI"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    data = search(q, n)
    if data.get("Code") != 0:
        print(f"搜索失败: {data.get('Message')}")
        sys.exit(1)
    items = data.get("Data", {}).get("Items", [])
    if not items:
        print("没有找到相关结果")
        sys.exit(0)
    for i, item in enumerate(items, 1):
        title = item.get("Title", "无标题")
        url = item.get("Url", "")
        author = item.get("AuthorName", "匿名")
        votes = item.get("VoteUpCount", 0)
        comments = item.get("CommentCount", 0)
        ctype = item.get("ContentType", "")
        text = item.get("ContentText", "").replace("<em>", "").replace("</em>", "")
        authority = item.get("AuthorityLevel", "")
        print(f"[{i}] {title}")
        print(f"    作者: {author} | 赞同: {votes} | 评论: {comments} | 类型: {ctype} | 权威: {authority}")
        print(f"    链接: {url}")
        print(f"    摘要: {text[:200]}")
        print()
