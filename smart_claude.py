#!/usr/bin/env python3
"""
Claude Code 智能启动器
自动检测 API 可用性，智谱限额时切换到 Gemini 备用

创建时间: 2026-04-15
创建系统: macOS
平台检测: if os.name == 'nt': Windows, else: macOS/Linux

用法:
  python3 smart_claude.py          # 自动选择后端
  python3 smart_claude.py --force-gemini  # 强制使用 Gemini
  python3 smart_claude.py --force-zhipu   # 强制使用智谱
  python3 smart_claude.py --status        # 仅检查状态
"""

import json
import os
import sys
import time
import subprocess
import signal
from pathlib import Path

# 平台检测
IS_WINDOWS = os.name == 'nt'

def get_project_dir():
    """获取项目目录"""
    script_dir = Path(__file__).parent.resolve()
    # 兼容两台电脑的路径
    if script_dir.name == 'VPT-初诊数据':
        return script_dir
    return script_dir

PROJECT_DIR = get_project_dir()
CONFIG_FILE = PROJECT_DIR / "api_config.json"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"❌ 未找到配置文件: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)


def get_settings_path():
    """获取 Claude Code settings.json 路径"""
    if IS_WINDOWS:
        return Path(os.environ.get('USERPROFILE', 'C:\\Users\\Administrator')) / '.claude' / 'settings.json'
    else:
        return Path.home() / '.claude' / 'settings.json'


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
            f"{url}/v1/messages",
            data=data,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
        )

        start = time.time()
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            body = json.loads(resp.read())
            elapsed = time.time() - start

            if status == 200:
                return True, f"可用 ({elapsed:.1f}s)"
            return False, f"HTTP {status}"

    except urllib.error.HTTPError as e:
        if e.code == 429:
            try:
                body = json.loads(e.read())
                msg = body.get('error', {}).get('message', '限额')
                # 提取重置时间
                if '重置' in msg:
                    reset_time = msg.split('重置')[-1].strip('。 ').strip()
                    return False, f"限额 (重置: {reset_time})"
            except Exception:
                pass
            return False, "已达限额 (429)"
        elif e.code == 401:
            return False, "认证失败 (401)"
        else:
            return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"连接失败 ({str(e)[:50]})"


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
        return False, f"连接失败 ({str(e)[:50]})"


def update_settings(backend, config):
    """更新 Claude Code settings.json"""
    settings_path = get_settings_path()
    if not settings_path.exists():
        print(f"⚠️ 未找到 settings.json: {settings_path}")
        return False

    with open(settings_path) as f:
        settings = json.load(f)

    if 'env' not in settings:
        settings['env'] = {}

    if backend == 'zhipu':
        settings['env']['ANTHROPIC_AUTH_TOKEN'] = config['glm']['api_key']
        settings['env']['ANTHROPIC_BASE_URL'] = config['glm'].get('anthropic_url', 'https://open.bigmodel.cn/api/anthropic')
        if 'ANTHROPIC_MODEL' in settings['env']:
            del settings['env']['ANTHROPIC_MODEL']
    elif backend == 'gemini':
        proxy_port = config['gemini'].get('proxy_port', 4000)
        settings['env']['ANTHROPIC_AUTH_TOKEN'] = 'gemini-proxy'
        settings['env']['ANTHROPIC_BASE_URL'] = f"http://127.0.0.1:{proxy_port}"
        if 'ANTHROPIC_MODEL' in settings['env']:
            del settings['env']['ANTHROPIC_MODEL']

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    return True


def start_gemini_proxy(config):
    """后台启动 Gemini 代理"""
    proxy_script = PROJECT_DIR / "gemini_proxy.py"
    if not proxy_script.exists():
        print(f"❌ 未找到代理脚本: {proxy_script}")
        return None

    proxy_port = config['gemini'].get('proxy_port', 4000)

    # 检查端口是否已被占用（代理已在运行）
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', proxy_port))
        sock.close()
        print(f"✅ Gemini 代理已在运行 (端口 {proxy_port})")
        return True
    except Exception:
        sock.close()

    # 启动代理
    env = os.environ.copy()
    env['GEMINI_API_KEY'] = config['gemini']['api_key']

    if IS_WINDOWS:
        CREATE_NO_WINDOW = 0x08000000
        proc = subprocess.Popen(
            [sys.executable, str(proxy_script)],
            env=env,
            creationflags=CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        proc = subprocess.Popen(
            [sys.executable, str(proxy_script)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    # 等待代理启动
    for _ in range(10):
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('127.0.0.1', proxy_port))
            sock.close()
            print(f"✅ Gemini 代理已启动 (端口 {proxy_port}, PID: {proc.pid})")
            return True
        except Exception:
            sock.close()

    print(f"⚠️ 代理启动超时")
    return False


def check_status(config):
    """仅检查状态，不启动"""
    print("=" * 50)
    print("  Claude Code API 状态检查")
    print("=" * 50)

    # 智谱
    print(f"\n📡 智谱 GLM ({config['glm']['latest_model']})")
    ok, msg = test_zhipu(config)
    print(f"   {'✅' if ok else '❌'} {msg}")

    # Gemini
    print(f"\n📡 Gemini ({config['gemini']['model']})")
    ok, msg = test_gemini(config)
    print(f"   {'✅' if ok else '❌'} {msg}")

    # 当前配置
    settings_path = get_settings_path()
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
        base_url = settings.get('env', {}).get('ANTHROPIC_BASE_URL', '未设置')
        print(f"\n🔧 当前后端: {base_url}")

    print()


def main():
    config = load_config()

    # 解析参数
    force = None
    status_only = False
    for arg in sys.argv[1:]:
        if arg == '--force-gemini':
            force = 'gemini'
        elif arg == '--force-zhipu':
            force = 'zhipu'
        elif arg == '--status':
            status_only = True

    if status_only:
        check_status(config)
        return

    print("🔍 检测 API 可用性...\n")

    # 确定使用哪个后端
    backend = None

    if force == 'gemini':
        print("⚡ 强制使用 Gemini")
        backend = 'gemini'
    elif force == 'zhipu':
        print("⚡ 强制使用智谱")
        backend = 'zhipu'
    else:
        # 自动检测
        print(f"📡 测试智谱 ({config['glm']['latest_model']})...", end=" ")
        zhipu_ok, zhipu_msg = test_zhipu(config)
        print(f"{'✅' if zhipu_ok else '❌'} {zhipu_msg}")

        if zhipu_ok:
            backend = 'zhipu'
        else:
            print(f"\n📡 测试 Gemini ({config['gemini']['model']})...", end=" ")
            gemini_ok, gemini_msg = test_gemini(config)
            print(f"{'✅' if gemini_ok else '❌'} {gemini_msg}")

            if gemini_ok:
                backend = 'gemini'
            else:
                print("\n❌ 两个 API 都不可用，请检查网络或等待限额重置")
                sys.exit(1)

    # 切换后端
    print(f"\n🔄 切换到: {backend.upper()}")

    if backend == 'gemini':
        # 启动 Gemini 代理
        print("🚀 启动 Gemini 代理...")
        if not start_gemini_proxy(config):
            print("❌ 代理启动失败")
            sys.exit(1)

    # 更新 settings.json
    if update_settings(backend, config):
        print(f"✅ settings.json 已更新 ({backend})")
    else:
        print(f"⚠️ settings.json 更新失败")
        sys.exit(1)

    # 启动 Claude Code
    print(f"\n{'='*50}")
    print(f"  🚀 启动 Claude Code ({backend})")
    print(f"{'='*50}\n")

    claude_cmd = 'claude.cmd' if IS_WINDOWS else 'claude'
    os.execvp(claude_cmd, [claude_cmd])


if __name__ == '__main__':
    main()
