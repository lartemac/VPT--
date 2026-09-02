"""DeepSeek 视觉模型调用工具（deepseek-v4-flash-vision-exp）

用法：
  python vision.py "图片路径或URL" "问题"
  python vision.py "图片路径或URL"            # 默认问题：详细描述图片

支持：本地图片文件（自动 base64 编码）或 http(s) 网络图片链接。
"""
import sys, os, io, json, base64, urllib.request, ssl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-flash-vision-exp"
SECRET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vision_secret.json")

# 常见图片扩展名 → MIME 类型
EXT_MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def load_api_key():
    """读取 API Key：优先环境变量 DEEPSEEK_API_KEY（手动提供，不留盘），其次本地密钥文件"""
    env_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if env_key:
        return env_key
    try:
        with open(SECRET_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("api_key", "")
    except Exception:
        return ""


def ask_vision(image, prompt):
    """调用视觉模型，返回文字结果。image 为本地路径或 http(s) URL。"""
    if image.startswith("http://") or image.startswith("https://"):
        # 网络图片：直接传 URL
        img_block = {"type": "image_url", "image_url": {"url": image}}
    else:
        # 本地图片：读文件转 base64
        if not os.path.exists(image):
            print(f"错误：图片文件不存在：{image}")
            sys.exit(1)
        ext = os.path.splitext(image)[1].lower()
        mime = EXT_MIME.get(ext, "image/jpeg")
        with open(image, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        img_block = {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}

    api_key = load_api_key()
    if not api_key:
        print("错误：未找到 API Key，请检查 vision_secret.json")
        sys.exit(1)

    payload = {
        "model": MODEL,
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    img_block,
                ],
            }
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # 解析返回
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"调用失败：{json.dumps(data, ensure_ascii=False)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('用法：python vision.py "图片路径或URL" ["问题"]')
        sys.exit(1)
    image = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "请详细描述这张图片的内容，包括其中的文字、数据、图表信息。"
    print(ask_vision(image, prompt))
