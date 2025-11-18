# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:0.672Z
# 文件描述：将 Markdown 转换为微信公众号、知乎、稀土掘金等平台格式(mdnice - Markdown to Multi-Platform Converter)
# 文件路径：mdnice/__init__.py

"""
快速开始:
    >>> from mdnice import to_wechat, to_zhihu, to_juejin
    >>> html = to_wechat('article.md', theme='rose')
    >>> html = to_zhihu('article.md', theme='geekBlack')
    >>> html = to_juejin('article.md', theme='scienceBlue')

通用转换:
    >>> from mdnice import convert
    >>> html = convert('article.md', platform='wechat')

图片上传:
    >>> def my_uploader(image_path: str) -> str:
    >>>     # 上传逻辑
    >>>     return "https://cdn.example.com/image.png"
    >>>
    >>> html = to_wechat(
    >>>     'article.md',
    >>>     image_uploader=my_uploader,
    >>>     image_upload_mode='local'  # 只上传本地图片
    >>> )
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
    create_smms_uploader,
    create_qiniu_uploader,
    create_github_uploader,
    create_local_uploader,
)

import os
import re
import time
import random
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from typing import Union, List, Optional, Callable, Dict, Any, Literal


__all__ = [
    'convert',
    'to_wechat',
    'to_zhihu',
    'to_juejin',
    'MarkdownConverter',
    'ConversionError',
    'ImageUploadMode',
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
    # 便捷函数
    'create_smms_uploader',
    'create_qiniu_uploader',
    'create_github_uploader',
    'create_local_uploader',
]


Platform = Literal['wechat', 'zhihu', 'juejin']
ImageUploadMode = Literal['local', 'remote', 'all']


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
                editor_url: Optional[str] = None,
                image_uploader: Optional[Callable[[str], str]] = None,
                image_upload_mode: ImageUploadMode = 'local',
                chromedriver_path: Optional[str] = None) -> None:  # 新增参数
        """
        初始化转换器
        
        :param headless: 是否使用无头模式
        :param wait_timeout: 等待超时时间（秒）
        :param retry_count: 失败重试次数
        :param on_error: 错误通知回调函数
        :param editor_url: 自定义编辑器网址
        :param image_uploader: 图片上传回调函数
        :param image_upload_mode: 图片上传模式
        :param chromedriver_path: 自定义 ChromeDriver 路径（可选，默认自动管理）
        """
        self.headless: bool = headless
        self.wait_timeout: int = wait_timeout
        self.retry_count: int = retry_count
        self.on_error: Optional[Callable[[
            str, Dict[str, Any]], None]] = on_error
        self.image_uploader: Optional[Callable[[str], str]] = image_uploader
        self.image_upload_mode: ImageUploadMode = image_upload_mode
        self.driver: Optional[webdriver.Chrome] = None

        # 默认和备用地址
        self.default_url: str = "https://xiaoqiangclub.github.io/md/"
        self.backup_url: str = "https://whaoa.github.io/markdown-nice/"

        # 构建URL列表（优先级：自定义 > 默认 > 备用）
        self.url_list: List[str] = []
        if editor_url:
            self.url_list.append(editor_url)
            print(f"🔧 使用自定义编辑器地址: {editor_url}")

        # 添加默认地址（如果不是自定义地址）
        if editor_url != self.default_url:
            self.url_list.append(self.default_url)

        # 添加备用地址（如果不重复）
        if self.backup_url not in self.url_list:
            self.url_list.append(self.backup_url)

        self.current_url: str = self.url_list[0]
        self.current_url_index: int = 0

        print(f"📋 可用地址列表: {len(self.url_list)} 个")
        for idx, url in enumerate(self.url_list, 1):
            url_type = "自定义" if idx == 1 and editor_url else (
                "默认" if url == self.default_url else "备用")
            print(f"   {idx}. [{url_type}] {url}")

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

        # ChromeDriver 路径
        self.chromedriver_path: Optional[str] = chromedriver_path

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


    def _init_driver(self) -> None:
        """初始化浏览器驱动"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--enable-clipboard')
            chrome_options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.clipboard': 1
            })

            # 支持自定义驱动路径
            if self.chromedriver_path:
                from selenium.webdriver.chrome.service import Service
                service = Service(executable_path=self.chromedriver_path)
                self.driver = webdriver.Chrome(
                    service=service, options=chrome_options)
                print(f"✅ 使用自定义 ChromeDriver: {self.chromedriver_path}")
            else:
                # 使用 Selenium Manager 自动管理
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✅ 浏览器驱动初始化成功（自动管理）")

            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(self.wait_timeout)

        except Exception as e:
            error_msg = f"浏览器驱动初始化失败: {str(e)}"
            print(f"❌ {error_msg}")

            if "chromedriver" in str(e).lower():
                print("💡 提示：")
                print("   1. 确保已安装 Chrome 浏览器")
                print("   2. 首次运行时会自动下载 ChromeDriver")
                print("   3. 或手动指定路径：chromedriver_path='/path/to/chromedriver'")

            self._notify_error(
                error_msg, {'stage': '初始化浏览器', 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _close_driver(self) -> None:
        """关闭浏览器驱动"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
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

                # 提示切换地址
                if url_index > 0:
                    url_type = "备用" if url == self.backup_url else (
                        "默认" if url == self.default_url else "其他")
                    print(f"🔄 切换到{url_type}地址...")

                print(
                    f"🌐 正在打开网页 [{url_index + 1}/{len(self.url_list)}]: {self.current_url}")
                self.driver.get(self.current_url)

                # 等待关键元素加载
                WebDriverWait(self.driver, self.wait_timeout).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "CodeMirror"))
                )
                time.sleep(3)
                print(f"✅ 网页加载成功")
                return

            except Exception as e:
                last_error = e
                error_msg = f"网页加载失败 ({url}): {str(e)}"
                print(f"❌ {error_msg}")

                # 如果还有其他URL可尝试
                if url_index < len(self.url_list) - 1:
                    print(f"⏳ 将在2秒后尝试下一个地址...")
                    time.sleep(2)
                else:
                    # 所有URL都失败了
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
            self.driver.execute_script(js_code)
            print("✅ 已注入复制拦截器")
        except Exception as e:
            error_msg = f"注入拦截器失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '注入拦截器', 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

    def _select_theme(self, theme: str) -> None:
        """
        选择主题
        
        :param theme: 主题名称
        """
        try:
            theme_button = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.element_to_be_clickable((By.ID, "nice-menu-theme"))
            )
            theme_button.click()
            time.sleep(0.5)

            theme_id = f"nice-menu-theme-{theme}"
            theme_item = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.element_to_be_clickable((By.ID, theme_id))
            )
            theme_item.click()

            print(f"🎨 已选择主题: {self.THEME_NAMES.get(theme, theme)}")
            time.sleep(1.5)
        except Exception as e:
            error_msg = f"选择主题失败: {str(e)}"
            print(f"❌ {error_msg}")
            self._notify_error(
                error_msg, {'stage': '选择主题', 'theme': theme, 'error_type': type(e).__name__})
            raise ConversionError(error_msg) from e

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

        # Data URL 特殊处理：在 'all' 模式下才上传
        if self._is_data_url(image_path):
            return self.image_upload_mode == 'all'

        # 根据模式决定是否上传
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
        print(
            f"🖼️ 开始处理Markdown中的图片 [模式: {mode_names[self.image_upload_mode]}]")

        # 匹配Markdown图片语法：![alt](path) 和 ![alt](path "title")
        pattern = r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'

        uploaded_count = 0
        skipped_count = 0
        failed_count = 0

        def replace_image(match: re.Match) -> str:
            nonlocal uploaded_count, skipped_count, failed_count

            alt_text = match.group(1)
            image_path = match.group(2)
            title_text = match.group(3) if match.group(3) else None

            # 检查是否为远程URL
            is_remote = self._is_remote_url(image_path)
            is_data = self._is_data_url(image_path)

            # 判断是否应该上传
            if not self._should_upload_image(image_path, is_remote):
                skipped_count += 1
                if is_remote:
                    print(f"  ⏭️ 跳过网络图片 [模式不匹配]: {image_path[:60]}...")
                elif is_data:
                    print(f"  ⏭️ 跳过Data URL图片 [模式不匹配]")
                else:
                    print(f"  ⏭️ 跳过本地图片 [模式不匹配]: {Path(image_path).name}")
                return match.group(0)

            # 需要上传的图片
            try:
                upload_target = image_path

                # 如果是本地路径，需要解析完整路径
                if not is_remote and not is_data:
                    # 处理相对路径
                    if base_path and not os.path.isabs(image_path):
                        full_path = base_path / image_path
                    else:
                        full_path = Path(image_path)

                    # 规范化路径
                    full_path = full_path.resolve()

                    # 检查文件是否存在
                    if not full_path.exists():
                        print(f"  ⚠️ 图片文件不存在，保持原样: {image_path}")
                        skipped_count += 1
                        return match.group(0)

                    # 检查是否为图片文件
                    valid_extensions = {'.jpg', '.jpeg',
                                        '.png', '.gif', '.bmp', '.webp', '.svg'}
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

                # 调用用户提供的上传函数
                uploaded_url = self.image_uploader(upload_target)

                if not uploaded_url:
                    raise ValueError("上传函数返回空URL")

                print(f"  ✅ 图片已上传: {uploaded_url}")
                uploaded_count += 1

                # 返回新的Markdown图片语法
                if title_text:
                    return f'![{alt_text}]({uploaded_url} "{title_text}")'
                else:
                    return f'![{alt_text}]({uploaded_url})'

            except Exception as e:
                print(f"  ❌ 图片上传失败: {str(e)}")
                failed_count += 1
                # 上传失败，保持原样
                return match.group(0)

        # 替换所有图片
        result = re.sub(pattern, replace_image, markdown_content)

        # 输出统计信息
        total = uploaded_count + skipped_count + failed_count
        if total > 0:
            print(
                f"🖼️ 图片处理完成: 共 {total} 张 (上传 {uploaded_count}, 跳过 {skipped_count}, 失败 {failed_count})")
        else:
            print(f"🖼️ 未检测到图片")

        return result

    def _input_markdown(self, markdown_content: str) -> None:
        """
        输入Markdown内容并触发转换
        
        :param markdown_content: Markdown文本内容
        """
        try:
            print(f"📝 正在输入Markdown内容（{len(markdown_content)} 字符）...")

            js_code = """
            var editor = document.querySelector('.CodeMirror').CodeMirror;
            var content = arguments[0];
            
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
            """

            self.driver.execute_script(js_code, markdown_content)
            time.sleep(1)

            current_content = self.driver.execute_script("""
                var editor = document.querySelector('.CodeMirror').CodeMirror;
                return editor ? editor.getValue() : null;
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
                preview_content = self.driver.execute_script("""
                    var editor = document.querySelector('#nice-rich-text-editor');
                    if (editor && editor.innerHTML) {
                        var content = editor.innerHTML.trim();
                        return content.length > 100;
                    }
                    return false;
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
            js_clear = """
            var editor = document.querySelector('.CodeMirror').CodeMirror;
            editor.setValue('');
            editor.refresh();
            """
            self.driver.execute_script(js_clear)
            time.sleep(0.5)
            print("✅ 已清空编辑器")
        except Exception as e:
            print(f"⚠️ 清空编辑器失败: {e}")

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

            preview_check = self.driver.execute_script("""
                var editor = document.querySelector('#nice-rich-text-editor');
                if (editor) {
                    return {
                        hasContent: editor.innerHTML.trim().length > 0,
                        contentLength: editor.innerHTML.trim().length
                    };
                }
                return null;
            """)

            if preview_check:
                print(
                    f"📊 预览区域状态: 长度={preview_check['contentLength']}, 有内容={preview_check['hasContent']}")
                if not preview_check['hasContent']:
                    print("⚠️ 警告：预览区域为空！可能转换未成功")

            self.driver.execute_script("window._capturedHTML = null;")

            try:
                copy_button = WebDriverWait(self.driver, self.wait_timeout).until(
                    EC.element_to_be_clickable((By.ID, button_id))
                )
                print(f"✅ 找到 {platform_name} 复制按钮")
            except TimeoutException:
                raise ConversionError(
                    f"找不到 {platform_name} 复制按钮（ID: {button_id}）")

            print(f"📋 正在触发 {platform_name} 格式复制...")
            copy_button.click()
            time.sleep(1.5)

            html_content = self.driver.execute_script(
                "return window._capturedHTML;")

            if not html_content:
                print("🔄 尝试使用CDP方法...")
                html_content = self._get_html_via_cdp(button_id)

            if not html_content:
                print("⚠️ 使用降级方案：直接从DOM获取（可能缺少部分样式）")
                html_content = self.driver.execute_script("""
                    var editor = document.querySelector('#nice-rich-text-editor');
                    return editor ? editor.innerHTML : '';
                """)

            if not html_content or len(html_content) < 50:
                raise ConversionError(
                    f"获取的HTML内容为空或过短（长度: {len(html_content) if html_content else 0}）")

            print(f"✅ 已获取 {platform_name} 格式HTML（{len(html_content)} 字符）")

            has_inline_style = 'style=' in html_content
            has_style_tag = '<style>' in html_content

            if has_inline_style or has_style_tag:
                print(
                    f"✅ HTML包含样式信息（内联样式:{has_inline_style}, 样式标签:{has_style_tag}）")
            else:
                print("⚠️ 警告：HTML可能不包含样式信息")

            return html_content

        except Exception as e:
            error_msg = f"获取HTML失败: {str(e)}"
            print(f"❌ {error_msg}")

            try:
                debug_info = self.driver.execute_script("""
                    return {
                        editorValue: document.querySelector('.CodeMirror')?.CodeMirror?.getValue()?.substring(0, 100),
                        previewContent: document.querySelector('#nice-rich-text-editor')?.innerHTML?.substring(0, 100),
                        capturedHTML: window._capturedHTML ? 'exists' : 'null'
                    };
                """)
                print(f"🔍 调试信息: {debug_info}")
            except:
                pass

            self._notify_error(error_msg, {
                'stage': '获取HTML',
                'platform': platform,
                'error_type': type(e).__name__
            })
            raise ConversionError(error_msg) from e

    def _get_html_via_cdp(self, button_id: str) -> Optional[str]:
        """
        通过CDP获取剪贴板内容
        
        :param button_id: 复制按钮的ID
        :return: 剪贴板中的HTML内容
        """
        try:
            self.driver.execute_cdp_cmd('Browser.grantPermissions', {
                'permissions': ['clipboardReadWrite', 'clipboardSanitizedWrite']
            })

            js_read_clipboard = f"""
            return new Promise(async (resolve) => {{
                try {{
                    document.querySelector('#{button_id}').click();
                    await new Promise(r => setTimeout(r, 800));
                    
                    const clipboardItems = await navigator.clipboard.read();
                    for (const item of clipboardItems) {{
                        if (item.types.includes('text/html')) {{
                            const blob = await item.getType('text/html');
                            const text = await blob.text();
                            resolve(text);
                            return;
                        }}
                    }}
                    resolve(null);
                }} catch (err) {{
                    console.error('读取剪贴板失败:', err);
                    resolve(null);
                }}
            }});
            """

            html_content = self.driver.execute_script(js_read_clipboard)
            if html_content:
                print("✅ 通过CDP成功获取剪贴板内容")
            return html_content
        except Exception as e:
            print(f"❌ CDP方法失败: {e}")
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
                    filename = Path(original_name).stem + \
                        f'_{platform_suffix}.html'
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
                platform: Platform = 'wechat') -> Union[str, List[str], Path, List[Path]]:
        """
        转换Markdown到指定平台格式

        :param markdown: Markdown内容或文件路径
        :param theme: 主题选择
        :param output_dir: 输出目录
        :param return_html: 是否返回HTML内容
        :param wrap_full_html: 是否包装为完整HTML
        :param platform: 目标平台（wechat/zhihu/juejin）
        :return: HTML内容或文件路径
        """
        try:
            if platform not in self.PLATFORM_CONFIG:
                raise ValueError(f"不支持的平台: {platform}")

            print(f"\n🎯 目标平台: {self.PLATFORM_CONFIG[platform]['name']}")

            self._retry_on_error(self._init_driver)
            self._retry_on_error(self._load_page)
            self._inject_copy_interceptor()

            is_multiple = isinstance(markdown, list)
            markdown_list = markdown if is_multiple else [markdown]

            results = []
            failed_items = []

            for idx, md_item in enumerate(markdown_list, 1):
                print(f"\n{'='*70}")
                print(f"📌 处理第 {idx}/{len(markdown_list)} 项")
                print(f"{'='*70}")

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

                        # 处理图片（传入文件所在目录用于解析相对路径）
                        md_content = self._process_images_in_markdown(
                            md_content,
                            base_path=file_path.parent
                        )
                    else:
                        md_content = md_item
                        original_name = None
                        print(f"📝 使用Markdown内容（{len(md_content)} 字符）")

                        # 处理图片（没有基准路径）
                        md_content = self._process_images_in_markdown(
                            md_content)

                    if idx > 1:
                        self._clear_editor()

                    selected_theme = self._parse_theme(theme)
                    self._select_theme(selected_theme)

                    self._input_markdown(md_content)

                    html_content = self._retry_on_error(
                        self._get_converted_html, platform)

                    if output_dir:
                        file_path = self._save_html(
                            html_content, output_dir, original_name, wrap_full_html, platform)
                        results.append(
                            file_path if not return_html else html_content)
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

            print(f"\n{'='*70}")
            if failed_items:
                print(f"⚠️ 部分完成！成功 {len(results)}/{len(markdown_list)} 项")
                for item in failed_items:
                    print(f"  ❌ 失败项 {item['index']}: {item['error']}")
            else:
                print(f"🎉 全部完成！共 {len(results)} 项")
            print(f"{'='*70}\n")

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
    retry_count: int = 1,
    on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    editor_url: Optional[str] = None,
    image_uploader: Optional[Callable[[str], str]] = None,
    image_upload_mode: ImageUploadMode = 'local'
) -> Union[str, List[str], Path, List[Path]]:
    """
    通用转换函数：转换Markdown到指定平台格式

    :param markdown: Markdown内容或文件路径（支持单个或列表）
    :param platform: 目标平台
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录（None则不保存）
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式
    :param wrap_full_html: 是否包装为完整HTML文档
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址
    :param image_uploader: 图片上传回调函数，接收图片路径或URL，返回图床URL
    :param image_upload_mode: 图片上传模式（local=仅本地, remote=仅网络, all=全部）
    :return: HTML内容字符串、文件路径或它们的列表
    """
    converter = MarkdownConverter(
        headless=headless,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode
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
    retry_count: int = 1,
    on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    editor_url: Optional[str] = None,
    image_uploader: Optional[Callable[[str], str]] = None,
    image_upload_mode: ImageUploadMode = 'local'
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为微信公众号格式

    :param markdown: Markdown内容或文件路径
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式
    :param wrap_full_html: 是否包装为完整HTML文档
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址
    :param image_uploader: 图片上传回调函数，接收图片路径或URL，返回图床URL
    :param image_upload_mode: 图片上传模式（local=仅本地, remote=仅网络, all=全部）
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
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode
    )


def to_zhihu(
    markdown: Union[str, Path, List[Union[str, Path]]],
    theme: Union[str, List[str], None] = 'normal',
    output_dir: Optional[Union[str, Path]] = None,
    return_html: bool = True,
    headless: bool = True,
    wrap_full_html: bool = False,
    retry_count: int = 1,
    on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    editor_url: Optional[str] = None,
    image_uploader: Optional[Callable[[str], str]] = None,
    image_upload_mode: ImageUploadMode = 'local'
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为知乎格式

    :param markdown: Markdown内容或文件路径
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式
    :param wrap_full_html: 是否包装为完整HTML文档
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址
    :param image_uploader: 图片上传回调函数，接收图片路径或URL，返回图床URL
    :param image_upload_mode: 图片上传模式（local=仅本地, remote=仅网络, all=全部）
    :return: HTML内容或文件路径
    """
    return convert(
        markdown=markdown,
        platform='zhihu',
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        headless=headless,
        wrap_full_html=wrap_full_html,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode
    )


def to_juejin(
    markdown: Union[str, Path, List[Union[str, Path]]],
    theme: Union[str, List[str], None] = 'normal',
    output_dir: Optional[Union[str, Path]] = None,
    return_html: bool = True,
    headless: bool = True,
    wrap_full_html: bool = False,
    retry_count: int = 1,
    on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    editor_url: Optional[str] = None,
    image_uploader: Optional[Callable[[str], str]] = None,
    image_upload_mode: ImageUploadMode = 'local'
) -> Union[str, List[str], Path, List[Path]]:
    """
    转换Markdown为稀土掘金格式

    :param markdown: Markdown内容或文件路径
    :param theme: 主题名称、列表或None（随机）
    :param output_dir: 输出目录
    :param return_html: 是否返回HTML内容
    :param headless: 是否使用无头模式
    :param wrap_full_html: 是否包装为完整HTML文档
    :param retry_count: 失败重试次数
    :param on_error: 错误通知回调函数
    :param editor_url: 自定义编辑器网址
    :param image_uploader: 图片上传回调函数，接收图片路径或URL，返回图床URL
    :param image_upload_mode: 图片上传模式（local=仅本地, remote=仅网络, all=全部）
    :return: HTML内容或文件路径
    """
    return convert(
        markdown=markdown,
        platform='juejin',
        theme=theme,
        output_dir=output_dir,
        return_html=return_html,
        headless=headless,
        wrap_full_html=wrap_full_html,
        retry_count=retry_count,
        on_error=on_error,
        editor_url=editor_url,
        image_uploader=image_uploader,
        image_upload_mode=image_upload_mode
    )