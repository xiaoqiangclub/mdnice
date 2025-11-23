#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代理功能测试脚本
"""

from mdnice import to_wechat


def test_local_browser_with_proxy():
    """测试本地浏览器使用代理"""
    print("\n" + "=" * 70)
    print("测试 1: 本地浏览器 + HTTP 代理")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# 测试标题\n\n这是一个测试内容。',
            headless=False,  # 显示浏览器窗口，方便调试
            output_dir='output',
            proxy={
                'server': 'http://127.0.0.1:7890'  # 替换为你的代理地址
            },
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_local_browser_with_socks5():
    """测试本地浏览器使用 SOCKS5 代理"""
    print("\n" + "=" * 70)
    print("测试 2: 本地浏览器 + SOCKS5 代理")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# SOCKS5 测试\n\n使用 SOCKS5 代理。',
            headless=False,
            output_dir='output',
            proxy={
                'server': 'socks5://192.168.1.111:20170'  # 替换为你的 SOCKS5 代理
            },
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_local_browser_with_auth_proxy():
    """测试本地浏览器使用需要认证的代理"""
    print("\n" + "=" * 70)
    print("测试 3: 本地浏览器 + 认证代理")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# 认证代理测试\n\n使用需要用户名密码的代理。',
            headless=False,
            output_dir='output',
            proxy={
                'server': 'http://proxy.example.com:8080',
                'username': 'your_username',  # 替换为实际用户名
                'password': 'your_password'  # 替换为实际密码
            },
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_remote_browser_with_proxy():
    """测试远程浏览器使用代理"""
    print("\n" + "=" * 70)
    print("测试 4: 远程浏览器 + HTTP 代理")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# 远程浏览器测试\n\n使用远程浏览器 + 代理。',
            browser_ws_endpoint='ws://localhost:3000',
            browser_token='xiaoqiangclub',
            output_dir='output',
            proxy={
                'server': 'http://127.0.0.1:7890'
            },
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_proxy_with_bypass():
    """测试代理绕过功能"""
    print("\n" + "=" * 70)
    print("测试 5: 代理绕过规则")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# 代理绕过测试\n\n本地地址不使用代理。',
            headless=False,
            output_dir='output',
            proxy={
                'server': 'http://127.0.0.1:7890',
                'bypass': 'localhost,127.0.0.1,*.local,192.168.*'  # 这些地址不走代理
            },
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_without_proxy():
    """对照组：不使用代理"""
    print("\n" + "=" * 70)
    print("测试 6: 不使用代理（对照组）")
    print("=" * 70)

    try:
        result = to_wechat(
            markdown='# 无代理测试\n\n直接连接。',
            headless=False,
            output_dir='output',
            wait_timeout=60
        )
        print("✅ 测试成功！")
        print(f"📄 HTML 长度: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    mdnice 代理功能测试                            ║
╚══════════════════════════════════════════════════════════════════╝

📌 测试前准备：
1. 确保代理服务器正在运行（例如 Clash、V2Ray 等）
2. 修改脚本中的代理地址为实际地址
3. 常见代理端口：
   - Clash: 7890 (HTTP), 7891 (SOCKS5)
   - V2Ray: 10809 (HTTP), 10808 (SOCKS5)
   - SSR: 1080 (SOCKS5)

🔍 选择要运行的测试：
""")

    tests = {
        '1': ('本地浏览器 + HTTP 代理', test_local_browser_with_proxy),
        '2': ('本地浏览器 + SOCKS5 代理', test_local_browser_with_socks5),
        '3': ('本地浏览器 + 认证代理', test_local_browser_with_auth_proxy),
        '4': ('远程浏览器 + HTTP 代理', test_remote_browser_with_proxy),
        '5': ('代理绕过规则', test_proxy_with_bypass),
        '6': ('不使用代理（对照组）', test_without_proxy),
        'all': ('运行所有测试', None)
    }

    for key, (name, _) in tests.items():
        print(f"  {key}. {name}")

    choice = input("\n请选择测试编号（1-6 或 all）: ").strip()

    if choice == 'all':
        # 运行除了需要认证的所有测试
        for key in ['1', '2', '5', '6']:
            tests[key][1]()
    elif choice in tests and choice != 'all':
        tests[choice][1]()
    else:
        print("❌ 无效的选择")