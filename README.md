<div align="center">

![mdnice](https://s2.loli.net/2025/11/18/xzuPwHCoDiET5r6.jpg)

[![PyPI version](https://img.shields.io/badge/PyPI-0.0.3-blue)](https://pypi.org/project/mdnice) [![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://pypi.org/project/mdnice/) [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE) 

</div>

## 📖 目录

- [✨ 功能特性](#-功能特性)
- [🚀 快速开始](#-快速开始)
- [📦 安装](#-安装)
- [💡 使用文档](#-使用文档)
- [🎨 主题列表](#-主题列表)
- [📤 图片上传](#-图片上传)
- [🌐 远程浏览器](#-远程浏览器)
- [📚 API 参考](#-api-参考)
- [🔧 高级用法](#-高级用法)
- [❓ 常见问题](#-常见问题)
- [📝 更新日志](#-更新日志)
- [💖 打赏支持](#-打赏支持)
- [📄 许可证](#-许可证)

---

# 📝 mdnice

> 将 Markdown 转换为微信公众号、知乎、稀土掘金支持的富文本格式

## ✨ 功能特性

### 🎯 核心功能

- ✅ **多平台支持** - 一键转换为微信公众号、知乎、稀土掘金格式
- ✅ **20+ 精美主题** - 内置 20 种精心设计的文章主题
- ✅ **7 种代码主题** - 支持多种代码高亮主题（Monokai、GitHub、VS2015 等）
- ✅ **Mac 风格代码块** - 可选的 macOS 风格代码装饰
- ✅ **批量处理** - 支持批量转换多个 Markdown 文件
- ✅ **智能重试** - 网络故障自动重试机制
- ✅ **完整样式** - 保留所有内联样式，格式完美还原
- ✅ **HTML 清理** - 自动移除编辑器标记，代码更简洁
- ✅ **零配置** - Playwright 内置浏览器驱动，开箱即用

### 🌐 远程浏览器支持

- 🐳 **Docker 容器环境** - 无需在容器中安装浏览器
- ☁️ **云函数/无服务器** - 完美适配 AWS Lambda、阿里云函数计算等
- 🔄 **共享浏览器服务** - 多实例共享，节省资源
- 💻 **资源受限环境** - 减少本地资源消耗
- 🔌 **灵活部署** - 支持 browserless 和 Playwright 官方远程浏览器

### 📤 图片上传

- 🖼️ **智能识别** - 自动识别本地图片、网络图片、Data URL
- 🎯 **灵活模式** - 支持 3 种上传模式（仅本地/仅网络/全部）
- 🔌 **易于集成** - 简单回调函数即可对接任何图床
- ⚡ **高效处理** - 批量上传，错误容错
- 🌐 **多图床支持** - 内置 9 种主流图床上传器

#### 支持的图床

| 图床名称 | 免费额度 | 特点 | 适用场景 |
|---------|---------|------|---------|
| SM.MS | 5MB/文件 | 国内访问快 | 临时上传 |
| 微信公众号 | - | 官方稳定 | 公众号文章 ⭐ |
| 七牛云 | 10GB 存储 | 稳定可靠 | 长期存储 |
| 阿里云 OSS | 40GB(6个月) | 企业级 | 生产环境 |
| GitHub | 无限 | 完全免费 | 技术博客 |
| 本地存储 | - | 无网络依赖 | 本地预览 |

### 📊 支持平台

| 平台 | 函数 | 说明 |
|------|------|------|
| 📱 微信公众号 | `to_wechat()` | 完美适配公众号编辑器 |
| 📘 知乎 | `to_zhihu()` | 适配知乎文章编辑器 |
| 💎 稀土掘金 | `to_juejin()` | 适配掘金文章编辑器 |

---

## 🚀 快速开始

### 最简单的使用

```python
from mdnice import to_wechat

# 一行代码完成转换
html = to_wechat('article.md')
print(f"转换成功！HTML长度：{len(html)}")
```

> 💡 **首次运行提示**：需要先安装 Playwright 浏览器（仅一次）

### 5 分钟上手

```python
from mdnice import to_wechat, to_zhihu, to_juejin

# 示例 1: 微信公众号格式（带代码主题）
html = to_wechat(
    'article.md',
    theme='rose',              # 文章主题
    code_theme='monokai',      # 代码主题
    mac_style=True,            # Mac 风格代码块
    output_dir='output/wechat'
)

# 示例 2: 知乎格式
html = to_zhihu(
    'article.md',
    theme='geekBlack',
    code_theme='github',
    mac_style=False,
    output_dir='output/zhihu'
)

# 示例 3: 批量转换
to_wechat(
    ['article1.md', 'article2.md', 'article3.md'],
    theme='random',            # 随机主题
    output_dir='output/batch'
)
```

---

## 📦 安装

### 环境要求

- **Python**: 3.10+
- **浏览器**: 自动安装（Playwright 内置）
- **驱动**: 无需手动安装 ✨

### 安装步骤

#### 1. 安装 mdnice

```bash
pip install mdnice
```

#### 2. 安装 Playwright 浏览器（首次使用）

```bash
playwright install chromium
```

**就这么简单！** 🎉 安装完成后即可使用。

> 💡 **提示**：`playwright install chromium` 只需运行一次，会自动下载约 200MB 的 Chromium 浏览器。

#### 其他安装方式

```bash
# 使用 poetry
poetry add mdnice
poetry run playwright install chromium

# 从源码安装
git clone https://github.com/xiaoqiangclub/mdnice.git
cd mdnice
pip install -e .
playwright install chromium
```

### 验证安装

```python
from mdnice import to_wechat, __version__

# 查看版本
print(f"mdnice 版本: {__version__}")

# 测试转换
html = to_wechat("# 测试\n\n这是测试内容。")
print("✅ 安装成功！" if html else "❌ 安装失败")
```

---

## 💡 使用文档

### 基础用法

#### 1. 转换单个文件

```python
from mdnice import to_wechat

# 转换文件
html = to_wechat('article.md', theme='rose')

# 保存为 HTML
to_wechat(
    'article.md',
    theme='rose',
    output_dir='output'  # 自动保存为 output/article_wechat.html
)
```

#### 2. 转换 Markdown 文本

```python
from mdnice import to_wechat

markdown_text = """
# 标题

这是 **Markdown** 文本。

```python
print("Hello World")
```
"""

html = to_wechat(markdown_text, theme='geekBlack')
```

#### 3. 使用 Path 对象

```python
from pathlib import Path
from mdnice import to_wechat

file_path = Path('documents/article.md')
html = to_wechat(file_path, theme='scienceBlue')
```

### 批量转换

```python
from mdnice import to_wechat

files = ['article1.md', 'article2.md', 'article3.md']

# 批量转换，随机主题
html_list = to_wechat(
    files,
    theme='random',
    output_dir='output/batch'
)

print(f"成功转换 {len(html_list)} 个文件")
```

### 自定义主题

```python
from mdnice import to_wechat

# 指定主题
html = to_wechat('article.md', theme='rose', code_theme='monokai')

# 完全随机
html = to_wechat('article.md', theme='random')

# 从列表中随机
html = to_wechat(
    'article.md',
    theme=['rose', 'geekBlack', 'scienceBlue']
)
```

### 多平台转换

```python
from mdnice import to_wechat, to_zhihu, to_juejin

article = 'article.md'

# 一文多发
to_wechat(article, theme='rose', output_dir='output/wechat')
to_zhihu(article, theme='geekBlack', output_dir='output/zhihu')
to_juejin(article, theme='scienceBlue', output_dir='output/juejin')
```

---

## 🎨 主题列表

### 文章主题（20 种）

| 主题代码 | 中文名称 | 风格 | 推荐场景 |
|---------|---------|------|---------|
| `rose` | 蔷薇紫 | 优雅紫色系 | 优质文章 ⭐ |
| `geekBlack` | 极客黑 | 程序员最爱 | 技术博客 ⭐ |
| `scienceBlue` | 科技蓝 | 科技感蓝色 | 科技文章 ⭐ |
| `extremeBlack` | 极简黑 | 黑白极简 | 极简风格 |
| `blueMountain` | 前端之巅同款 | 专业技术 | 技术分享 |
| `normal` | 默认主题 | 简洁大方 | 通用文章 |
| `shanchui` | 山吹 | 温暖黄色 | 温馨内容 |
| `fullStackBlue` | 全栈蓝 | 专业蓝色 | 技术文章 |
| `nightPurple` | 凝夜紫 | 深邃紫色 | 深度分析 |
| `cuteGreen` | 萌绿 | 清新绿色 | 轻松阅读 |

[查看所有 20 种主题](https://github.com/xiaoqiangclub/mdnice#完整主题列表)

### 代码主题（7 种）

| 主题代码 | 主题名称 | 风格 |
|---------|---------|------|
| `atom-one-dark` | Atom One Dark | 深色经典（默认）⭐ |
| `monokai` | Monokai | 经典 Monokai ⭐ |
| `github` | GitHub | GitHub 风格 |
| `vs2015` | VS2015 | Visual Studio 风格 |
| `atom-one-light` | Atom One Light | 浅色经典 |
| `xcode` | Xcode | Xcode 编辑器风格 |
| `wechat` | 微信代码主题 | 微信官方风格 |

### Mac 风格代码块

```python
from mdnice import to_wechat

# 启用 Mac 风格（默认）
html = to_wechat('article.md', mac_style=True)

# 禁用 Mac 风格
html = to_wechat('article.md', mac_style=False)
```

---

## 📤 图片上传

mdnice 支持自动将图片上传到图床，适应不同平台要求。

### 快速开始

```python
from mdnice import to_wechat

def upload_image(image_path: str) -> str:
    """自定义上传函数"""
    # 你的上传逻辑
    return "https://cdn.example.com/image.jpg"

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=upload_image,
    image_upload_mode='local'  # 只上传本地图片
)
```

### 使用内置图床

#### 1. SM.MS 图床

```python
from mdnice import to_wechat
from mdnice.image_uploaders import create_smms_uploader

# 创建上传器
uploader = create_smms_uploader(
    api_token='YOUR_TOKEN',
    api_domain='https://smms.app'  # 国内优化域名
)

# 使用
html = to_wechat(
    'article.md',
    image_uploader=uploader,
    image_upload_mode='all'  # 上传所有图片
)
```

#### 2. 微信公众号图床

```python
from mdnice import to_wechat
from mdnice.image_uploaders import create_wechat_uploader, WechatUploadType

# 创建微信上传器
uploader = create_wechat_uploader(
    app_id='wx1234567890',
    app_secret='your_app_secret',
    upload_type=WechatUploadType.NEWS_IMAGE  # 图文消息图片
)

html = to_wechat(
    'article.md',
    image_uploader=uploader,
    image_upload_mode='local'
)
```

**微信图床上传类型：**

- `TEMPORARY` - 临时素材（3天有效期）
- `PERMANENT` - 永久素材
- `NEWS_IMAGE` - 图文消息图片（推荐）✨

#### 3. 七牛云

```python
from mdnice.image_uploaders import create_qiniu_uploader

uploader = create_qiniu_uploader(
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY',
    bucket='your_bucket',
    domain='your-cdn-domain.com'
)
```

#### 4. GitHub 图床

```python
from mdnice.image_uploaders import create_github_uploader

uploader = create_github_uploader(
    token='ghp_your_token',
    repo='username/image-repo',
    branch='main',
    use_jsdelivr=True  # 使用 CDN 加速
)
```

### 上传模式

| 模式 | 值 | 说明 |
|------|-----|------|
| 仅本地 | `'local'` | 只上传本地图片（默认） |
| 仅网络 | `'remote'` | 只上传网络图片 |
| 全部 | `'all'` | 上传所有图片 |

---

## 🌐 远程浏览器

mdnice 支持连接到远程浏览器服务，特别适用于容器化部署和云函数环境。

### 为什么使用远程浏览器？

- 🐳 **容器环境** - 无需在容器中安装浏览器
- ☁️ **云函数** - AWS Lambda、阿里云函数计算等
- 💰 **节省资源** - 多个实例共享一个浏览器
- ⚡ **更快启动** - 浏览器常驻，无需每次启动

### 支持的远程浏览器

#### 1. browserless（推荐）

```bash
# 启动 browserless
docker run -p 3000:3000 ghcr.io/browserless/chromium
```

```python
from mdnice import to_wechat

# 连接到 browserless
html = to_wechat(
    'article.md',
    theme='rose',
    browser_ws_endpoint='ws://localhost:3000'
)
```

#### 2. 带 Token 的 browserless

```python
# 方式 1: 独立参数
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_secret_token'
)

# 方式 2: URL 参数
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000?token=your_secret_token'
)
```

#### 3. browserless.io 云服务

```python
html = to_wechat(
    'article.md',
    browser_ws_endpoint='wss://chrome.browserless.io',
    browser_token='YOUR_API_KEY'
)
```

#### 4. Playwright 官方远程浏览器

```python
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3001',
    browser_connection_type='playwright'
)
```

### Docker Compose 部署

```yaml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium:latest
    ports:
      - "3000:3000"
    environment:
      - MAX_CONCURRENT_SESSIONS=10
      - CONNECTION_TIMEOUT=60000
      - TOKEN=your_secret_token  # 可选
    restart: unless-stopped
```

```bash
# 启动服务
docker-compose up -d

# 使用
python your_script.py
```

### 连接参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `browser_ws_endpoint` | `str` | `None` | WebSocket 端点 |
| `browser_type` | `str` | `'chromium'` | 浏览器类型 |
| `browser_connection_type` | `str` | `'auto'` | 连接类型（auto/cdp/playwright） |
| `browser_token` | `str` | `None` | 访问令牌 |

---

## 📚 API 参考

### 平台专用函数

#### `to_wechat()`

```python
def to_wechat(
    markdown: Union[str, Path, List],
    theme: Union[str, List[str], None] = 'normal',
    code_theme: str = 'atom-one-dark',
    mac_style: bool = True,
    output_dir: Optional[Union[str, Path]] = None,
    return_html: bool = True,
    headless: bool = True,
    wrap_full_html: bool = False,
    retry_count: int = 1,
    on_error: Optional[Callable] = None,
    editor_url: Optional[str] = None,
    image_uploader: Optional[Callable] = None,
    image_upload_mode: str = 'local',
    browser_ws_endpoint: Optional[str] = None,
    browser_type: str = 'chromium',
    browser_connection_type: str = 'auto',
    browser_token: Optional[str] = None,
    clean_html: bool = True
) -> Union[str, List[str], Path, List[Path]]
```

**核心参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `markdown` | `str/Path/List` | **必需** | Markdown 内容或文件路径 |
| `theme` | `str/List/None` | `'normal'` | 文章主题 |
| `code_theme` | `str` | `'atom-one-dark'` | 代码主题 |
| `mac_style` | `bool` | `True` | 是否启用 Mac 风格 |
| `output_dir` | `str/Path/None` | `None` | 输出目录 |
| `clean_html` | `bool` | `True` | 清理编辑器标记 |

**图片上传参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_uploader` | `Callable` | `None` | 图片上传函数 |
| `image_upload_mode` | `str` | `'local'` | 上传模式（local/remote/all） |

**远程浏览器参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `browser_ws_endpoint` | `str` | `None` | WebSocket 端点 |
| `browser_token` | `str` | `None` | 访问令牌 |
| `browser_connection_type` | `str` | `'auto'` | 连接类型 |

#### `to_zhihu()` 和 `to_juejin()`

参数与 `to_wechat()` 完全相同。

### 通用转换函数

```python
from mdnice import convert

html = convert(
    'article.md',
    platform='wechat',  # 或 'zhihu', 'juejin'
    theme='rose'
)
```

### 核心类

```python
from mdnice import MarkdownConverter

converter = MarkdownConverter(
    headless=True,
    code_theme='monokai',
    mac_style=True,
    browser_ws_endpoint='ws://localhost:3000',
    clean_html=True
)

html = converter.convert('article.md', platform='wechat')
```

---

## 🔧 高级用法

### 1. 自定义编辑器地址

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    editor_url='https://your-domain.com/markdown-nice/'
)
```

**智能容错**：自定义地址 → 默认地址 → 备用地址

### 2. 错误通知回调

```python
def error_handler(error_msg: str, context: dict):
    print(f"错误：{error_msg}")
    print(f"阶段：{context.get('stage')}")
    # 发送通知、记录日志等

html = to_wechat(
    'article.md',
    on_error=error_handler,
    retry_count=2
)
```

### 3. 生成完整 HTML 文档

```python
html = to_wechat(
    'article.md',
    wrap_full_html=True  # 包含 <html>, <head>, <body> 等
)
```

### 4. 查看所有可用主题

```python
from mdnice import MarkdownConverter

# 文章主题
print("文章主题:", MarkdownConverter.AVAILABLE_THEMES)
print("主题名称:", MarkdownConverter.THEME_NAMES)

# 代码主题
print("代码主题:", MarkdownConverter.AVAILABLE_CODE_THEMES)
```

### 5. 组合多个高级选项

```python
from mdnice import MarkdownConverter
from mdnice.image_uploaders import create_wechat_uploader, WechatUploadType

# 创建图床上传器
uploader = create_wechat_uploader(
    app_id='wx123',
    app_secret='secret',
    upload_type=WechatUploadType.NEWS_IMAGE
)

# 创建转换器
converter = MarkdownConverter(
    headless=True,
    wait_timeout=60,
    retry_count=3,
    code_theme='monokai',
    mac_style=True,
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_token',
    image_uploader=uploader,
    clean_html=True
)

# 转换
html = converter.convert(
    markdown='article.md',
    theme='rose',
    platform='wechat',
    output_dir='output',
    wrap_full_html=True
)
```

---

## ❓ 常见问题

### Q1: Python 版本要求？

**A:** mdnice 0.0.3+ 需要 **Python 3.10 或更高版本**。

检查版本：
```bash
python --version  # 需要 >= 3.10
```

### Q2: 首次运行提示安装浏览器？

**A:** 正常现象。运行以下命令安装：

```bash
playwright install chromium
```

这会下载约 200MB 的 Chromium 浏览器，只需运行一次。

### Q3: 浏览器下载失败？

**A:** 可能的解决方案：

#### 方案 1: 使用代理

```bash
# Linux/macOS
export HTTPS_PROXY=http://your-proxy:port

# Windows (PowerShell)
$env:HTTPS_PROXY="http://your-proxy:port"

# 然后安装
playwright install chromium
```

#### 方案 2: 使用远程浏览器

```python
# 无需本地安装浏览器
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000'
)
```

### Q4: 如何查看 Playwright 浏览器位置？

```bash
# 查看已安装的浏览器
playwright show-browsers

# 默认位置：
# Windows: %USERPROFILE%\AppData\Local\ms-playwright
# Linux: ~/.cache/ms-playwright
# macOS: ~/Library/Caches/ms-playwright
```

### Q5: 图片上传失败怎么处理？

**A:** 图片上传失败不会影响整体转换，失败的图片会保持原样。建议：

```python
def safe_uploader(image_path: str) -> str:
    try:
        return upload(image_path)
    except Exception as e:
        print(f"上传失败: {e}")
        return image_path  # 失败返回原路径
```

### Q6: 支持哪些图片格式？

**A:** 支持常见图片格式：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`

### Q7: Windows 下路径问题？

**A:** 使用以下方式之一：

```python
# 原始字符串
html = to_wechat(r'D:\Documents\article.md')

# 正斜杠
html = to_wechat('D:/Documents/article.md')

# Path 对象（推荐）
from pathlib import Path
html = to_wechat(Path('D:/Documents/article.md'))
```

### Q8: 如何清除浏览器缓存？

```bash
# 卸载浏览器
playwright uninstall

# 重新安装
playwright install chromium
```

### Q9: 远程浏览器连接失败？

**A:** 检查清单：

1. 浏览器服务是否运行：`curl http://localhost:3000/`
2. WebSocket 端点是否正确
3. Token 是否有效（如果需要）
4. 网络连接和防火墙设置

### Q10: 如何禁用 HTML 清理？

```python
# 保留编辑器标记（如果需要）
html = to_wechat('article.md', clean_html=False)
```

---

## 📝 更新日志

### v0.0.3

**🎉 重大更新**

#### 新增功能

- ✨ **迁移到 Playwright** - 替代 Selenium，性能更好更稳定
  - 内置浏览器驱动，无需手动配置
  - 更快的执行速度
  - 更友好的 API
- ✨ **代码主题支持** - 新增 7 种代码高亮主题
  - `wechat`, `atom-one-dark`, `atom-one-light`
  - `monokai`, `github`, `vs2015`, `xcode`
- ✨ **Mac 风格代码块** - 可选的 macOS 风格装饰
- ✨ **远程浏览器支持** - 完美支持容器化部署
  - browserless（CDP 协议）
  - Playwright 官方远程浏览器
  - 自动检测连接类型
  - Token 认证支持
- ✨ **微信公众号图床** - 新增微信图床上传器
  - 临时素材、永久素材、图文消息图片
  - 自动 Token 管理和缓存
  - 支持服务器获取 Token
- ✨ **HTML 清理** - 自动移除编辑器标记
  - 移除 `data-tool="mdnice编辑器"`
  - 移除 `data-website` 等属性
  - 更简洁的 HTML 代码

#### 改进

- ⚡ **性能提升** - Playwright 比 Selenium 快 30%+
- 🛡️ **稳定性增强** - 更可靠的元素定位和操作
- 📝 **代码质量** - 消除所有类型检查警告
- 🎨 **用户体验** - 更友好的日志输出

#### 破坏性变更

- ⚠️ **Python 版本要求** - 从 3.8+ 提升到 **3.10+**
- ⚠️ **依赖变更** - 从 Selenium 迁移到 Playwright
- ⚠️ **安装步骤** - 需要运行 `playwright install chromium`

#### 迁移指南

从 v0.0.2 升级：

```bash
# 1. 检查 Python 版本
python --version  # 需要 >= 3.10

# 2. 升级 mdnice
pip install --upgrade mdnice

# 3. 安装 Playwright 浏览器
playwright install chromium

# 4. 代码无需修改（API 向后兼容）
```

### v0.0.2

#### 新增

- ✨ 图片自动上传功能
- ✨ 多图床支持（8 种）
- 🔧 便捷函数

### v0.0.1

**🎉 首次发布**

- ✨ 支持微信公众号、知乎、稀土掘金
- ✨ 20 种精美主题
- ✨ 批量转换功能

---

## 💖 打赏支持

如果这个项目对你有帮助，欢迎打赏支持！你的支持是我持续更新的动力 💪

<div align="center">

![打赏支持](https://s2.loli.net/2025/11/10/lQRcAvN3Lgxukqb.png)

**扫码打赏 | 支持作者 | 持续更新**

</div>

---

## 🙏 致谢

感谢以下开源项目：

- [markdown-nice](https://github.com/whaoa/markdown-nice) - 优秀的 Markdown 编辑器
- [Playwright](https://playwright.dev/) - 现代化的浏览器自动化框架
- [Poetry](https://python-poetry.org/) - Python 依赖管理工具

感谢所有贡献者和使用者的支持！⭐

---

## 📄 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。

---

<div align="center">

**Made with ❤️ by [xiaoqiang](https://github.com/xiaoqiangclub)**

**欢迎关注微信公众号：XiaoqiangClub**

[⬆ 回到顶部](#-mdnice)

</div>