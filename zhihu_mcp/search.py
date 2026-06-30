"""知乎搜索命令行工具（全网搜索 + 站内搜索）

用法：
  python search.py "关键词" [数量] [模式]
  模式：global（默认，全网搜索）或 zhihu（站内搜索）

示例：
  python search.py "口腔医学" 10         # 全网搜索，10条
  python search.py "VPT活髓" 5 zhihu     # 站内搜索，5条
"""
import sys, io, json, time, urllib.request, urllib.parse, ssl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ACCESS_SECRET = "YOUR_ZHIHU_ACCESS_SECRET"
URLS = {
    "global": "https://developer.zhihu.com/api/v1/content/global_search",
    "zhihu": "https://developer.zhihu.com/api/v1/content/zhihu_search",
}
MAX_COUNT = {"global": 20, "zhihu": 10}


def search(query, count=10, mode="global"):
    max_n = MAX_COUNT.get(mode, 20)
    params = urllib.parse.urlencode({"Query": query, "Count": min(count, max_n)})
    url = f"{URLS.get(mode, URLS['global'])}?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {ACCESS_SECRET}",
        "X-Request-Timestamp": str(int(time.time())),
        "Content-Type": "application/json",
    })
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def print_results(items):
    if not items:
        print("没有找到相关结果")
        return
    for i, item in enumerate(items, 1):
        title = item.get("Title", "无标题")
        url = item.get("Url", "")
        author = item.get("AuthorName", "匿名")
        votes = item.get("VoteUpCount", 0)
        comments = item.get("CommentCount", 0)
        ctype = item.get("ContentType", "")
        text = item.get("ContentText", "").replace("<em>", "").replace("</em>", "")
        authority = item.get("AuthorityLevel", "")
        score = item.get("RankingScore", "")
        print(f"[{i}] {title}")
        print(f"    作者: {author} | 赞同: {votes} | 评论: {comments} | 类型: {ctype} | 权威: {authority}", end="")
        if score:
            print(f" | 匹配度: {score:.2f}", end="")
        print()
        print(f"    链接: {url}")
        print(f"    摘要: {text[:200]}")
        print()


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "AI"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    mode = sys.argv[3] if len(sys.argv) > 3 else "global"
    if mode not in URLS:
        mode = "global"
    data = search(q, n, mode)
    if data.get("Code") != 0:
        print(f"搜索失败({data.get('Code')}): {data.get('Message')}")
        sys.exit(1)
    print_results(data.get("Data", {}).get("Items", []))
