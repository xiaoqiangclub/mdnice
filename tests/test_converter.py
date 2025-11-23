# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：单元测试
# 文件路径：tests/test_converter.py

import pytest
from pathlib import Path
from mdnice import (
    MarkdownConverter,
    ConversionError,
    convert,
    to_wechat,
    to_zhihu,
    to_juejin,
    __version__,
)


class TestVersion:
    """测试版本信息"""

    def test_version_exists(self):
        """测试版本号存在"""
        assert __version__
        assert isinstance(__version__, str)
        assert len(__version__) > 0
        assert __version__ == "0.0.3"  # 验证版本号


class TestMarkdownConverter:
    """测试 MarkdownConverter 类"""

    def test_init_default(self):
        """测试默认初始化"""
        converter = MarkdownConverter()
        assert converter.headless is True
        assert converter.wait_timeout == 30
        assert converter.retry_count == 1
        assert converter.image_uploader is None
        assert converter.image_upload_mode == 'local'
        assert converter.chromedriver_path is None  # 🆕 测试新参数

    def test_init_custom(self):
        """测试自定义初始化"""
        converter = MarkdownConverter(
            headless=False,
            wait_timeout=60,
            retry_count=3,
            image_upload_mode='all',
            chromedriver_path='/custom/path/chromedriver'  # 🆕
        )
        assert converter.headless is False
        assert converter.wait_timeout == 60
        assert converter.retry_count == 3
        assert converter.image_upload_mode == 'all'
        assert converter.chromedriver_path == '/custom/path/chromedriver'  # 🆕

    def test_url_list(self):
        """测试URL列表"""
        converter = MarkdownConverter()
        assert len(converter.url_list) >= 2
        assert converter.default_url in converter.url_list
        assert converter.backup_url in converter.url_list

    def test_custom_editor_url(self):
        """测试自定义编辑器URL"""
        custom_url = "https://custom.example.com/"
        converter = MarkdownConverter(editor_url=custom_url)
        assert custom_url in converter.url_list
        assert converter.url_list[0] == custom_url


class TestThemes:
    """测试主题功能"""

    def test_available_themes(self):
        """测试主题列表"""
        converter = MarkdownConverter()
        assert len(converter.AVAILABLE_THEMES) == 20
        assert 'normal' in converter.AVAILABLE_THEMES
        assert 'rose' in converter.AVAILABLE_THEMES
        assert 'geekBlack' in converter.AVAILABLE_THEMES

    def test_theme_names(self):
        """测试主题名称"""
        converter = MarkdownConverter()
        assert converter.THEME_NAMES['rose'] == '蔷薇紫'
        assert converter.THEME_NAMES['geekBlack'] == '极客黑'
        assert converter.THEME_NAMES['normal'] == '默认主题'

    def test_parse_theme_single(self):
        """测试解析单个主题"""
        converter = MarkdownConverter()
        theme = converter._parse_theme('rose')
        assert theme == 'rose'

    def test_parse_theme_list(self):
        """测试从列表解析主题"""
        converter = MarkdownConverter()
        themes = ['rose', 'geekBlack', 'scienceBlue']
        theme = converter._parse_theme(themes)
        assert theme in themes

    def test_parse_theme_random(self):
        """测试随机主题"""
        converter = MarkdownConverter()
        theme = converter._parse_theme('random')
        assert theme in converter.AVAILABLE_THEMES

    def test_parse_theme_invalid(self):
        """测试无效主题"""
        converter = MarkdownConverter()
        with pytest.raises(ValueError):
            converter._parse_theme('invalid_theme')


class TestPlatforms:
    """测试平台配置"""

    def test_platform_config(self):
        """测试平台配置"""
        converter = MarkdownConverter()
        assert 'wechat' in converter.PLATFORM_CONFIG
        assert 'zhihu' in converter.PLATFORM_CONFIG
        assert 'juejin' in converter.PLATFORM_CONFIG

    def test_platform_info(self):
        """测试平台信息"""
        converter = MarkdownConverter()
        wechat = converter.PLATFORM_CONFIG['wechat']
        assert 'button_id' in wechat
        assert 'name' in wechat
        assert 'suffix' in wechat
        assert wechat['name'] == '微信公众号'


class TestImageUpload:
    """测试图片上传功能"""

    def test_is_remote_url(self):
        """测试远程URL识别"""
        converter = MarkdownConverter()
        assert converter._is_remote_url('http://example.com/image.jpg') is True
        assert converter._is_remote_url(
            'https://example.com/image.jpg') is True
        assert converter._is_remote_url('ftp://example.com/image.jpg') is True
        assert converter._is_remote_url('/path/to/image.jpg') is False
        assert converter._is_remote_url('image.jpg') is False

    def test_is_data_url(self):
        """测试DataURL识别"""
        converter = MarkdownConverter()
        assert converter._is_data_url('data:image/png;base64,iVBOR...') is True
        assert converter._is_data_url('http://example.com/image.jpg') is False

    def test_should_upload_local_mode(self):
        """测试本地模式上传判断"""
        def mock_uploader(path: str) -> str:
            return "https://cdn.com/image.jpg"

        converter = MarkdownConverter(
            image_uploader=mock_uploader,
            image_upload_mode='local'
        )

        # 本地图片应该上传
        assert converter._should_upload_image(
            '/path/to/image.jpg', False) is True
        # 远程图片不应该上传
        assert converter._should_upload_image(
            'http://example.com/img.jpg', True) is False

    def test_should_upload_remote_mode(self):
        """测试远程模式上传判断"""
        def mock_uploader(path: str) -> str:
            return "https://cdn.com/image.jpg"

        converter = MarkdownConverter(
            image_uploader=mock_uploader,
            image_upload_mode='remote'
        )

        # 本地图片不应该上传
        assert converter._should_upload_image(
            '/path/to/image.jpg', False) is False
        # 远程图片应该上传
        assert converter._should_upload_image(
            'http://example.com/img.jpg', True) is True

    def test_should_upload_all_mode(self):
        """测试全部模式上传判断"""
        def mock_uploader(path: str) -> str:
            return "https://cdn.com/image.jpg"

        converter = MarkdownConverter(
            image_uploader=mock_uploader,
            image_upload_mode='all'
        )

        # 所有类型都应该上传
        assert converter._should_upload_image(
            '/path/to/image.jpg', False) is True
        assert converter._should_upload_image(
            'http://example.com/img.jpg', True) is True

    def test_no_uploader(self):
        """测试未设置上传器"""
        converter = MarkdownConverter(image_upload_mode='all')
        assert converter._should_upload_image(
            '/path/to/image.jpg', False) is False


class TestConvenienceFunctions:
    """测试便捷函数"""

    def test_functions_exist(self):
        """测试函数存在"""
        assert callable(convert)
        assert callable(to_wechat)
        assert callable(to_zhihu)
        assert callable(to_juejin)


class TestExceptions:
    """测试异常"""

    def test_conversion_error(self):
        """测试自定义异常"""
        with pytest.raises(ConversionError):
            raise ConversionError("测试错误")


class TestImageUploaders:
    """测试图床上传工具"""

    def test_import_image_uploaders(self):
        """测试导入图床工具"""
        try:
            from mdnice.image_uploaders import (
                SMUploader,
                create_smms_uploader,
                LuoGuoUploader
            )
            assert callable(create_smms_uploader)
        except ImportError as e:
            pytest.fail(f"导入图床工具失败: {e}")

    def test_smms_uploader_init(self):
        """测试 SM.MS 上传器初始化"""
        from mdnice.image_uploaders import SMUploader

        # 默认域名
        uploader1 = SMUploader(api_token='test_token')
        assert 'smms.app' in uploader1.api_url

        # 自定义域名
        uploader2 = SMUploader(
            api_token='test_token',
            api_domain='https://sm.ms'
        )
        assert 'sm.ms' in uploader2.api_url


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
