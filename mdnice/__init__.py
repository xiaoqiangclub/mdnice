# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:0.672Z
# 文件描述：将 Markdown 转换为微信公众号、知乎、稀土掘金等平台格式(mdnice - Markdown to Multi-Platform Converter)
# 文件路径：mdnice/__init__.py

"""
mdnice - Markdown 多平台格式转换工具

支持转换为微信公众号、知乎、稀土掘金格式，支持本地浏览器和远程浏览器。
"""

# 导入版本信息
from .__version__ import (
    __version__,
    __author__,
    __email__,
    __license__,
    __copyright__,
    __url__,
    __description__,
)

# 导入图床上传器
from .image_uploaders import (
    SMUploader,
    ImgURLUploader,
    LuoGuoUploader,
    QiniuUploader,
    AliyunOSSUploader,
    UpyunUploader,
    GitHubUploader,
    LocalStorageUploader,
    WechatUploader,
    WechatUploadType,
    create_smms_uploader,
    create_qiniu_uploader,
    create_github_uploader,
    create_local_uploader,
    create_wechat_uploader,
)

import os
import re
import time
import random
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, Browser, Page, Playwright, TimeoutError as PlaywrightTimeoutError
from typing import Union, List, Optional, Callable, Dict, Any, Literal

__all__ = [
    'convert',
    'to_wechat',
    'to_zhihu',
    'to_juejin',
    'MarkdownConverter',
    'ConversionError',
    'ImageUploadMode',
    'CodeTheme',
    'BrowserType',
    'BrowserConnectionType',
    '__version__',
    # 图床上传器类
    'SMUploader',
    'ImgURLUploader',
    'LuoGuoUploader',
    'QiniuUploader',
    'AliyunOSSUploader',
    'UpyunUploader',
    'GitHubUploader',
    'LocalStorageUploader',
    'WechatUploader',
    'WechatUploadType',
    # 便捷函数
    'create_smms_uploader',
    'create_qiniu_uploader',
    'create_github_uploader',
    'create_local_uploader',
    'create_wechat_uploader',
]

Platform = Literal['wechat', 'zhihu', 'juejin']
ImageUploadMode = Literal['local', 'remote', 'all']
CodeTheme = Literal['wechat', 'atom-one-dark', 'atom-one-light', 'monokai', 'github', 'vs2015', 'xcode']
BrowserType = Literal['chromium', 'firefox', 'webkit']
BrowserConnectionType = Literal['auto', 'cdp', 'playwright']


class ConversionError(Exception):
    """转换过程中的自定义异常"""
    pass


class MarkdownConverter:
    """Markdown转多平台格式转换器"""

    AVAILABLE_THEMES = [
        'normal', 'shanchui', 'rose', 'fullStackBlue', 'nightPurple',
        'cuteGreen', 'extremeBlack', 'orangeHeart', 'ink', 'purple',
        'green', 'cyan', 'wechatFormat', 'blueCyan', 'blueMountain',
        'geekBlack', 'red', 'blue', 'scienceBlue', 'simple'
    ]

    THEME_NAMES = {
        'normal': '默认主题', 'shanchui': '山吹', 'rose': '蔷薇紫',
        'fullStackBlue': '全栈蓝', 'nightPurple': '凝夜紫', 'cuteGreen': '萌绿',
        'extremeBlack': '极简黑', 'orangeHeart': '橙心', 'ink': '墨黑',
        'purple': '姹紫', 'green': '绿意', 'cyan': '嫩青',
        'wechatFormat': 'WeChat-Format', 'blueCyan': '兰青',
        'blueMountain': '前端之巅同款', 'geekBlack': '极客黑',
        'red': '红绯', 'blue': '蓝莹', 'scienceBlue': '科技蓝', 'simple': '简'
    }

    AVAILABLE_CODE_THEMES = [
        'wechat', 'atom-one-dark', 'atom-one-light',
        'monokai', 'github', 'vs2015', 'xcode'
    ]

    CODE_THEME_CONFIG = {
        'wechat': {'id': 'nice-menu-codetheme-wechat', 'name': '微信代码主题'},
        'atom-one-dark': {'id': 'nice-menu-codetheme-atomOneDark', 'name': 'Atom One Dark'},
        'atom-one-light': {'id': 'nice-menu-codetheme-atomOneLight', 'name': 'Atom One Light'},
        'monokai': {'id': 'nice-menu-codetheme-monokai', 'name': 'Monokai'},
        'github': {'id': 'nice-menu-codetheme-github', 'name': 'GitHub'},
        'vs2015': {'id': 'nice-menu-codetheme-vs2015', 'name': 'VS2015'},
        'xcode': {'id': 'nice-menu-codetheme-xcode', 'name': 'Xcode'}
    }

    PLATFORM_CONFIG = {
        'wechat': {'button_id': 'nice-sidebar-wechat', 'name': '微信公众号', 'suffix': 'wechat'},
        'zhihu': {'button_id': 'nice-sidebar-zhihu', 'name': '知乎', 'suffix': 'zhihu'},
        'juejin': {'button_id': 'nice-sidebar-juejin', 'name': '稀土掘金', 'suffix': 'juejin'}
    }

    def __init__(self,
                 headless: bool = True,
                 wait_timeout: int = 30,
                 retry_count: int = 1,
                 on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
                 editor_url: Optional[Union[str, List[str]]] = None,
                 image_uploader: Optional[Callable[[str], str]] = None,
                 image_upload_mode: ImageUploadMode = 'local',
                 code_theme: CodeTheme = 'atom-one-dark',
                 mac_style: bool = True,
                 browser_ws_endpoint: Optional[str] = None,
                 browser_type: BrowserType = 'chromium',
                 browser_connection_type: BrowserConnectionType = 'auto',
                 browser_token: Optional[str] = None,
                 clean_html: bool = True,
                 proxy: Optional[Dict[str, str]] = None) -> None:
        """
        初始化转换器

        :param headless: 是否使用无头模式（远程浏览器时忽略）
        :param wait_timeout: 等待超时时间（秒）
        :param retry_count: 失败重试次数
        :param on_error: 错误通知回调函数
        :param editor_url: 自定义编辑器网址（字符串或列表）
        :param image_uploader: 图片上传回调函数
        :param image_upload_mode: 图片上传模式（local/remote/all）
        :param code_theme: 代码主题
        :param mac_style: 是否启用 Mac 风格
        :param browser_ws_endpoint: 远程浏览器 WebSocket 端点
        :param browser_type: 浏览器类型（chromium/firefox/webkit）
        :param browser_connection_type: 连接类型（auto/cdp/playwright）
        :param browser_token: 远程浏览器访问令牌
        :param clean_html: 是否清理HTML中的编辑器标记（默认True）
        :param proxy: 代理配置，例如 {'server': 'http://proxy.com:8080', 'username': 'user', 'password': 'pass'}
        """
        self.headless: bool = headless
        self.wait_timeout: int = wait_timeout * 1000  # Playwright 使用毫秒
        self.retry_count: int = retry_count
        self.on_error: Optional[Callable[[str, Dict[str, Any]], None]] = on_error
        self.image_uploader: Optional[Callable[[str], str]] = image_uploader
        self.image_upload_mode: ImageUploadMode = image_upload_mode
        self.code_theme: CodeTheme = code_theme
        self.mac_style: bool = mac_style
        self.clean_html: bool = clean_html
        self.proxy: Optional[Dict[str, str]] = proxy

        # 远程浏览器配置
        self.browser_ws_endpoint: Optional[str] = browser_ws_endpoint
        self.browser_type: BrowserType = browser_type
        self.browser_connection_type: BrowserConnectionType = browser_connection_type
        self.browser_token: Optional[str] = browser_token

        # Playwright 相关对象
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        # 默认和备用地址
        self.default_url: str = "https://xiaoqiangclub.github.io/md/"
        self.backup_url: str = "https://whaoa.github.io/markdown-nice/"

        # 构建URL列表（优先级：自定义 > 默认 > 备用）
        self.url_list: List[str] = []

        # 处理 editor_url 参数（支持字符串或列表）
        if editor_url:
            if isinstance(editor_url, str):
                self.url_list.append(editor_url)
                print(f"🔧 使用自定义编辑器地址: {editor_url}")
            elif isinstance(editor_url, list):
                self.url_list.extend(editor_url)
                print(f"🔧 使用自定义编辑器地址列表: {len(editor_url)} 个")
                for idx, url in enumerate(editor_url, 1):
                    print(f"   {idx}. {url}")
            else:
                raise ValueError("editor_url 必须是字符串或字符串列表")

        # 添加默认地址（如果不在列表中）
        if self.default_url not in self.url_list:
            self.url_list.append(self.default_url)

        # 添加备用地址（如果不在列表中）
        if self.backup_url not in self.url_list:
            self.url_list.append(self.backup_url)

        self.current_url: str = self.url_list[0]
        self.current_url_index: int = 0

        print(f"📋 可用地址列表: {len(self.url_list)} 个")
        for idx, url in enumerate(self.url_list, 1):
            if editor_url and url in (editor_url if isinstance(editor_url, list) else [editor_url]):
                url_type = "自定义"
            elif url == self.default_url:
                url_type = "默认"
            elif url == self.backup_url:
                url_type = "备用"
            else:
                url_type = "其他"
            print(f"   {idx}. [{url_type}] {url}")

        # 代理配置提示
        if self.proxy:
            proxy_server = self.proxy.get('server', 'N/A')
            print(f"🌐 代理配置: {proxy_server}")
            if 'username' in self.proxy:
                print(f"   认证: {'*' * 8}")

        # 浏览器模式提示
        if self.browser_ws_endpoint:
            connection_type_name = {
                'auto': '自动检测',
                'cdp': 'CDP (browserless)',
                'playwright': 'Playwright 协议'
            }
            print(f"🌐 浏览器模式: 远程浏览器")
            print(f"   WebSocket: {self.browser_ws_endpoint}")
            print(
                f"   连接类型: {connection_type_name.get(self.browser_connection_type, self.browser_connection_type)}")
            print(f"   浏览器类型: {self.browser_type}")
            if self.browser_token:
                print(f"   Token: {'*' * 8}{self.browser_token[-4:] if len(self.browser_token) > 4 else '****'}")
        else:
            print(f"💻 浏览器模式: 本地浏览器 ({'无头' if self.headless else '有头'})")

        # 代码主题提示
        if self.code_theme not in self.AVAILABLE_CODE_THEMES:
            print(f"⚠️ 警告: 代码主题 '{self.code_theme}' 无效，将使用默认主题 'atom-one-dark'")
            self.code_theme = 'atom-one-dark'
        else:
            print(f"💻 代码主题: {self.CODE_THEME_CONFIG[self.code_theme]['name']}")

        print(f"🍎 Mac 风格: {'已启用' if self.mac_style else '已禁用'}")
        print(f"⏱️ 超时时间: {wait_timeout} 秒")

        # 图片上传功能提示
        if self.image_uploader:
            mode_names = {
                'local': '仅本地图片',
                'remote': '仅网络图片',
                'all': '所有图片'
            }
            print(f"📤 已启用图片自动上传功能 [模式: {mode_names[self.image_upload_mode]}]")
        elif self.image_upload_mode != 'local':
            print(f"⚠️ 警告: 未设置图片上传函数，image_upload_mode 参数将被忽略")

    def _clean_html(self, html_content: str) -> str:
        """
        清理HTML中的编辑器标记

        移除：
        - data-tool="mdnice编辑器"
        - data-website="https://www.mdnice.com"
        - 其他 mdnice 相关属性

        :param html_content: 原始HTML内容
        :return: 清理后的HTML内容
        """
        if not self.clean_html:
            return html_content

        try:
            import re

            # 移除 data-tool 属性
            html_content = re.sub(
                r'\s*data-tool="mdnice编辑器"',
                '',
                html_content
            )

            # 移除 data-website 属性
            html_content = re.sub(
                r'\s*data-website="[^"]*"',
                '',
                html_content
            )

            # 可选：移除其他 mdnice 相关的 data 属性
            # html_content = re.sub(
            #     r'\s*data-mdnice-[^=]*="[^"]*"',
            #     '',
            #     html_content
            # )

            print("✅ HTML 已清理编辑器标记")
            return html_content

        except Exception as e:
            print(f"⚠️ HTML 清理失败: {e}")
            # 清理失败也返回原内容，不影响功能
            return html_content

    def _build_ws_url_with_token(self, ws_endpoint: str, token: Optional[str]) -> str:
        """
        构建带 Token 的 WebSocket URL

        :param ws_endpoint: WebSocket 端点
        :param token: 访问令牌
        :return: 完整的 WebSocket URL
        """
        if not token:
            return ws_endpoint

        if '?' in ws_endpoint:
            return f"{ws_endpoint}&token={token}"
        else:
            return f"{ws_endpoint}?token={token}"

    def _detect_connection_type(self, ws_endpoint: str) -> BrowserConnectionType:
        """
        自动检测连接类型

        :param ws_endpoint: WebSocket 端点
        :return: 连接类型
        """
        if 'browserless' in ws_endpoint.lower():
            return 'cdp'

        if 'playwright' in ws_endpoint.lower():
            return 'playwright'

        if '/devtools/browser/' in ws_endpoint:
            return 'cdp'

        return 'cdp'

    def _is_page_valid(self) -> bool:
        """
        检查页面是否仍然有效

        :return: 页面是否有效
        """
        try:
            if not self.page:
                return False
            # ✅ evaluate() 不支持 timeout 参数，使用默认超时
            self.page.evaluate("() => true")
            return True
        except Exception:
            return False

    def _init_driver(self) -> None:
        """初始化浏览器驱动"""
        try:
            self.playwright = sync_playwright().start()

            if self.browser_ws_endpoint:
                # ========== 远程浏览器 ==========
                ws_url = self._build_ws_url_with_token(
                    self.browser_ws_endpoint,
                    self.browser_token
                )

                connection_type = self.browser_connection_type
                if connection_type == 'auto':
                    connection_type = self._detect_connection_type(self.browser_ws_endpoint)
                    print(f"🔍 自动检测连接类型: {connection_type}")

                print(f"🔗 正在连接到远程浏览器...")
                print(f"   端点: {self.browser_ws_endpoint}")
                print(f"   连接方式: {connection_type}")

                browser_launcher = getattr(self.playwright, self.browser_type)

                if connection_type == 'cdp':
                    try:
                        self.browser = browser_launcher.connect_over_cdp(ws_url)
                        print(f"✅ 已通过 CDP 连接到远程浏览器")
                    except Exception as e:
                        print(f"⚠️ CDP 连接失败: {e}")
                        print(f"🔄 尝试使用 Playwright 协议连接...")
                        self.browser = browser_launcher.connect(ws_url)
                        print(f"✅ 已通过 Playwright 协议连接到远程浏览器")

                elif connection_type == 'playwright':
                    self.browser = browser_launcher.connect(ws_url)
                    print(f"✅ 已通过 Playwright 协议连接到远程浏览器")

                else:
                    raise ValueError(f"不支持的连接类型: {connection_type}")

                # ✅ 远程浏览器的上下文和页面处理
                context = None

                # 检查是否有现有上下文
                if self.browser.contexts:
                    existing_context = self.browser.contexts[0]

                    # 如果设置了代理，必须创建新上下文（因为无法修改现有上下文的代理）
                    if self.proxy:
                        print(f"   检测到代理配置，需要创建新的浏览器上下文")
                        context = None  # 强制创建新上下文
                    else:
                        # 没有代理要求，可以使用现有上下文
                        context = existing_context
                        print(f"   使用现有浏览器上下文")

                # 创建新上下文（如果需要）
                if not context:
                    context_options = {
                        'viewport': {'width': 1920, 'height': 1080},
                        'permissions': ['clipboard-read', 'clipboard-write']
                    }

                    if self.proxy:
                        context_options['proxy'] = self.proxy
                        print(f"   ✅ 应用代理配置: {self.proxy.get('server', 'N/A')}")

                    context = self.browser.new_context(**context_options)
                    print(f"   创建新浏览器上下文")

                # 获取或创建页面
                if context.pages:
                    self.page = context.pages[0]
                    print(f"   使用现有页面（共 {len(context.pages)} 个页面）")
                else:
                    self.page = context.new_page()
                    print(f"   创建新页面")

            else:
                # ========== 本地浏览器 ==========
                browser_launcher = getattr(self.playwright, self.browser_type)

                # ✅ 本地浏览器：代理可以在 launch 时设置（全局）
                launch_args = {
                    'headless': self.headless,
                    'args': [
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu'
                    ]
                }

                # 方式1：在 launch 时设置代理（全局代理，推荐）
                if self.proxy:
                    launch_args['proxy'] = self.proxy
                    print(f"   ✅ 应用全局代理: {self.proxy.get('server', 'N/A')}")

                self.browser = browser_launcher.launch(**launch_args)

                # 创建上下文
                context_options = {
                    'viewport': {'width': 1920, 'height': 1080},
                    'permissions': ['clipboard-read', 'clipboard-write']
                }

                # 方式2：也可以在 context 时再次设置或覆盖代理
                # 如果 launch 时已设置代理，这里可以省略
                # if self.proxy:
                #     context_options['proxy'] = self.proxy

                context = self.browser.new_context(**context_options)
                self.page = context.new_page()

                print(f"✅ 本地浏览器驱动初始化成功（{self.browser_type}）")

            self.page.set_default_timeout(self.wait_timeout)

        except Exception as e:
            error_msg = f"浏览器驱动初始化失败: {str(e)}"
            print(f"❌ {error_msg}")

            if self.browser_ws_endpoint:
                print("💡 远程浏览器连接失败，请检查：")
                print("   1. 远程浏览器服务是否正在运行")
                print("   2. WebSocket 端点是否正确")
                print("   3. Token 是否有效（如果需要）")
                print("   4. 网络连接和防火墙设置")
                if self.proxy:
                    print("   5. 代理服务器是否可访问")
                print(f"\n🔧 测试连接：")

                test_url = self.browser_ws_endpoint.replace('ws://', 'http://').replace('wss://', 'https://')
                if '?' in test_url:
                    test_url = test_url.split('?')[0]
                print(f"   curl {test_url}")

                print(f"\n📚 支持的部署方式：")
                print(f"   - browserless: docker run -p 3000:3000 ghcr.io/browserless/chromium")
                print(f"   - Playwright: docker run -p 3001:3000 mcr.microsoft.com/playwright:latest")
            else:
                print("💡 提示：")
                print("   1. 确保已安装 Playwright: pip install playwright")
                print("   2. 首次使用需安装浏览器: playwright install chromium")
                if self.proxy:
                    print("   3. 检查代理服务器配置是否正确")

            self._notify_error(
                error_msg, {'stage': '初始化浏览器', 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _close_driver(self) -> None:
        """关闭浏览器驱动"""
        try:
            if self.page:
                self.page.close()
                self.page = None
            if self.browser:
                self.browser.close()
                self.browser = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️ 关闭浏览器时出错: {e}")

    def _load_page(self) -> None:
        """加载网页（支持多URL自动切换）"""
        last_error = None

        for url_index, url in enumerate(self.url_list):
            try:
                self.current_url = url
                self.current_url_index = url_index

                if url_index > 0:
                    url_type = "备用" if url == self.backup_url else (
                        "默认" if url == self.default_url else "其他")
                    print(f"🔄 切换到{url_type}地址...")

                print(f"🌐 正在打开网页 [{url_index + 1}/{len(self.url_list)}]: {self.current_url}")

                # 🔧 去掉页面有效性检查，直接加载（goto 会自动处理）
                self.page.goto(self.current_url, wait_until='domcontentloaded')
                self.page.wait_for_selector('.CodeMirror', timeout=self.wait_timeout)
                time.sleep(3)

                print(f"✅ 网页加载成功")
                return

            except Exception as e:
                last_error = e
                error_msg = f"网页加载失败 ({url}): {str(e)}"
                print(f"❌ {error_msg}")

                if url_index < len(self.url_list) - 1:
                    print(f"⏳ 将在2秒后尝试下一个地址...")
                    time.sleep(2)
                else:
                    final_error_msg = f"所有地址均无法访问（共尝试 {len(self.url_list)} 个）"
                    print(f"💔 {final_error_msg}")
                    self._notify_error(
                        final_error_msg,
                        {
                            'stage': '加载网页',
                            'tried_urls': self.url_list,
                            'last_error': str(last_error),
                            'error_type': type(last_error).__name__
                        }
                    )
                    raise ConversionError(
                        f"{final_error_msg}，最后错误: {str(last_error)}") from last_error

    def _inject_copy_interceptor(self) -> None:
        """注入JavaScript代码来拦截复制事件"""
        try:
            # 给页面一点时间完成加载和JS初始化
            time.sleep(1)

            # 先授予剪贴板权限（如果是远程浏览器）
            if self.browser_ws_endpoint:
                self._grant_clipboard_permissions()

            js_code = """
            window._capturedHTML = null;
            window._copyInterceptorReady = false;

            document.addEventListener('copy', function(e) {
                console.log('复制事件已触发');
                if (e.clipboardData) {
                    var htmlData = e.clipboardData.getData('text/html');
                    if (htmlData) {
                        window._capturedHTML = htmlData;
                        console.log('已捕获HTML，长度:', htmlData.length);
                    }
                }
            }, true);

            window._copyInterceptorReady = true;
            console.log('复制拦截器已安装');
            """

            self.page.evaluate(js_code)
            print("✅ 已注入复制拦截器")

        except Exception as e:
            error_msg = f"注入拦截器失败: {str(e)}"
            print(f"❌ {error_msg}")
            # 注入失败不抛出异常，因为我们有其他获取方案
            print(f"⚠️ 将使用备用方案获取HTML")

    def _select_theme(self, theme: str) -> None:
        """
        选择主题

        :param theme: 主题名称
        """
        try:
            # 检查页面有效性
            if not self._is_page_valid():
                raise ConversionError("页面已失效，无法选择主题")

            theme_button = self.page.locator('#nice-menu-theme')
            theme_button.wait_for(state='visible', timeout=self.wait_timeout)
            theme_button.click()
            time.sleep(0.5)

            theme_id = f'#nice-menu-theme-{theme}'
            theme_item = self.page.locator(theme_id)
            theme_item.wait_for(state='visible', timeout=self.wait_timeout)
            theme_item.click()

            print(f"🎨 已选择主题: {self.THEME_NAMES.get(theme, theme)}")
            time.sleep(1.5)
        except Exception as e:
            error_msg = f"选择主题失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '选择主题', 'theme': theme, 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _select_code_theme(self, code_theme: str) -> None:
        """
        选择代码主题

        :param code_theme: 代码主题名称
        """
        try:
            # 检查页面有效性
            if not self._is_page_valid():
                raise ConversionError("页面已失效，无法选择代码主题")

            if code_theme not in self.AVAILABLE_CODE_THEMES:
                print(f"⚠️ 跳过无效的代码主题: {code_theme}")
                return

            code_theme_button = self.page.locator('#nice-menu-codetheme')
            code_theme_button.wait_for(state='visible', timeout=self.wait_timeout)
            code_theme_button.click()
            time.sleep(0.5)

            theme_config = self.CODE_THEME_CONFIG[code_theme]
            theme_id = f'#{theme_config["id"]}'
            theme_item = self.page.locator(theme_id)
            theme_item.wait_for(state='visible', timeout=self.wait_timeout)
            theme_item.click()

            print(f"💻 已选择代码主题: {theme_config['name']}")

            self.page.evaluate("() => document.body.click()")
            time.sleep(0.5)

        except Exception as e:
            error_msg = f"选择代码主题失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '选择代码主题', 'code_theme': code_theme, 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _set_mac_style(self, enable: bool) -> None:
        """
        设置 Mac 风格

        :param enable: 是否启用 Mac 风格
        """
        try:
            code_theme_button = self.page.locator('#nice-menu-codetheme')
            code_theme_button.wait_for(state='visible', timeout=self.wait_timeout)
            code_theme_button.click()
            time.sleep(0.5)

            mac_style_button = self.page.locator('#nice-menu-codetheme-apple')
            mac_style_button.wait_for(state='visible', timeout=self.wait_timeout)

            # ✅ 更健壮的选中状态判断
            is_selected = self.page.evaluate("""
                () => {
                    const macItem = document.querySelector('#nice-menu-codetheme-apple');
                    if (!macItem) return false;

                    // 方法1：检查 flag 内是否有 ✔️
                    const flagElement = macItem.querySelector('.nice-codetheme-item-flag');
                    if (flagElement) {
                        const hasCheckmark = flagElement.innerHTML.trim().length > 0;
                        if (hasCheckmark) return true;
                    }

                    // 方法2：检查是否有 'selected' 或 'active' 类名
                    if (macItem.classList.contains('selected') || 
                        macItem.classList.contains('active') ||
                        macItem.classList.contains('checked')) {
                        return true;
                    }

                    // 方法3：检查 aria-checked 属性
                    if (macItem.getAttribute('aria-checked') === 'true') {
                        return true;
                    }

                    return false;
                }
            """)

            # 只有当期望状态与当前状态不一致时才点击
            should_click = (enable and not is_selected) or (not enable and is_selected)

            if should_click:
                mac_style_button.click()
                action = '启用' if enable else '禁用'
                print(f"🍎 已{action} Mac 风格（从 {'选中' if is_selected else '未选中'} 切换）")
                time.sleep(0.3)  # 给一点时间让动画完成
            else:
                status = '已启用' if enable else '已禁用'
                print(f"🍎 Mac 风格{status}（当前状态: {'选中' if is_selected else '未选中'}，无需切换）")

            # 点击其他地方关闭菜单
            self.page.evaluate("() => document.body.click()")
            time.sleep(0.5)

        except Exception as e:
            error_msg = f"设置 Mac 风格失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '设置Mac风格', 'enable': enable, 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _notify_error(self, error_msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        发送错误通知

        :param error_msg: 错误消息
        :param context: 错误上下文信息
        """
        if self.on_error:
            try:
                self.on_error(error_msg, context or {})
            except Exception as e:
                print(f"⚠️ 错误通知回调执行失败: {e}")

    def _retry_on_error(self, func: Callable, *args, **kwargs) -> Any:
        """
        带重试机制的函数执行器

        :param func: 要执行的函数
        :return: 函数执行结果
        """
        last_error = None
        for attempt in range(self.retry_count + 1):
            try:
                if attempt > 0:
                    print(f"🔄 正在进行第 {attempt}/{self.retry_count} 次重试...")
                    time.sleep(2)
                result = func(*args, **kwargs)
                if attempt > 0:
                    print(f"✅ 重试成功！")
                return result
            except Exception as e:
                last_error = e
                if attempt < self.retry_count:
                    print(f"❌ 执行失败（第{attempt + 1}次尝试）: {str(e)}")
                    print(f"⏳ 将在2秒后重试...")
        raise last_error

    def _is_remote_url(self, path: str) -> bool:
        """
        判断路径是否为网络URL

        :param path: 路径字符串
        :return: 是否为网络URL
        """
        parsed = urlparse(path)
        return parsed.scheme in ('http', 'https', 'ftp')

    def _is_data_url(self, path: str) -> bool:
        """
        判断是否为Data URL（base64编码的图片）

        :param path: 路径字符串
        :return: 是否为Data URL
        """
        return path.startswith('data:image/')

    def _should_upload_image(self, image_path: str, is_remote: bool) -> bool:
        """
        根据上传模式判断是否应该上传该图片

        :param image_path: 图片路径
        :param is_remote: 是否为远程URL
        :return: 是否应该上传
        """
        if not self.image_uploader:
            return False

        if self._is_data_url(image_path):
            return self.image_upload_mode == 'all'

        if self.image_upload_mode == 'all':
            return True
        elif self.image_upload_mode == 'local':
            return not is_remote
        elif self.image_upload_mode == 'remote':
            return is_remote

        return False

    def _process_images_in_markdown(self, markdown_content: str, base_path: Optional[Path] = None) -> str:
        """
        处理Markdown中的图片，根据模式上传到图床

        :param markdown_content: Markdown内容
        :param base_path: Markdown文件所在目录，用于解析相对路径
        :return: 处理后的Markdown内容
        """
        if not self.image_uploader:
            return markdown_content

        mode_names = {
            'local': '仅本地图片',
            'remote': '仅网络图片',
            'all': '所有图片'
        }
        print(f"🖼️ 开始处理Markdown中的图片 [模式: {mode_names[self.image_upload_mode]}]")

        pattern = r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'

        uploaded_count = 0
        skipped_count = 0
        failed_count = 0

        def replace_image(match: re.Match) -> str:
            nonlocal uploaded_count, skipped_count, failed_count

            alt_text = match.group(1)
            image_path = match.group(2)
            title_text = match.group(3) if match.group(3) else None

            is_remote = self._is_remote_url(image_path)
            is_data = self._is_data_url(image_path)

            if not self._should_upload_image(image_path, is_remote):
                skipped_count += 1
                if is_remote:
                    print(f"  ⏭️ 跳过网络图片 [模式不匹配]: {image_path[:60]}...")
                elif is_data:
                    print(f"  ⏭️ 跳过Data URL图片 [模式不匹配]")
                else:
                    print(f"  ⏭️ 跳过本地图片 [模式不匹配]: {Path(image_path).name}")
                return match.group(0)

            try:
                upload_target = image_path

                if not is_remote and not is_data:
                    if base_path and not os.path.isabs(image_path):
                        full_path = base_path / image_path
                    else:
                        full_path = Path(image_path)

                    full_path = full_path.resolve()

                    if not full_path.exists():
                        print(f"  ⚠️ 图片文件不存在，保持原样: {image_path}")
                        skipped_count += 1
                        return match.group(0)

                    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
                    if full_path.suffix.lower() not in valid_extensions:
                        print(f"  ⚠️ 非图片文件，跳过: {full_path.name}")
                        skipped_count += 1
                        return match.group(0)

                    upload_target = str(full_path)
                    print(f"  📤 正在上传本地图片: {full_path.name}")
                elif is_data:
                    print(f"  📤 正在上传Data URL图片")
                else:
                    print(f"  📤 正在上传网络图片: {image_path[:60]}...")

                uploaded_url = self.image_uploader(upload_target)

                if not uploaded_url:
                    raise ValueError("上传函数返回空URL")

                print(f"  ✅ 图片已上传: {uploaded_url}")
                uploaded_count += 1

                if title_text:
                    return f'![{alt_text}]({uploaded_url} "{title_text}")'
                else:
                    return f'![{alt_text}]({uploaded_url})'

            except Exception as e:
                print(f"  ❌ 图片上传失败: {str(e)}")
                failed_count += 1
                return match.group(0)

        result = re.sub(pattern, replace_image, markdown_content)

        total = uploaded_count + skipped_count + failed_count
        if total > 0:
            print(f"🖼️ 图片处理完成: 共 {total} 张 (上传 {uploaded_count}, 跳过 {skipped_count}, 失败 {failed_count})")
        else:
            print(f"🖼️ 未检测到图片")

        return result

    def _input_markdown(self, markdown_content: str) -> None:
        """
        输入Markdown内容并触发转换

        :param markdown_content: Markdown文本内容
        """
        try:
            # 检查页面有效性
            if not self._is_page_valid():
                raise ConversionError("页面已失效，无法输入 Markdown")

            print(f"📝 正在输入Markdown内容（{len(markdown_content)} 字符）...")

            js_code = """
            (content) => {
                var editor = document.querySelector('.CodeMirror').CodeMirror;

                if (!editor) {
                    throw new Error('找不到CodeMirror编辑器');
                }

                editor.setValue(content);
                editor.refresh();

                var changeEvent = new Event('change', { bubbles: true });
                var inputEvent = new Event('input', { bubbles: true });

                editor.getTextArea().dispatchEvent(changeEvent);
                editor.getTextArea().dispatchEvent(inputEvent);

                setTimeout(function() {
                    editor.focus();
                    editor.execCommand('selectAll');
                    editor.replaceSelection(content);
                }, 100);

                return true;
            }
            """

            self.page.evaluate(js_code, markdown_content)
            time.sleep(1)

            current_content = self.page.evaluate("""
                () => {
                    var editor = document.querySelector('.CodeMirror').CodeMirror;
                    return editor ? editor.getValue() : null;
                }
            """)

            if current_content is None:
                raise ConversionError("无法获取编辑器内容，编辑器可能未正确初始化")

            if current_content == markdown_content:
                print(f"✅ Markdown内容已设置")
            else:
                print(f"⚠️ 警告：设置的内容可能不完整")

            print("⏳ 等待内容转换...")
            if not self._wait_for_preview_update():
                print("⚠️ 警告：预览内容可能未完全更新，但继续尝试...")
            else:
                print(f"✅ 内容转换完成")

        except Exception as e:
            error_msg = f"输入Markdown失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(error_msg, {
                'stage': '输入Markdown',
                'content_length': len(markdown_content),
                'error_type': type(e).__name__
            })
            raise ConversionError(error_msg) from e

    def _wait_for_preview_update(self, timeout: int = 10) -> bool:
        """
        等待预览区域更新

        :param timeout: 超时时间（秒）
        :return: 是否成功更新
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 检查页面有效性
                if not self._is_page_valid():
                    return False

                preview_content = self.page.evaluate("""
                    () => {
                        var editor = document.querySelector('#nice-rich-text-editor');
                        if (editor && editor.innerHTML) {
                            var content = editor.innerHTML.trim();
                            return content.length > 100;
                        }
                        return false;
                    }
                """)

                if preview_content:
                    print("✅ 检测到预览内容已更新")
                    time.sleep(1)
                    return True
            except Exception:
                pass

            time.sleep(0.5)

        return False

    def _clear_editor(self) -> None:
        """清空编辑器内容"""
        try:
            # 检查页面有效性
            if not self._is_page_valid():
                print(f"⚠️ 页面无效，跳过清空编辑器")
                return

            js_clear = """
            () => {
                var editor = document.querySelector('.CodeMirror').CodeMirror;
                editor.setValue('');
                editor.refresh();
            }
            """
            self.page.evaluate(js_clear)
            time.sleep(0.5)
            print("✅ 已清空编辑器")
        except Exception as e:
            print(f"⚠️ 清空编辑器失败: {e}")

    def _grant_clipboard_permissions(self) -> None:
        """
        使用 CDP 授予剪贴板权限
        """
        try:
            # 获取 CDP Session
            cdp = self.page.context.new_cdp_session(self.page)

            # 授予剪贴板权限
            cdp.send('Browser.grantPermissions', {
                'permissions': ['clipboardReadWrite', 'clipboardSanitizedWrite'],
                'origin': self.current_url
            })

            print("✅ 已授予剪贴板权限 (CDP)")

        except Exception as e:
            print(f"⚠️ CDP 授予剪贴板权限失败: {e}，将使用备用方案")

    def _get_html_via_cdp(self, button_id: str) -> Optional[str]:
        """
        使用 CDP 获取剪贴板中的 HTML 内容

        :param button_id: 复制按钮的 ID
        :return: 剪贴板中的 HTML 内容
        """
        try:
            print("🔄 尝试使用 CDP 获取剪贴板内容...")

            # 获取 CDP Session
            cdp = self.page.context.new_cdp_session(self.page)

            # 先点击复制按钮
            copy_button = self.page.locator(f'#{button_id}')
            copy_button.click()
            time.sleep(1)

            # 使用 CDP 的 Runtime.evaluate 执行 JavaScript
            # 这种方式更稳定，不会因为页面状态而失败
            result = cdp.send('Runtime.evaluate', {
                'expression': '''
                (async () => {
                    try {
                        const clipboardItems = await navigator.clipboard.read();
                        for (const item of clipboardItems) {
                            if (item.types.includes('text/html')) {
                                const blob = await item.getType('text/html');
                                const text = await blob.text();
                                return text;
                            }
                        }
                        return null;
                    } catch (err) {
                        return 'ERROR: ' + err.message;
                    }
                })()
                ''',
                'awaitPromise': True,
                'returnByValue': True
            })

            if 'result' in result and 'value' in result['result']:
                html_content = result['result']['value']
                if html_content and not html_content.startswith('ERROR:'):
                    print(f"✅ 通过 CDP 成功获取内容（{len(html_content)} 字符）")
                    return html_content
                else:
                    print(f"⚠️ CDP 返回错误: {html_content}")

            return None

        except Exception as e:
            print(f"❌ CDP 方法失败: {e}")
            return None

    def _get_html_via_dom_direct(self) -> Optional[str]:
        """
        直接从 DOM 获取 HTML（最稳定的降级方案）

        :return: 预览区域的 HTML 内容
        """
        try:
            print("🔄 使用 DOM 直接获取方案...")

            # 使用 CDP 的 Runtime.evaluate，即使页面状态异常也能工作
            cdp = self.page.context.new_cdp_session(self.page)

            result = cdp.send('Runtime.evaluate', {
                'expression': '''
                (() => {
                    const editor = document.querySelector('#nice-rich-text-editor');
                    return editor ? editor.innerHTML : null;
                })()
                ''',
                'returnByValue': True
            })

            if 'result' in result and 'value' in result['result']:
                html_content = result['result']['value']
                if html_content:
                    print(f"✅ 通过 DOM 直接获取成功（{len(html_content)} 字符）")
                    return html_content

            return None

        except Exception as e:
            print(f"❌ DOM 直接获取失败: {e}")
            return None

    def _get_converted_html(self, platform: Platform = 'wechat') -> str:
        """
        获取转换后的HTML内容（带样式）

        :param platform: 目标平台
        :return: 转换后的带样式HTML字符串
        """
        try:
            if platform not in self.PLATFORM_CONFIG:
                raise ValueError(f"不支持的平台: {platform}")

            platform_info = self.PLATFORM_CONFIG[platform]
            button_id = platform_info['button_id']
            platform_name = platform_info['name']

            print(f"📋 准备获取 {platform_name} 格式HTML...")

            # 检查预览区域
            try:
                preview_check = self.page.evaluate("""
                    () => {
                        var editor = document.querySelector('#nice-rich-text-editor');
                        if (editor) {
                            return {
                                hasContent: editor.innerHTML.trim().length > 0,
                                contentLength: editor.innerHTML.trim().length
                            };
                        }
                        return null;
                    }
                """)

                if preview_check:
                    print(
                        f"📊 预览区域状态: 长度={preview_check['contentLength']}, 有内容={preview_check['hasContent']}")
                    if not preview_check['hasContent']:
                        print("⚠️ 警告：预览区域为空！")
            except Exception as e:
                print(f"⚠️ 检查预览区域失败: {e}")

            # 清空之前捕获的内容
            try:
                self.page.evaluate("() => { window._capturedHTML = null; }")
            except:
                pass

            # 确认复制按钮存在
            try:
                copy_button = self.page.locator(f'#{button_id}')
                copy_button.wait_for(state='visible', timeout=self.wait_timeout)
                print(f"✅ 找到 {platform_name} 复制按钮")
            except PlaywrightTimeoutError:
                raise ConversionError(f"找不到 {platform_name} 复制按钮（ID: {button_id}）")

            html_content = None

            # 方案1：尝试使用传统的拦截方法
            try:
                print(f"📋 方案1: 尝试使用拦截器获取...")
                copy_button.click()
                time.sleep(1.5)
                html_content = self.page.evaluate("() => window._capturedHTML")
                if html_content:
                    print(f"✅ 拦截器方案成功（{len(html_content)} 字符）")
            except Exception as e:
                print(f"⚠️ 拦截器方案失败: {e}")

            # 方案2：使用 CDP 获取剪贴板
            if not html_content:
                html_content = self._get_html_via_cdp(button_id)

            # 方案3：使用传统剪贴板 API
            if not html_content:
                try:
                    print("📋 方案3: 尝试使用传统剪贴板 API...")
                    html_content = self._get_html_via_clipboard(button_id)
                except Exception as e:
                    print(f"⚠️ 传统剪贴板 API 失败: {e}")

            # 方案4：直接从 DOM 获取（使用 CDP）
            if not html_content:
                html_content = self._get_html_via_dom_direct()

            # 方案5：最后的降级方案（使用普通 evaluate）
            if not html_content:
                try:
                    print("📋 方案5: 最后降级方案（DOM 获取）...")
                    html_content = self.page.evaluate("""
                        () => {
                            var editor = document.querySelector('#nice-rich-text-editor');
                            return editor ? editor.innerHTML : '';
                        }
                    """)
                    if html_content:
                        print(f"✅ 降级方案成功（{len(html_content)} 字符）")
                except Exception as e:
                    print(f"⚠️ 降级方案也失败: {e}")

            # 验证内容
            if not html_content or len(html_content) < 50:
                raise ConversionError(
                    f"获取的HTML内容为空或过短（长度: {len(html_content) if html_content else 0}）")

            print(f"✅ 已获取 {platform_name} 格式HTML（{len(html_content)} 字符）")

            # 检查样式
            has_inline_style = 'style=' in html_content
            has_style_tag = '<style>' in html_content

            if has_inline_style or has_style_tag:
                print(f"✅ HTML包含样式信息（内联样式:{has_inline_style}, 样式标签:{has_style_tag}）")
            else:
                print("⚠️ 警告：HTML可能不包含样式信息")

            # 清理HTML
            html_content = self._clean_html(html_content)

            return html_content

        except Exception as e:
            error_msg = f"获取HTML失败: {str(e)}"
            print(f"❌ {error_msg}")

            self._notify_error(error_msg, {
                'stage': '获取HTML',
                'platform': platform,
                'error_type': type(e).__name__
            })
            raise ConversionError(error_msg) from e

    def _get_html_via_clipboard(self, button_id: str) -> Optional[str]:
        """
        通过剪贴板API获取HTML内容

        :param button_id: 复制按钮的ID
        :return: 剪贴板中的HTML内容
        """
        try:
            js_read_clipboard = f"""
            async () => {{
                try {{
                    document.querySelector('#{button_id}').click();
                    await new Promise(r => setTimeout(r, 800));

                    const clipboardItems = await navigator.clipboard.read();
                    for (const item of clipboardItems) {{
                        if (item.types.includes('text/html')) {{
                            const blob = await item.getType('text/html');
                            const text = await blob.text();
                            return text;
                        }}
                    }}
                    return null;
                }} catch (err) {{
                    console.error('读取剪贴板失败:', err);
                    return null;
                }}
            }}
            """

            html_content = self.page.evaluate(js_read_clipboard)
            if html_content:
                print("✅ 通过剪贴板API成功获取内容")
            return html_content
        except Exception as e:
            print(f"❌ 剪贴板API方法失败: {e}")
            return None

    def _read_markdown_file(self, file_path: Union[str, Path]) -> str:
        """
        读取Markdown文件

        :param file_path: 文件路径
        :return: 文件内容
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            error_msg = f"读取文件失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '读取文件', 'file_path': str(file_path)})
            raise

    def _wrap_full_html(self, html_content: str, title: str = "文章", platform: Platform = 'wechat') -> str:
        """
        包装为完整HTML文档

        :param html_content: HTML内容片段
        :param title: 文档标题
        :param platform: 目标平台
        :return: 完整的HTML文档
        """
        platform_name = self.PLATFORM_CONFIG[platform]['name']
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title} - {platform_name}</title>
    <link rel="icon" href="https://s2.loli.net/2025/07/27/ZmzSQsgpKOM2xBk.png" type="image/png">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .platform-badge {{
            display: inline-block;
            padding: 4px 12px;
            margin-bottom: 20px;
            background-color: #e8f4fd;
            color: #1890ff;
            border-radius: 4px;
            font-size: 14px;
        }}
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 20px; }}
        }}
        @media print {{
            body {{ background-color: white; }}
            .container {{ box-shadow: none; padding: 0; }}
            .platform-badge {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="platform-badge">📝 {platform_name}格式</div>
{html_content}
    </div>
</body>
</html>"""

    def _save_html(self,
                   html_content: str,
                   output_path: Union[str, Path],
                   original_name: Optional[str] = None,
                   wrap_full_html: bool = False,
                   platform: Platform = 'wechat') -> Path:
        """
        保存HTML文件

        :param html_content: HTML内容
        :param output_path: 输出路径
        :param original_name: 原始文件名
        :param wrap_full_html: 是否包装为完整HTML
        :param platform: 目标平台
        :return: 保存的文件路径
        """
        try:
            output_path = Path(output_path)
            platform_suffix = self.PLATFORM_CONFIG[platform]['suffix']

            if output_path.is_dir() or not output_path.suffix:
                output_path.mkdir(parents=True, exist_ok=True)
                if original_name:
                    filename = Path(original_name).stem + f'_{platform_suffix}.html'
                else:
                    filename = f'article_{platform_suffix}_{int(time.time())}.html'
                output_path = output_path / filename
            else:
                output_path.parent.mkdir(parents=True, exist_ok=True)

            title = Path(original_name).stem if original_name else "文章"
            final_html = self._wrap_full_html(
                html_content, title, platform) if wrap_full_html else html_content

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)

            print(f"💾 已保存HTML文件: {output_path}")
            return output_path
        except Exception as e:
            error_msg = f"保存文件失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '保存文件', 'output_path': str(output_path)})
            raise

    def _parse_theme(self, theme: Union[str, List[str], None]) -> str:
        """
        解析主题选项

        :param theme: 主题选项
        :return: 选中的主题名
        """
        if theme is None or theme == 'random':
            selected = random.choice(self.AVAILABLE_THEMES)
            print(f"🎲 随机选择主题: {self.THEME_NAMES[selected]}")
        elif isinstance(theme, list):
            valid = [t for t in theme if t in self.AVAILABLE_THEMES]
            if not valid:
                raise ValueError("主题列表中没有有效主题")
            selected = random.choice(valid)
            print(f"🎲 从列表随机选择: {self.THEME_NAMES[selected]}")
        else:
            if theme not in self.AVAILABLE_THEMES:
                raise ValueError(f"无效主题: {theme}")
            selected = theme
        return selected

    def convert(self,
                markdown: Union[str, Path, List[Union[str, Path]]],
                theme: Union[str, List[str], None] = 'normal',
                output_dir: Optional[Union[str, Path]] = None,
                return_html: bool = True,
                wrap_full_html: bool = False,
                platform: Platform = 'wechat',
                code_theme: Optional[CodeTheme] = None,
                mac_style: Optional[bool] = None) -> Union[str, List[str], Path, List[Path]]:
        """
        转换Markdown到指定平台格式

        :param markdown: Markdown内容或文件路径
        :param theme: 主题选择
        :param output_dir: 输出目录
        :param return_html: 是否返回HTML内容
        :param wrap_full_html: 是否包装为完整HTML
        :param platform: 目标平台（wechat/zhihu/juejin）
        :param code_theme: 代码主题（可选，覆盖初始化时的设置）
        :param mac_style: Mac 风格（可选，覆盖初始化时的设置）
        :return: HTML内容或文件路径
        """
        try:
            if platform not in self.PLATFORM_CONFIG:
                raise ValueError(f"不支持的平台: {platform}")

            final_code_theme = code_theme if code_theme is not None else self.code_theme
            final_mac_style = mac_style if mac_style is not None else self.mac_style

            print(f"\n🎯 目标平台: {self.PLATFORM_CONFIG[platform]['name']}")

            self._retry_on_error(self._init_driver)
            self._retry_on_error(self._load_page)
            self._inject_copy_interceptor()

            is_multiple = isinstance(markdown, list)
            markdown_list = markdown if is_multiple else [markdown]

            results = []
            failed_items = []

            for idx, md_item in enumerate(markdown_list, 1):
                print(f"\n{'=' * 70}")
                print(f"📌 处理第 {idx}/{len(markdown_list)} 项")
                print(f"{'=' * 70}")

                try:
                    is_file = isinstance(md_item, Path) or (
                            isinstance(md_item, str) and
                            (md_item.endswith('.md') or md_item.endswith('.markdown')) and
                            os.path.exists(md_item)
                    )

                    if is_file:
                        file_path = Path(md_item)
                        md_content = self._read_markdown_file(file_path)
                        original_name = file_path.name
                        print(f"📄 读取文件: {md_item}（{len(md_content)} 字符）")

                        md_content = self._process_images_in_markdown(
                            md_content,
                            base_path=file_path.parent
                        )
                    else:
                        md_content = md_item
                        original_name = None
                        print(f"📝 使用Markdown内容（{len(md_content)} 字符）")

                        md_content = self._process_images_in_markdown(md_content)

                    if idx > 1:
                        self._clear_editor()

                    selected_theme = self._parse_theme(theme)
                    self._select_theme(selected_theme)

                    self._select_code_theme(final_code_theme)

                    self._set_mac_style(final_mac_style)

                    self._input_markdown(md_content)

                    html_content = self._retry_on_error(
                        self._get_converted_html, platform)

                    if output_dir:
                        file_path = self._save_html(
                            html_content, output_dir, original_name, wrap_full_html, platform)
                        results.append(file_path if not return_html else html_content)
                    else:
                        results.append(html_content)

                    if idx < len(markdown_list):
                        self._inject_copy_interceptor()
                        time.sleep(1)

                except Exception as e:
                    error_msg = f"处理第 {idx} 项失败: {str(e)}"
                    print(f"❌ {error_msg}")
                    failed_items.append({'index': idx, 'error': str(e)})
                    self._notify_error(
                        error_msg, {'stage': '转换单项', 'index': idx, 'platform': platform})

                    if len(markdown_list) == 1:
                        raise
                    else:
                        print(f"⚠️ 跳过该项，继续处理...")

            print(f"\n{'=' * 70}")
            if failed_items:
                print(f"⚠️ 部分完成！成功 {len(results)}/{len(markdown_list)} 项")
                for item in failed_items:
                    print(f"  ❌ 失败项 {item['index']}: {item['error']}")
            else:
                print(f"🎉 全部完成！共 {len(results)} 项")
            print(f"{'=' * 70}\n")

            if not results:
                raise ConversionError("所有项目均转换失败")

            return results if is_multiple else results[0]

        except Exception as e:
            error_msg = f"转换出错: {str(e)}"
            print(f"\n❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '总体流程', 'platform': platform})
            raise
        finally:
            self._close_driver()


# ============================================================================
# 便捷函数
# ============================================================================

def convert(
        markdown: Union[str, Path, List[Union[str, Path]]],
        platform: Platform = 'wechat',
        theme: Union[str, List[str], None] = 'normal',
        output_dir: Optional[Union[str, Path]] = None,
        return_html: bool = True,
        headless: bool = True,
        wrap_full_html: bool = False,
        wait_timeout: int = 30,
        retry_count: int = 1,
        on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        editor_url: Optional[Union[str, List[str]]] = None,
        image_uploader: Optional[Callable[[str], str]] = None,
        image_upload_mode: ImageUploadMode = 'local',
        code_theme: CodeTheme = 'atom-one-dark',
        mac_style: bool = True,
        browser_ws_endpoint: Optional[str] = None,
        browser_type: BrowserType = 'chromium',
        browser_connection_type: BrowserConnectionType = 'auto',
        browser_token: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None
) -> Union[str, List[str], Path, List[Path]]:
    """
    通用转换函数：转换Markdown到指定平台格式

    :param markdown: Markdown内容或文件路径（支持单个或列表）
    :param platform: 目标平台（wechat/zhihu/juejin）
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录（None则不保存）
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式（远程浏览器时忽略）
    :param wrap_full_html: 是否包装为完整HTML文档
    :param wait_timeout: 等待超时时间（秒）
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址（字符串或列表）
    :param image_uploader: 图片上传回调函数
    :param image_upload_mode: 图片上传模式（local/remote/all）
    :param code_theme: 代码主题
    :param mac_style: 是否启用 Mac 风格
    :param browser_ws_endpoint: 远程浏览器 WebSocket 端点
    :param browser_type: 浏览器类型（chromium/firefox/webkit）
    :param browser_connection_type: 连接类型（auto/cdp/playwright）
    :param browser_token: 远程浏览器访问令牌
    :param proxy: 代理配置，例如 {'server': 'http://proxy.com:8080'}
    :return: HTML内容字符串、文件路径或它们的列表
    """
    converter = MarkdownConverter(
        headless=headless,
        wait_timeout=wait_timeout,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode,
        code_theme=code_theme,
        mac_style=mac_style,
        browser_ws_endpoint=browser_ws_endpoint,
        browser_type=browser_type,
        browser_connection_type=browser_connection_type,
        browser_token=browser_token,
        proxy=proxy
    )
    return converter.convert(
        markdown=markdown,
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        wrap_full_html=wrap_full_html,
        platform=platform
    )


def to_wechat(
        markdown: Union[str, Path, List[Union[str, Path]]],
        theme: Union[str, List[str], None] = 'normal',
        output_dir: Optional[Union[str, Path]] = None,
        return_html: bool = True,
        headless: bool = True,
        wrap_full_html: bool = False,
        wait_timeout: int = 30,
        retry_count: int = 1,
        on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        editor_url: Optional[Union[str, List[str]]] = None,
        image_uploader: Optional[Callable[[str], str]] = None,
        image_upload_mode: ImageUploadMode = 'local',
        code_theme: CodeTheme = 'atom-one-dark',
        mac_style: bool = True,
        browser_ws_endpoint: Optional[str] = None,
        browser_type: BrowserType = 'chromium',
        browser_connection_type: BrowserConnectionType = 'auto',
        browser_token: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为微信公众号格式

    :param markdown: Markdown内容或文件路径
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式（远程浏览器时忽略）
    :param wrap_full_html: 是否包装为完整HTML文档
    :param wait_timeout: 等待超时时间（秒）
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址（字符串或列表）
    :param image_uploader: 图片上传回调函数
    :param image_upload_mode: 图片上传模式（local/remote/all）
    :param code_theme: 代码主题
    :param mac_style: 是否启用 Mac 风格
    :param browser_ws_endpoint: 远程浏览器 WebSocket 端点
    :param browser_type: 浏览器类型（chromium/firefox/webkit）
    :param browser_connection_type: 连接类型（auto/cdp/playwright）
    :param browser_token: 远程浏览器访问令牌
    :param proxy: 代理配置
    :return: HTML内容或文件路径
    """
    return convert(
        markdown=markdown,
        platform='wechat',
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        headless=headless,
        wrap_full_html=wrap_full_html,
        wait_timeout=wait_timeout,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode,
        code_theme=code_theme,
        mac_style=mac_style,
        browser_ws_endpoint=browser_ws_endpoint,
        browser_type=browser_type,
        browser_connection_type=browser_connection_type,
        browser_token=browser_token,
        proxy=proxy
    )


def to_zhihu(
        markdown: Union[str, Path, List[Union[str, Path]]],
        theme: Union[str, List[str], None] = 'normal',
        output_dir: Optional[Union[str, Path]] = None,
        return_html: bool = True,
        headless: bool = True,
        wrap_full_html: bool = False,
        wait_timeout: int = 30,
        retry_count: int = 1,
        on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        editor_url: Optional[Union[str, List[str]]] = None,
        image_uploader: Optional[Callable[[str], str]] = None,
        image_upload_mode: ImageUploadMode = 'local',
        code_theme: CodeTheme = 'atom-one-dark',
        mac_style: bool = True,
        browser_ws_endpoint: Optional[str] = None,
        browser_type: BrowserType = 'chromium',
        browser_connection_type: BrowserConnectionType = 'auto',
        browser_token: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为知乎格式

    参数说明同 to_wechat
    """
    return convert(
        markdown=markdown,
        platform='zhihu',
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        headless=headless,
        wrap_full_html=wrap_full_html,
        wait_timeout=wait_timeout,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode,
        code_theme=code_theme,
        mac_style=mac_style,
        browser_ws_endpoint=browser_ws_endpoint,
        browser_type=browser_type,
        browser_connection_type=browser_connection_type,
        browser_token=browser_token,
        proxy=proxy
    )


def to_juejin(
        markdown: Union[str, Path, List[Union[str, Path]]],
        theme: Union[str, List[str], None] = 'normal',
        output_dir: Optional[Union[str, Path]] = None,
        return_html: bool = True,
        headless: bool = True,
        wrap_full_html: bool = False,
        wait_timeout: int = 30,
        retry_count: int = 1,
        on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        editor_url: Optional[Union[str, List[str]]] = None,
        image_uploader: Optional[Callable[[str], str]] = None,
        image_upload_mode: ImageUploadMode = 'local',
        code_theme: CodeTheme = 'atom-one-dark',
        mac_style: bool = True,
        browser_ws_endpoint: Optional[str] = None,
        browser_type: BrowserType = 'chromium',
        browser_connection_type: BrowserConnectionType = 'auto',
        browser_token: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为稀土掘金格式

    参数说明同 to_wechat
    """
    return convert(
        markdown=markdown,
        platform='juejin',
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        headless=headless,
        wrap_full_html=wrap_full_html,
        wait_timeout=wait_timeout,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode,
        code_theme=code_theme,
        mac_style=mac_style,
        browser_ws_endpoint=browser_ws_endpoint,
        browser_type=browser_type,
        browser_connection_type=browser_connection_type,
        browser_token=browser_token,
        proxy=proxy
    )