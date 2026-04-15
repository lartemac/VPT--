#!/usr/bin/env python3
"""
Claude Code 智能启动器
自动检测 API 可用性，智谱限额时切换到 Gemini 备用

创建时间: 2026-04-15
创建系统: macOS
平台检测: if os.name == 'nt': Windows, else: macOS/Linux

用法:
  python3 smart_claude.py --auto         # 自动模式（被 claude 命令自动调用）
  python3 smart_claude.py --status       # 检查状态
  python3 smart_claude.py --force-gemini # 强制 Gemini
  python3 smart_claude.py --force-zhipu  # 强制智谱
"""

import json
import os
import sys
import time
import tempfile
import subprocess
from pathlib import Path

# Windows 控制台 UTF-8 支持
if os.name == 'nt':
    os.system('')  # 启用 ANSI 转义
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

IS_WINDOWS = os.name == 'nt'

def get_project_dir():
    return Path(__file__).parent.resolve()

PROJECT_DIR = get_project_dir()
CONFIG_FILE = PROJECT_DIR / "api_config.json"
CACHE_FILE = Path(tempfile.gettempdir()) / "claude_api_cache.json"
CACHE_TTL = 180  # 缓存有效期：3分钟


def load_config():
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, encoding='utf-8') as f:
        return json.load(f)


def get_settings_path():
    base = Path(os.environ.get('USERPROFILE', str(Path.home()))) / '.claude' if IS_WINDOWS else Path.home() / '.claude'
    local = base / 'settings.local.json'
    shared = base / 'settings.json'
    return local if local.exists() else shared


def read_cache():
    """读取缓存"""
    try:
        if CACHE_FILE.exists():
            cache = json.loads(CACHE_FILE.read_text())
            age = time.time() - cache.get('ts', 0)
            if age < CACHE_TTL:
                return cache
    except Exception:
        pass
    return None


def write_cache(backend, zhipu_ok, reset_time=None):
    """写入缓存"""
    try:
        CACHE_FILE.write_text(json.dumps({
            'ts': time.time(),
            'backend': backend,
            'zhipu_ok': zhipu_ok,
            'reset_time': reset_time
        }))
    except Exception:
        pass


def test_zhipu(config):
    """测试智谱 API 是否可用"""
    api_key = config['glm']['api_key']
    url = config['glm'].get('anthropic_url', 'https://open.bigmodel.cn/api/anthropic')

    try:
        import urllib.request
        import urllib.error

        data = json.dumps({
            "model": config['glm']['latest_model'],
            "max_tokens": 5,
            "messages": [{"role": "user", "content": "hi"}]
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{url}/v1/messages", data=data,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
        )

        start = time.time()
        with urllib.request.urlopen(req, timeout=15) as resp:
            elapsed = time.time() - start
            if resp.status == 200:
                return True, f"可用 ({elapsed:.1f}s)", None
            return False, f"HTTP {resp.status}", None

    except urllib.error.HTTPError as e:
        reset_time = None
        if e.code == 429:
            try:
                body = json.loads(e.read())
                msg = body.get('error', {}).get('message', '')
                if '重置' in msg:
                    reset_time = msg.split('重置')[-1].strip('。 ').strip()
                    return False, f"限额 (重置: {reset_time})", reset_time
            except Exception:
                pass
            return False, "已达限额 (429)", None
        return False, f"HTTP {e.code}", None
    except Exception as e:
        return False, f"连接失败", None


def test_gemini(config):
    """测试 Gemini API 是否可用"""
    api_key = config['gemini']['api_key']
    model_name = config['gemini'].get('model', 'gemini-2.5-flash')
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content('hi', generation_config=genai.GenerationConfig(max_output_tokens=5))
        if response.text:
            return True, f"可用 ({model_name})"
        return False, "无响应"
    except Exception as e:
        return False, f"连接失败"


def update_settings(backend, config):
    """更新 Claude Code settings.json"""
    settings_path = get_settings_path()
    if not settings_path.exists():
        return False

    with open(settings_path, encoding='utf-8') as f:
        settings = json.load(f)

    if 'env' not in settings:
        settings['env'] = {}

    if backend == 'zhipu':
        settings['env']['ANTHROPIC_AUTH_TOKEN'] = config['glm']['api_key']
        settings['env']['ANTHROPIC_BASE_URL'] = config['glm'].get('anthropic_url', 'https://open.bigmodel.cn/api/anthropic')
    elif backend == 'gemini':
        proxy_port = config['gemini'].get('proxy_port', 4000)
        settings['env']['ANTHROPIC_AUTH_TOKEN'] = 'gemini-proxy'
        settings['env']['ANTHROPIC_BASE_URL'] = f"http://127.0.0.1:{proxy_port}"

    for key in ['ANTHROPIC_MODEL']:
        settings['env'].pop(key, None)

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    return True


def is_proxy_running(port):
    """检查代理是否在运行"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', port))
        sock.close()
        return True
    except Exception:
        sock.close()
        return False


def start_gemini_proxy(config):
    """后台启动 Gemini 代理"""
    proxy_script = PROJECT_DIR / "gemini_proxy.py"
    if not proxy_script.exists():
        return False

    proxy_port = config['gemini'].get('proxy_port', 4000)
    if is_proxy_running(proxy_port):
        return True

    proc = subprocess.Popen(
        [sys.executable, str(proxy_script)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    for _ in range(10):
        time.sleep(0.5)
        if is_proxy_running(proxy_port):
            return True
    return False


def auto_mode(config):
    """自动模式：被 claude 命令自动调用，静默执行"""
    if not config:
        return  # 无配置文件，跳过

    # 1. 读缓存：智谱上次正常且未过期 → 直接返回，不做任何检测
    cache = read_cache()
    if cache and cache.get('zhipu_ok'):
        return  # 3分钟内检测过智谱正常，跳过

    # 2. 缓存过期或上次异常 → 检测智谱
    zhipu_ok, msg, reset_time = test_zhipu(config)

    if zhipu_ok:
        # 智谱恢复了 → 切回智谱
        write_cache('zhipu', True)
        update_settings('zhipu', config)
        return

    # 3. 智谱不可用 → 检测 Gemini
    write_cache('zhipu', False, reset_time)
    gemini_ok, gemini_msg = test_gemini(config)

    if gemini_ok:
        # 启动代理并切换
        if start_gemini_proxy(config):
            update_settings('gemini', config)
            print(f"⚠️ 智谱 {msg} → 已自动切换 Gemini")
            write_cache('gemini', False, reset_time)
        else:
            print(f"⚠️ 智谱 {msg}, Gemini 代理启动失败")
    else:
        print(f"⚠️ 智谱 {msg}, Gemini {gemini_msg}")
        print("   两个 API 都不可用，请等待限额重置")


def interactive_mode(force=None):
    """交互模式：手动选择后端"""
    config = load_config()
    if not config:
        print("❌ 未找到 api_config.json")
        sys.exit(1)

    backend = force
    if not backend:
        print("🔍 检测 API 可用性...\n")
        zhipu_ok, zhipu_msg, _ = test_zhipu(config)
        print(f"📡 智谱: {'✅' if zhipu_ok else '❌'} {zhipu_msg}")
        if zhipu_ok:
            backend = 'zhipu'
        else:
            gemini_ok, gemini_msg = test_gemini(config)
            print(f"📡 Gemini: {'✅' if gemini_ok else '❌'} {gemini_msg}")
            backend = 'gemini' if gemini_ok else None

    if not backend:
        print("\n❌ 两个 API 都不可用")
        sys.exit(1)

    print(f"\n🔄 切换到: {backend.upper()}")
    if backend == 'gemini' and not start_gemini_proxy(config):
        print("❌ 代理启动失败")
        sys.exit(1)

    update_settings(backend, config)
    print(f"✅ 已更新 settings.json ({backend})")

    claude_cmd = 'claude.cmd' if IS_WINDOWS else 'claude'
    os.execvp(claude_cmd, [claude_cmd])


def check_status(config):
    """状态检查"""
    print("=" * 50)
    print("  Claude Code API 状态检查")
    print("=" * 50)

    zhipu_ok, zhipu_msg, reset = test_zhipu(config)
    print(f"\n📡 智谱 GLM ({config['glm']['latest_model']})")
    print(f"   {'✅' if zhipu_ok else '❌'} {zhipu_msg}")

    gemini_ok, gemini_msg = test_gemini(config)
    print(f"\n📡 Gemini ({config['gemini']['model']})")
    print(f"   {'✅' if gemini_ok else '❌'} {gemini_msg}")

    settings_path = get_settings_path()
    if settings_path.exists():
        with open(settings_path, encoding='utf-8') as f:
            settings = json.load(f)
        url = settings.get('env', {}).get('ANTHROPIC_BASE_URL', '未设置')
        backend = '智谱' if 'bigmodel' in url else 'Gemini' if '127.0.0.1' in url else url
        print(f"\n🔧 当前后端: {backend}")

    cache = read_cache()
    if cache:
        age = int(time.time() - cache.get('ts', 0))
        print(f"📋 缓存: {cache.get('backend', '?')} (检测于 {age}s 前)")

    print()


def main():
    args = sys.argv[1:]
    config = load_config()

    if '--auto' in args:
        auto_mode(config)
        return

    if '--status' in args:
        if not config:
            print("❌ 未找到 api_config.json"); return
        check_status(config)
        return

    if '--force-gemini' in args:
        interactive_mode(force='gemini')
    elif '--force-zhipu' in args:
        interactive_mode(force='zhipu')
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
