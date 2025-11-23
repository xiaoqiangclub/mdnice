# mdnice - Markdown 多平台格式转换工具

<div align="center">

![mdnice](https://s2.loli.net/2025/11/18/xzuPwHCoDiET5r6.jpg)

[![PyPI version](https://img.shields.io/badge/PyPI-0.0.3-blue)](https://pypi.org/project/mdnice) [![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://pypi.org/project/mdnice/)
[![Downloads](https://pepy.tech/badge/mdnice)](https://pepy.tech/project/mdnice)



**一键将 Markdown 转换为微信公众号、知乎、稀土掘金等平台的富文本格式**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [安装](#-安装) • [使用文档](#-基础用法) • [API 参考](#-api-参考)

</div>


---

## ✨ 功能特性

### 🎨 多平台支持

| 平台 | 函数 | 说明 |
|------|------|------|
| 📱 微信公众号 | `to_wechat()` | 完美适配公众号编辑器 |
| 📘 知乎 | `to_zhihu()` | 适配知乎文章编辑器 |
| 💎 稀土掘金 | `to_juejin()` | 适配掘金文章编辑器 |

### 🎭 丰富主题

- **20+ 文章主题** - 蔷薇紫、极客黑、科技蓝等精美主题
- **7 种代码主题** - Atom One Dark、Monokai、GitHub 等
- **Mac 风格代码块** - 可选的 macOS 风格装饰（智能识别，避免重复操作）
- **随机主题** - 支持随机选择或从列表中随机

### 📤 图片自动上传

- 🖼️ **智能识别** - 自动识别本地图片、网络图片、Data URL
- 🎯 **灵活模式** - 支持 3 种上传模式（仅本地/仅网络/全部）
- 🔌 **易于集成** - 简单回调函数即可对接任何图床
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

### 🌐 网络代理（新增）

- 🔒 **HTTP/HTTPS 代理** - 支持标准 HTTP 代理
- 🚀 **SOCKS5 代理** - 支持 SOCKS5 协议
- 🔐 **代理认证** - 支持用户名/密码认证
- 🎯 **代理绕过** - 灵活的绕过规则配置
- 🌍 **跨平台支持** - 本地和远程浏览器均支持

### 🔧 远程浏览器

- 🐳 **Docker 容器环境** - 无需在容器中安装浏览器
- ☁️ **云函数/无服务器** - 完美适配 AWS Lambda、阿里云函数计算等
- 🔄 **共享浏览器服务** - 多实例共享，节省资源
- 💻 **资源受限环境** - 减少本地资源消耗
- 🔌 **灵活部署** - 支持 browserless 和 Playwright 官方远程浏览器

### 🛡️ 稳定可靠

- ✅ **CDP 协议支持** - 使用 Chrome DevTools Protocol 确保稳定性
- 🔄 **多层降级方案** - 5 种方案确保内容获取成功
- 🔁 **自动重试** - 失败自动重试，提高成功率
- 📋 **智能容错** - 多编辑器地址自动降级

---

## 🚀 快速开始

### 最简单的使用

```python
from mdnice import to_wechat

# 一行代码完成转换
html = to_wechat('article.md')
print(f"转换成功！HTML长度：{len(html)}")
```

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

## 💡 基础用法

### 1. 转换单个文件

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

### 2. 转换 Markdown 文本

```python
from mdnice import to_wechat

markdown_text = """
# 标题

这是 **Markdown** 文本。

```python
print("Hello World")
\u0060``
"""

html = to_wechat(markdown_text, theme='geekBlack')
```

### 3. 使用 Path 对象

```python
from pathlib import Path
from mdnice import to_wechat

file_path = Path('documents/article.md')
html = to_wechat(file_path, theme='scienceBlue')
```

### 4. 批量转换

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

### 5. 自定义主题

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

### 6. 多平台转换

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
| `orangeHeart` | 橙心 | 活力橙色 | 活力内容 |
| `ink` | 墨黑 | 水墨风格 | 文艺范 |
| `purple` | 姹紫 | 紫色系 | 时尚前沿 |
| `green` | 绿意 | 绿色系 | 清新自然 |
| `cyan` | 嫩青 | 青色系 | 小清新 |
| `wechatFormat` | WeChat-Format | 微信官方 | 公众号 |
| `blueCyan` | 兰青 | 蓝青色 | 专业严谨 |
| `red` | 红绯 | 红色系 | 热情洋溢 |
| `blue` | 蓝莹 | 蓝色系 | 沉稳大气 |
| `simple` | 简 | 极简风 | 简约主义 |

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

# 启用 Mac 风格（默认，智能识别避免重复操作）
html = to_wechat('article.md', mac_style=True)

# 禁用 Mac 风格
html = to_wechat('article.md', mac_style=False)
```

> 💡 **智能识别**：Mac 风格默认已启用，当 `mac_style=True` 时会检测当前状态，避免重复点击导致的状态切换。

---

## 📤 图片自动上传

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
    image_uploader=upload_image,
    image_upload_mode='local'  # 只上传本地图片
)
```

### 使用内置图床

#### 1. SM.MS 图床

```python
from mdnice import to_wechat, create_smms_uploader

# 创建上传器
uploader = create_smms_uploader(token='YOUR_SMMS_TOKEN')

# 使用
html = to_wechat(
    'article.md',
    image_uploader=uploader,
    image_upload_mode='all'  # 上传所有图片
)
```

#### 2. 微信公众号图床

```python
from mdnice import to_wechat, create_wechat_uploader, WechatUploadType

# 创建微信上传器
uploader = create_wechat_uploader(
    upload_type=WechatUploadType.NEWS_IMAGE,  # 图文消息图片（推荐）
    cookie='your_wechat_cookie'
)

html = to_wechat(
    'article.md',
    image_uploader=uploader,
    image_upload_mode='local'
)
```

**微信图床上传类型：**
- `WechatUploadType.TEMPORARY` - 临时素材（3天有效期）
- `WechatUploadType.PERMANENT` - 永久素材
- `WechatUploadType.NEWS_IMAGE` - 图文消息图片（推荐）✨

#### 3. 七牛云

```python
from mdnice import create_qiniu_uploader

uploader = create_qiniu_uploader(
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY',
    bucket_name='your-bucket',
    domain='https://cdn.example.com'
)
```

#### 4. GitHub 图床

```python
from mdnice import create_github_uploader

uploader = create_github_uploader(
    token='ghp_your_token',
    repo='username/image-repo',
    branch='main',
    path='images'
)
```

#### 5. 本地存储

```python
from mdnice import create_local_uploader

uploader = create_local_uploader(
    output_dir='images',
    url_prefix='https://example.com/images'
)
```

### 上传模式

| 模式 | 值 | 说明 |
|------|-----|------|
| 仅本地 | `'local'` | 只上传本地图片（默认） |
| 仅网络 | `'remote'` | 只上传网络图片 |
| 全部 | `'all'` | 上传所有图片 |

---

## 🌐 网络代理

mdnice 支持通过代理访问编辑器和上传图片，解决网络访问限制问题。

### 为什么需要代理？

- 🚫 **网络限制** - 编辑器地址访问受限
- 🖼️ **图床上传** - 某些图床需要代理访问
- 🌍 **跨境访问** - 访问国外资源
- 🔒 **企业环境** - 公司网络需要代理

### HTTP/HTTPS 代理

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    proxy={
        'server': 'http://127.0.0.1:7890'
    }
)
```

### SOCKS5 代理

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    proxy={
        'server': 'socks5://127.0.0.1:1080'
    }
)
```

### 需要认证的代理

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    proxy={
        'server': 'http://proxy.example.com:8080',
        'username': 'your_username',
        'password': 'your_password'
    }
)
```

### 代理绕过规则

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    proxy={
        'server': 'http://127.0.0.1:7890',
        'bypass': 'localhost,127.0.0.1,*.local,192.168.*'  # 这些地址不走代理
    }
)
```

### 常见代理工具端口

| 工具 | HTTP 端口 | SOCKS5 端口 |
|------|----------|------------|
| Clash | 7890 | 7891 |
| V2Ray | 10809 | 10808 |
| Shadowsocks | 1087 | 1080 |

### 远程浏览器 + 代理

```python
from mdnice import to_wechat

# 远程浏览器使用代理
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_token',
    proxy={
        'server': 'http://127.0.0.1:7890'
    },
    wait_timeout=60  # 使用代理建议增加超时
)
```

> ⚠️ **注意**：如果远程浏览器在 Docker 容器中，代理地址需使用 `host.docker.internal` 而不是 `127.0.0.1`

```python
# Docker 容器中的远程浏览器
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000',
    proxy={
        'server': 'http://host.docker.internal:7890'  # Docker 专用
    }
)
```

---

## 🔧 远程浏览器

mdnice 支持连接到远程浏览器服务，特别适用于容器化部署和云函数环境。

### 为什么使用远程浏览器？

- 🐳 **容器环境** - 无需在容器中安装浏览器
- ☁️ **云函数** - AWS Lambda、阿里云函数计算等
- 💰 **节省资源** - 多个实例共享一个浏览器
- ⚡ **更快启动** - 浏览器常驻，无需每次启动

### 使用 browserless（推荐）

#### 1. 启动 browserless

```bash
# 基础启动
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 带 Token 认证
docker run -p 3000:3000 \
  -e "TOKEN=your_secret_token" \
  ghcr.io/browserless/chromium
```

#### 2. 连接使用

```python
from mdnice import to_wechat

# 基础连接
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000'
)

# 带 Token 认证
html = to_wechat(
    'article.md',
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_secret_token'
)
```

### 使用 browserless.io 云服务

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    browser_ws_endpoint='wss://chrome.browserless.io',
    browser_token='YOUR_API_KEY',
    wait_timeout=60
)
```

### 自定义编辑器地址

mdnice 支持自定义编辑器地址，并提供多地址自动降级功能。

#### 单个地址

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    editor_url='https://your-domain.com/markdown-nice/'
)
```

#### 多地址降级（推荐）

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    editor_url=[
        'https://editor1.com',  # 优先使用
        'https://editor2.com',  # 第一个失败时使用
        'https://editor3.com'   # 第二个失败时使用
    ]
)
```

> 💡 **智能容错**：自定义地址失败后会自动降级到默认地址和备用地址，确保转换成功。

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
      - TOKEN=your_secret_token
    restart: unless-stopped
```

```bash
# 启动服务
docker-compose up -d

# 使用
python your_script.py
```

---

## 📚 API 参考

### 平台专用函数

#### `to_wechat()` / `to_zhihu()` / `to_juejin()`

```python
def to_wechat(
    markdown: Union[str, Path, List],
    theme: Union[str, List[str], None] = 'normal',
    code_theme: CodeTheme = 'atom-one-dark',
    mac_style: bool = True,
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
    browser_ws_endpoint: Optional[str] = None,
    browser_type: BrowserType = 'chromium',
    browser_connection_type: BrowserConnectionType = 'auto',
    browser_token: Optional[str] = None,
    proxy: Optional[Dict[str, str]] = None,
    clean_html: bool = True
) -> Union[str, List[str], Path, List[Path]]
```

### 参数说明

#### 核心参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `markdown` | `str/Path/List` | **必需** | Markdown 内容、文件路径或列表 |
| `theme` | `str/List/None` | `'normal'` | 文章主题（可选 `'random'` 或主题列表） |
| `code_theme` | `str` | `'atom-one-dark'` | 代码高亮主题 |
| `mac_style` | `bool` | `True` | 是否启用 Mac 风格代码块 |
| `output_dir` | `str/Path/None` | `None` | 输出目录（None 则不保存文件） |
| `return_html` | `bool` | `True` | 是否返回 HTML 内容 |
| `wrap_full_html` | `bool` | `False` | 是否包装为完整 HTML 文档 |
| `clean_html` | `bool` | `True` | 是否清理 HTML 中的编辑器标记 |

#### 浏览器参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `headless` | `bool` | `True` | 是否使用无头模式（远程浏览器时忽略） |
| `wait_timeout` | `int` | `30` | 等待超时时间（秒） |
| `retry_count` | `int` | `1` | 失败重试次数 |

#### 图片上传参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_uploader` | `Callable` | `None` | 图片上传函数 `(image_path: str) -> str` |
| `image_upload_mode` | `str` | `'local'` | 上传模式：`'local'`/`'remote'`/`'all'` |

#### 远程浏览器参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `browser_ws_endpoint` | `str` | `None` | WebSocket 端点（如 `ws://localhost:3000`） |
| `browser_type` | `str` | `'chromium'` | 浏览器类型：`'chromium'`/`'firefox'`/`'webkit'` |
| `browser_connection_type` | `str` | `'auto'` | 连接类型：`'auto'`/`'cdp'`/`'playwright'` |
| `browser_token` | `str` | `None` | 远程浏览器访问令牌 |

#### 网络代理参数（新增）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `proxy` | `dict` | `None` | 代理配置（见下方详细说明） |

**代理配置格式：**

```python
proxy = {
    'server': 'http://127.0.0.1:7890',  # 必需：代理服务器地址
    'username': 'user',                  # 可选：认证用户名
    'password': 'pass',                  # 可选：认证密码
    'bypass': 'localhost,*.local'        # 可选：绕过规则
}
```

#### 高级参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `editor_url` | `str/List` | `None` | 自定义编辑器地址（支持多地址降级） |
| `on_error` | `Callable` | `None` | 错误通知回调 `(error_msg: str, context: dict) -> None` |

### 通用转换函数

```python
from mdnice import convert

html = convert(
    markdown='article.md',
    platform='wechat',  # 或 'zhihu', 'juejin'
    theme='rose',
    # ... 其他参数与 to_wechat() 相同
)
```

### 核心类

```python
from mdnice import MarkdownConverter

# 创建转换器实例
converter = MarkdownConverter(
    headless=True,
    wait_timeout=30,
    retry_count=1,
    code_theme='monokai',
    mac_style=True,
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_token',
    proxy={'server': 'http://127.0.0.1:7890'},
    clean_html=True
)

# 转换
html = converter.convert(
    markdown='article.md',
    theme='rose',
    platform='wechat'
)
```

---

## 🔧 高级用法

### 1. 错误通知回调

```python
from mdnice import to_wechat

def error_handler(error_msg: str, context: dict):
    """自定义错误处理"""
    print(f"❌ 错误：{error_msg}")
    print(f"📍 阶段：{context.get('stage')}")
    print(f"📄 详情：{context}")
    
    # 发送通知、记录日志等
    # send_notification(error_msg)
    # logger.error(error_msg, extra=context)

html = to_wechat(
    'article.md',
    on_error=error_handler,
    retry_count=3  # 增加重试次数
)
```

### 2. 生成完整 HTML 文档

```python
from mdnice import to_wechat

html = to_wechat(
    'article.md',
    wrap_full_html=True  # 包含 <!DOCTYPE html>, <html>, <head>, <body> 等
)

# 生成的 HTML 可以直接在浏览器中打开
with open('article.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

### 3. 查看所有可用主题

```python
from mdnice import MarkdownConverter

# 文章主题
print("文章主题列表:")
for theme in MarkdownConverter.AVAILABLE_THEMES:
    print(f"  - {theme}: {MarkdownConverter.THEME_NAMES.get(theme, theme)}")

# 代码主题
print("\n代码主题列表:")
for theme in MarkdownConverter.AVAILABLE_CODE_THEMES:
    config = MarkdownConverter.CODE_THEME_CONFIG[theme]
    print(f"  - {theme}: {config['name']}")
```

### 4. 组合使用所有高级选项

```python
from mdnice import MarkdownConverter, create_wechat_uploader, WechatUploadType

# 创建图床上传器
uploader = create_wechat_uploader(
    upload_type=WechatUploadType.NEWS_IMAGE,
    cookie='your_wechat_cookie'
)

# 错误处理
def error_handler(msg, ctx):
    print(f"Error: {msg}")

# 创建转换器
converter = MarkdownConverter(
    headless=True,
    wait_timeout=60,
    retry_count=3,
    code_theme='monokai',
    mac_style=True,
    browser_ws_endpoint='ws://localhost:3000',
    browser_token='your_token',
    proxy={'server': 'http://127.0.0.1:7890'},
    image_uploader=uploader,
    image_upload_mode='all',
    editor_url=[
        'https://editor1.com',
        'https://editor2.com'
    ],
    on_error=error_handler,
    clean_html=True
)

# 批量转换
results = converter.convert(
    markdown=['a.md', 'b.md', 'c.md'],
    theme='random',
    platform='wechat',
    output_dir='output',
    wrap_full_html=True
)

print(f"成功转换 {len(results)} 个文件")
```

---

## ❓ 常见问题

### Q1: Python 版本要求？

**A:** mdnice 需要 **Python 3.10 或更高版本**。

```bash
# 检查版本
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

#### 方案 1: 使用代理下载

```bash
# Linux/macOS
export HTTPS_PROXY=http://127.0.0.1:7890
playwright install chromium

# Windows PowerShell
$env:HTTPS_PROXY="http://127.0.0.1:7890"
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

### Q4: 代理连接失败？

**A:** 检查清单：

```bash
# 1. 验证代理可用性
curl -x http://127.0.0.1:7890 http://httpbin.org/ip

# 2. 检查代理格式
# ✅ 正确：proxy = {'server': 'http://127.0.0.1:7890'}
# ❌ 错误：proxy = {'server': '127.0.0.1:7890'}  # 缺少协议

# 3. SOCKS5 代理格式
# ✅ 正确：proxy = {'server': 'socks5://127.0.0.1:1080'}
# ❌ 错误：proxy = {'server': 'socks://127.0.0.1:1080'}  # 应该是 socks5
```

### Q5: 远程浏览器连接失败？

**A:** 检查清单：

```bash
# 1. 检查浏览器服务是否运行
curl http://localhost:3000/

# 2. 如果使用 Docker
docker ps  # 检查容器是否运行
docker logs <container-id>  # 查看日志

# 3. 检查防火墙和网络
telnet localhost 3000
```

### Q6: 图片上传失败怎么处理？

**A:** 图片上传失败不会中断转换，失败的图片会保持原样。建议：

```python
def safe_uploader(image_path: str) -> str:
    """带容错的上传函数"""
    try:
        url = your_upload_function(image_path)
        print(f"✅ 上传成功: {url}")
        return url
    except Exception as e:
        print(f"⚠️ 上传失败: {e}，保持原路径")
        return image_path  # 失败返回原路径
```

### Q7: Windows 下路径问题？

**A:** 使用以下方式之一：

```python
# 方式 1: 原始字符串
html = to_wechat(r'D:\Documents\article.md')

# 方式 2: 正斜杠
html = to_wechat('D:/Documents/article.md')

# 方式 3: Path 对象（推荐）
from pathlib import Path
html = to_wechat(Path('D:/Documents/article.md'))
```

### Q8: Mac 风格代码块没有生效？

**A:** Mac 风格默认已启用，mdnice 会智能识别当前状态：

```python
# 默认已启用，设置为 True 时会检测状态，避免重复操作
html = to_wechat('article.md', mac_style=True)

# 如需禁用
html = to_wechat('article.md', mac_style=False)
```

### Q9: 如何查看详细的转换日志？

```python
from mdnice import to_wechat

# mdnice 会自动输出详细日志，包括：
# - 浏览器初始化状态
# - 页面加载进度
# - 主题选择
# - 图片上传状态
# - 内容获取方案
# - 错误信息和重试

html = to_wechat('article.md', headless=False)  # 显示浏览器窗口
```

### Q10: 超时问题如何解决？

```python
from mdnice import to_wechat

# 增加超时时间和重试次数
html = to_wechat(
    'article.md',
    wait_timeout=60,   # 增加到 60 秒
    retry_count=3      # 增加重试次数
)
```

---

## 📝 更新日志

### v0.0.3 (2025-01)

**🎉 重大更新**

#### 新增功能

- ✨ **迁移到 Playwright** - 替代 Selenium，性能提升 30%+
  - 内置浏览器驱动，无需手动配置
  - 更稳定的元素定位和操作
  - 更友好的 API
- ✨ **代码主题支持** - 新增 7 种代码高亮主题
- ✨ **Mac 风格代码块** - 可选的 macOS 风格装饰，智能识别当前状态
- ✨ **远程浏览器支持** - 完美支持容器化部署
  - browserless（CDP 协议）
  - Playwright 官方远程浏览器
  - 自动检测连接类型
  - Token 认证支持
- ✨ **网络代理支持**（新增） - 解决网络访问限制
  - HTTP/HTTPS 代理
  - SOCKS5 代理
  - 代理认证
  - 代理绕过规则
- ✨ **多编辑器地址支持**（新增） - 智能降级
  - 支持字符串或列表
  - 自动降级到默认和备用地址
- ✨ **CDP 协议支持**（新增） - 确保内容获取稳定性
  - 使用 Chrome DevTools Protocol
  - 5 层降级方案
  - 剪贴板权限授予
- ✨ **微信公众号图床** - 新增微信图床上传器
  - 临时素材、永久素材、图文消息图片
  - 自动 Token 管理和缓存
- ✨ **HTML 清理** - 自动移除编辑器标记
  - 移除 `data-tool="mdnice编辑器"`
  - 移除 `data-website` 等属性

#### 改进

- ⚡ **性能提升** - Playwright 比 Selenium 快 30%+
- 🛡️ **稳定性增强** - 多层降级方案确保成功
- 🔧 **远程浏览器优化** - 智能使用现有页面，避免创建冲突
- 📝 **代码质量** - 消除所有类型检查警告
- 🎨 **用户体验** - 更友好的日志输出和错误提示

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

- [markdown-nice](https://github.com/mdnice/markdown-nice) - 优秀的 Markdown 编辑器
- [Playwright](https://playwright.dev/) - 现代化的浏览器自动化框架
- [Poetry](https://python-poetry.org/) - Python 依赖管理工具

感谢所有贡献者和使用者的支持！⭐

---

## 📄 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。

---

<div align="center">

**Made with ❤️ by [Xiaoqiang](https://github.com/xiaoqiangclub)**

**欢迎关注微信公众号：XiaoqiangClub**

[⬆ 回到顶部](#mdnice---markdown-多平台格式转换工具)

</div>