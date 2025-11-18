<div align="center">

![mdnice](images/mdnice.jpg)

[![PyPI version](https://badge.fury.io/py/mdnice.svg)](https://badge.fury.io/py/mdnice) [![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://pypi.org/project/mdnice/) [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE) 

</div>



## 📖 目录

- [✨ 功能特性](#-功能特性)
- [🚀 快速开始](#-快速开始)
- [📦 安装](#-安装)
- [💡 使用文档](#-使用文档)
  - [基础用法](#基础用法)
  - [批量转换](#批量转换)
  - [自定义主题](#自定义主题)
  - [多平台转换](#多平台转换)
  - [图片上传](#图片上传)
- [🎨 主题列表](#-主题列表)
- [📚 API 参考](#-api-参考)
  - [平台专用函数](#平台专用函数)
  - [通用转换函数](#通用转换函数)
  - [核心类](#核心类)
- [⚙️ 配置选项](#️-配置选项)
- [🔧 高级用法](#-高级用法)
- [❓ 常见问题](#-常见问题)
- [💖 打赏支持](#-打赏支持)
- [📄 许可证](#-许可证)

---
# 📝 mdnice

> 将 Markdown 转换为微信公众号、知乎、稀土掘金支持的富文本格式

## ✨ 功能特性

### 🎯 核心功能

- ✅ **多平台支持** - 一键转换为微信公众号、知乎、稀土掘金格式
- ✅ **20+精美主题** - 内置20种精心设计的主题样式，随心选择
- ✅ **批量处理** - 支持批量转换多个 Markdown 文件
- ✅ **智能重试** - 网络故障自动重试机制，确保转换成功
- ✅ **完整样式** - 保留所有内联样式，确保格式完美还原
- ✅ **自定义编辑器** - 支持使用自定义部署的 markdown-nice 编辑器
- ✅ **图片自动上传** - 支持本地图片自动上传到图床 
- ✅ **零配置** - Selenium 自动管理 ChromeDriver，开箱即用 

### 🛡️ 稳定性保障

- 🔄 **自动容错** - 编辑器地址故障自动切换备用地址
- 🔄 **智能降级** - 多种HTML获取方案，确保转换成功
- 🔄 **错误通知** - 可自定义错误回调函数，实时掌握转换状态
- 🔄 **详细日志** - 实时输出转换进度和状态，方便调试
- 🔄 **驱动自动管理** - Selenium 4.6+ 自动下载和管理 ChromeDriver

### 📊 支持平台

| 平台 | 函数 | 说明 |
|------|------|------|
| 📱 微信公众号 | `to_wechat()` | 完美适配公众号编辑器，支持代码高亮 |
| 📘 知乎 | `to_zhihu()` | 适配知乎文章编辑器，保留样式 |
| 💎 稀土掘金 | `to_juejin()` | 适配掘金文章编辑器，专业美观 |

### 🎨 精选主题

内置 **20种** 精美主题，包括：

- 🌸 **蔷薇紫** (rose) - 优雅的紫色系
- 🖤 **极客黑** (geekBlack) - 程序员最爱
- 🔵 **科技蓝** (scienceBlue) - 科技感十足
- 🌿 **萌绿** (cuteGreen) - 清新自然
- 🎯 **前端之巅同款** (blueMountain) - 专业技术风格
- ... 更多主题等你探索

### 📤 图片上传功能

- 🖼️ **智能识别** - 自动识别本地图片、网络图片、DataURL
- 🎯 **灵活模式** - 支持3种上传模式（仅本地/仅网络/全部）
- 🔌 **易于集成** - 简单回调函数即可对接任何图床
- ⚡ **高效处理** - 批量上传，错误容错
- 🌐 **多图床支持** - 内置多种主流图床上传器（SM.MS、七牛云、阿里云OSS、GitHub等）

#### 支持的图床上传器

我们提供了多种图床上传器，可以直接使用：

| 图床名称 | 类名 | 特点 | 使用场景 |
|---------|------|----|---------|
| SM.MS | `SMUploader` | 免费，5MB限制 | 临时上传 |
| ImgURL | `ImgURLUploader` | 免费，10MB限制 | 免费图床 |
| 路过图床 | `LuoGuoUploader` | 免费，无需注册 | 快速上传 |
| 七牛云 | `QiniuUploader` | 10GB免费存储 | 长期存储 |
| 阿里云OSS | `AliyunOSSUploader` | 40GB免费存储 | 企业级 |
| 又拍云 | `UpyunUploader` | 10GB免费存储 | 稳定可靠 |
| GitHub | `GitHubUploader` | 完全免费，无限流量 | 技术博客 |
| 本地存储 | `LocalStorageUploader` | 保存到本地目录 | 本地预览 |

#### 便捷函数

为了简化使用，我们还提供了便捷函数：

- `create_smms_uploader()` - 创建 SM.MS 上传函数
- `create_qiniu_uploader()` - 创建七牛云上传函数
- `create_github_uploader()` - 创建 GitHub 上传函数
- `create_local_uploader()` - 创建本地存储上传函数

#### 在主函数中的调用方法

你可以通过以下方式使用图片上传功能：

```python
from mdnice import to_wechat, create_smms_uploader

# 方法1: 使用便捷函数
smms_uploader = create_smms_uploader(
    api_token='YOUR_TOKEN',
    api_domain='https://smms.app'  # 国内优化域名
)

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=smms_uploader,      # 传入上传函数
    image_upload_mode='local'          # 上传模式：local/remote/all
)

# 方法2: 使用具体的上传器类
from mdnice.image_uploaders import SMUploader

uploader = SMUploader(
    api_token='YOUR_TOKEN',
    api_domain='https://smms.app'
)

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=uploader.upload,    # 传入upload方法
    image_upload_mode='all'            # 上传所有图片
)

# 方法3: 自定义上传函数
def my_custom_uploader(image_path: str) -> str:
    """自定义上传逻辑"""
    # 你的上传代码
    return "https://your-cdn.com/image.jpg"

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=my_custom_uploader,
    image_upload_mode='remote'         # 只上传网络图片
)
```

#### 上传模式说明

- `local`: 只上传本地图片文件
- `remote`: 只上传网络图片（重新上传到你的图床）
- `all`: 上传所有类型的图片（本地+网络+DataURL）


### 📤 图片上传功能

- 🖼️ **智能识别** - 自动识别本地图片、网络图片、DataURL
- 🎯 **灵活模式** - 支持3种上传模式（仅本地/仅网络/全部）
- 🔌 **易于集成** - 简单回调函数即可对接任何图床
- ⚡ **高效处理** - 批量上传，错误容错
- 🌐 **多图床支持** - 内置多种主流图床上传器（SM.MS、七牛云、阿里云OSS、GitHub等）

#### 支持的图床上传器

我们提供了多种图床上传器，可以直接使用：

| 图床名称 | 类名 | 特点 | 使用场景 |
|---------|------|----|---------|
| SM.MS | `SMUploader` | 免费，5MB限制 | 临时上传 |
| ImgURL | `ImgURLUploader` | 免费，10MB限制 | 免费图床 |
| 路过图床 | `LuoGuoUploader` | 免费，无需注册 | 快速上传 |
| 七牛云 | `QiniuUploader` | 10GB免费存储 | 长期存储 |
| 阿里云OSS | `AliyunOSSUploader` | 40GB免费存储 | 企业级 |
| 又拍云 | `UpyunUploader` | 10GB免费存储 | 稳定可靠 |
| GitHub | `GitHubUploader` | 完全免费，无限流量 | 技术博客 |
| 本地存储 | `LocalStorageUploader` | 保存到本地目录 | 本地预览 |

#### 便捷函数

为了简化使用，我们还提供了便捷函数：

- `create_smms_uploader()` - 创建 SM.MS 上传函数
- `create_qiniu_uploader()` - 创建七牛云上传函数
- `create_github_uploader()` - 创建 GitHub 上传函数
- `create_local_uploader()` - 创建本地存储上传函数

#### 在主函数中的调用方法

你可以通过以下方式使用图片上传功能：

```python
from mdnice import to_wechat, create_smms_uploader

# 方法1: 使用便捷函数
smms_uploader = create_smms_uploader(
    api_token='YOUR_TOKEN',
    api_domain='https://smms.app'  # 国内优化域名
)

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=smms_uploader,      # 传入上传函数
    image_upload_mode='local'          # 上传模式：local/remote/all
)

# 方法2: 使用具体的上传器类
from mdnice.image_uploaders import SMUploader

uploader = SMUploader(
    api_token='YOUR_TOKEN',
    api_domain='https://smms.app'
)

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=uploader.upload,    # 传入upload方法
    image_upload_mode='all'            # 上传所有图片
)

# 方法3: 自定义上传函数
def my_custom_uploader(image_path: str) -> str:
    """自定义上传逻辑"""
    # 你的上传代码
    return "https://your-cdn.com/image.jpg"

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=my_custom_uploader,
    image_upload_mode='remote'         # 只上传网络图片
)
```

#### 上传模式说明

- `local`: 只上传本地图片文件
- `remote`: 只上传网络图片（重新上传到你的图床）
- `all`: 上传所有类型的图片（本地+网络+DataURL）


- 🖼️ **智能识别** - 自动识别本地图片、网络图片、DataURL
- 🎯 **灵活模式** - 支持3种上传模式（仅本地/仅网络/全部）
- 🔌 **易于集成** - 简单回调函数即可对接任何图床
- ⚡ **高效处理** - 批量上传，错误容错

---

## 🚀 快速开始

### 最简单的使用

```python
from mdnice import to_wechat

# 一行代码完成转换
html = to_wechat('article.md')
print(f"转换成功！HTML长度：{len(html)}")
```

> 💡 **首次运行提示**：Selenium 会自动下载匹配的 ChromeDriver（约几秒到几十秒），后续运行会直接使用缓存。

### 5分钟上手示例

```python
from mdnice import to_wechat, to_zhihu, to_juejin

# 示例1：转换为微信公众号格式
html = to_wechat(
    'article.md',
    theme='rose',              # 使用蔷薇紫主题
    output_dir='output/wechat' # 保存到指定目录
)

# 示例2：转换为知乎格式
html = to_zhihu(
    'article.md',
    theme='geekBlack',         # 极客黑主题
    output_dir='output/zhihu'
)

# 示例3：转换为掘金格式
html = to_juejin(
    'article.md',
    theme='scienceBlue',       # 科技蓝主题
    output_dir='output/juejin'
)

# 示例4：批量转换
to_wechat(
    ['article1.md', 'article2.md', 'article3.md'],
    theme='random',            # 随机主题
    output_dir='output'
)
```

### 图片上传示例 

```python
from mdnice import to_wechat

# 定义图片上传函数
def upload_image(image_path: str) -> str:
    """上传图片到图床，返回URL"""
    # 你的图床上传逻辑
    # ...
    return "https://your-cdn.com/image.png"

# 使用图片上传功能
html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=upload_image,      # 传入上传函数
    image_upload_mode='local'         # 只上传本地图片
)
```

---

## 📦 安装

### 环境要求

- **Python**: 3.8+
- **浏览器**: Chrome/Chromium（自动检测）
- **驱动**: 无需手动安装（Selenium 4.6+ 自动管理）✨

### 安装步骤

#### 快速安装（推荐）

```bash
pip install mdnice
```

**就这么简单！** 🎉 安装完成后即可使用，Selenium 会自动：
- ✅ 检测系统中的 Chrome 浏览器版本
- ✅ 下载匹配的 ChromeDriver
- ✅ 缓存到本地（后续使用无需重复下载）

#### 其他安装方式

```bash
# 使用 poetry
poetry add mdnice

# 从源码安装
git clone https://github.com/xiaoqiangclub/mdnice.git
cd mdnice
pip install -e .
# 或
poetry install
```

### 验证安装

```python
from mdnice import to_wechat, __version__

# 查看版本
print(f"mdnice 版本: {__version__}")

# 测试转换（首次运行会自动下载 ChromeDriver）
html = to_wechat("# 测试标题\n\n这是测试内容。")
print("✅ 安装成功！" if html else "❌ 安装失败")
```

**首次运行说明：**

运行时你可能会看到：

```
INFO: Selenium Manager: driver found in cache: /path/to/chromedriver
```

这表示 Selenium 正在自动管理驱动，完全正常！

### 可选配置

<details>
<summary>点击展开：特殊场景下的配置选项</summary>

#### 场景1：手动指定 ChromeDriver 路径

如果你需要使用特定版本的 ChromeDriver：

```python
from mdnice import MarkdownConverter

converter = MarkdownConverter(
    chromedriver_path='/path/to/chromedriver'  # 指定驱动路径
)
html = converter.convert('article.md')
```

#### 场景2：离线环境

1. **在有网络的机器上预下载驱动**：
   ```bash
   python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit()"
   ```

2. **复制缓存目录到离线机器**：
   - Windows: `C:\Users\<用户名>\.cache\selenium`
   - Linux/macOS: `~/.cache/selenium`

#### 场景3：使用 webdriver-manager

虽然不是必需的，但如果你喜欢更多控制：

```bash
pip install webdriver-manager
```

然后可以在代码中：

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

#### 场景4：网络受限环境

设置代理：

```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port

# 然后正常使用
python your_script.py
```

</details>

---

## 💡 使用文档

### 基础用法

#### 1. 转换单个文件

```python
from mdnice import to_wechat

# 转换 Markdown 文件
html = to_wechat('article.md', theme='rose')

# 保存为 HTML 文件
to_wechat(
    'article.md',
    theme='rose',
    output_dir='output'  # 会自动保存为 output/article_wechat.html
)
```

#### 2. 转换 Markdown 文本

```python
from mdnice import to_wechat

# 直接传入 Markdown 内容
markdown_text = """
# 标题

这是一段 **Markdown** 文本。

- 列表项1
- 列表项2
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

#### 1. 转换多个文件

```python
from mdnice import to_wechat

files = [
    'article1.md',
    'article2.md',
    'article3.md'
]

# 批量转换，每个文件随机选择主题
html_list = to_wechat(
    files,
    theme='random',
    output_dir='output/batch'
)

print(f"成功转换 {len(html_list)} 个文件")
```

#### 2. 从列表中随机主题

```python
from mdnice import to_wechat

# 从指定主题中随机选择
to_wechat(
    ['a.md', 'b.md', 'c.md'],
    theme=['rose', 'geekBlack', 'scienceBlue'],  # 从这3个主题中随机
    output_dir='output'
)
```

### 自定义主题

```python
from mdnice import to_wechat

# 方式1: 指定单个主题
html = to_wechat('article.md', theme='rose')

# 方式2: 完全随机
html = to_wechat('article.md', theme='random')
# 或
html = to_wechat('article.md', theme=None)

# 方式3: 从列表中随机
html = to_wechat(
    'article.md',
    theme=['rose', 'geekBlack', 'scienceBlue']
)
```

### 多平台转换

#### 一文多发

```python
from mdnice import to_wechat, to_zhihu, to_juejin

article = 'article.md'

# 转换为微信公众号格式
to_wechat(article, theme='rose', output_dir='output/wechat')

# 转换为知乎格式
to_zhihu(article, theme='geekBlack', output_dir='output/zhihu')

# 转换为掘金格式
to_juejin(article, theme='scienceBlue', output_dir='output/juejin')

print("✅ 已生成所有平台格式！")
```

#### 使用通用函数

```python
from mdnice import convert

article = 'article.md'

for platform in ['wechat', 'zhihu', 'juejin']:
    convert(
        article,
        platform=platform,
        theme='rose',
        output_dir=f'output/{platform}'
    )
    print(f"✅ {platform} 格式转换完成")
```

### 图片上传 
> mdnice 支持自动将图片上传到图床，并替换为图床链接，以适应不同平台的要求。你可以直接调用 [内置的图床上传器](#支持的图床上传器)，也可以自定义上传器。

#### 1. 上传本地图片

```python
from mdnice import to_wechat
from pathlib import Path

def upload_to_imagebed(image_path: str) -> str:
    """上传本地图片到图床"""
    # 读取图片
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 上传到图床（示例）
    # url = upload_to_sm_ms(image_data)
    # url = upload_to_qiniu(image_data)
    
    return f"https://cdn.example.com/{Path(image_path).name}"

html = to_wechat(
    'article.md',
    theme='rose',
    image_uploader=upload_to_imagebed,
    image_upload_mode='local'  # 只上传本地图片（默认）
)
```

#### 2. 上传网络图片

```python
import requests
from mdnice import to_wechat

def download_and_reupload(image_url: str) -> str:
    """下载网络图片并重新上传"""
    # 下载图片
    response = requests.get(image_url, timeout=10)
    image_data = response.content
    
    # 上传到自己的CDN
    # new_url = upload_to_my_cdn(image_data)
    
    return f"https://my-cdn.com/images/{hash(image_url)}.jpg"

html = to_wechat(
    'article.md',
    image_uploader=download_and_reupload,
    image_upload_mode='remote'  # 只上传网络图片
)
```

#### 3. 上传所有图片

```python
from mdnice import to_wechat

def universal_uploader(image: str) -> str:
    """通用上传器，处理所有类型图片"""
    import requests
    from pathlib import Path
    
    # 网络图片
    if image.startswith('http'):
        response = requests.get(image, timeout=10)
        image_data = response.content
        filename = f"remote_{hash(image)}.jpg"
    # 本地图片
    else:
        with open(image, 'rb') as f:
            image_data = f.read()
        filename = Path(image).name
    
    # 统一上传
    # url = upload_to_imagebed(image_data, filename)
    
    return f"https://img.example.com/{filename}"

html = to_wechat(
    'article.md',
    image_uploader=universal_uploader,
    image_upload_mode='all'  # 上传所有图片
)
```

---

## 🎨 主题列表

### 所有可用主题（20种）

| 主题代码 | 中文名称 | 风格描述 | 适用场景 |
|---------|---------|---------|---------|
| `normal` | 默认主题 | 简洁大方 | 通用文章 |
| `shanchui` | 山吹 | 温暖黄色调 | 温馨内容 |
| `rose` | 蔷薇紫 | 优雅紫色系 | 优质文章 ⭐ |
| `fullStackBlue` | 全栈蓝 | 专业蓝色调 | 技术文章 |
| `nightPurple` | 凝夜紫 | 深邃紫色 | 深度分析 |
| `cuteGreen` | 萌绿 | 清新绿色 | 轻松阅读 |
| `extremeBlack` | 极简黑 | 黑白极简 | 极简风格 ⭐|
| `orangeHeart` | 橙心 | 活力橙色 | 热情洋溢 |
| `ink` | 墨黑 | 中国风墨色 | 传统文化 |
| `purple` | 姹紫 | 鲜艳紫色 | 创意内容 |
| `green` | 绿意 | 自然绿色 | 生活分享 |
| `cyan` | 嫩青 | 清爽青色 | 清新文字 |
| `wechatFormat` | WeChat-Format | 微信官方风格 | 公众号文章 |
| `blueCyan` | 兰青 | 蓝青色调 | 文艺范儿 |
| `blueMountain` | 前端之巅同款 | 前端之巅风格 | 技术分享  |
| `geekBlack` | 极客黑 | 程序员最爱 | 技术博客 |
| `red` | 红绯 | 热情红色 | 重要通知 |
| `blue` | 蓝莹 | 清澈蓝色 | 专业内容 |
| `scienceBlue` | 科技蓝 | 科技感蓝色 | 科技文章 |
| `simple` | 简 | 极简主义 | 简约风格 |

### 主题预览

```python
from mdnice import MarkdownConverter

# 查看所有可用主题
print("可用主题：", MarkdownConverter.AVAILABLE_THEMES)
print("主题名称：", MarkdownConverter.THEME_NAMES)
```

---

## 📚 API 参考

### 平台专用函数

#### `to_wechat()` - 微信公众号

```python
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
) -> Union[str, List[str], Path, List[Path]]
```

**参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `markdown` | `str/Path/List` | **必需** | Markdown 内容或文件路径 |
| `theme` | `str/List/None` | `'normal'` | 主题名称、列表或 None（随机） |
| `output_dir` | `str/Path/None` | `None` | 输出目录 |
| `return_html` | `bool` | `True` | 是否返回 HTML 内容 |
| `headless` | `bool` | `True` | 是否使用无头模式 |
| `wrap_full_html` | `bool` | `False` | 是否包装为完整 HTML 文档 |
| `retry_count` | `int` | `1` | 失败重试次数 |
| `on_error` | `Callable/None` | `None` | 错误通知回调函数 |
| `editor_url` | `str/None` | `None` | 自定义编辑器网址 |
| `image_uploader` | `Callable/None` | `None` | 图片上传回调函数  |
| `image_upload_mode` | `str` | `'local'` | 图片上传模式  |

**图片上传模式：**

- `'local'`: 只上传本地图片（默认）
- `'remote'`: 只上传网络图片
- `'all'`: 上传所有图片（本地+网络+DataURL）

**示例：**

```python
from mdnice import to_wechat

# 基础用法
html = to_wechat('article.md')

# 完整参数
html = to_wechat(
    markdown='article.md',
    theme='rose',
    output_dir='output',
    return_html=True,
    headless=True,
    wrap_full_html=False,
    retry_count=2,
    editor_url=None,
    image_uploader=my_uploader,
    image_upload_mode='local'
)
```

#### `to_zhihu()` 和 `to_juejin()`

参数与 `to_wechat()` 完全相同。

### 通用转换函数

#### `convert()` - 通用转换

```python
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
) -> Union[str, List[str], Path, List[Path]]
```

**额外参数：**

- `platform`: 目标平台（'wechat', 'zhihu', 'juejin'）

### 核心类

#### `MarkdownConverter` - 转换器类

```python
class MarkdownConverter:
    def __init__(
        self,
        headless: bool = True,
        wait_timeout: int = 30,
        retry_count: int = 1,
        on_error: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        editor_url: Optional[str] = None,
        image_uploader: Optional[Callable[[str], str]] = None,
        image_upload_mode: ImageUploadMode = 'local',
        chromedriver_path: Optional[str] = None  # 
    )
```

**类属性：**

- `AVAILABLE_THEMES`: 所有可用主题列表（20个）
- `THEME_NAMES`: 主题中文名称字典
- `PLATFORM_CONFIG`: 平台配置信息

**新增参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `chromedriver_path` | `str/None` | `None` | 自定义 ChromeDriver 路径（可选） |

**示例：**

```python
from mdnice import MarkdownConverter

# 基础用法（自动管理驱动）
converter = MarkdownConverter(
    headless=False,
    wait_timeout=60,
    retry_count=2
)

# 高级用法（自定义驱动路径）
converter = MarkdownConverter(
    headless=False,
    chromedriver_path='/path/to/chromedriver'  # 使用特定版本驱动
)

# 执行转换
html = converter.convert(
    markdown='article.md',
    theme='rose',
    platform='wechat'
)
```

---

## ⚙️ 配置选项

### 完整参数列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `markdown` | `str/Path/List` | **必需** | Markdown 内容或文件路径 |
| `platform` | `str` | `'wechat'` | 目标平台 |
| `theme` | `str/List/None` | `'normal'` | 主题名称、列表或 None |
| `output_dir` | `str/Path/None` | `None` | 输出目录 |
| `return_html` | `bool` | `True` | 是否返回 HTML 内容 |
| `headless` | `bool` | `True` | 是否使用无头模式 |
| `wrap_full_html` | `bool` | `False` | 是否包装为完整 HTML |
| `retry_count` | `int` | `1` | 失败重试次数 |
| `wait_timeout` | `int` | `30` | 页面加载超时时间（秒） |
| `on_error` | `Callable/None` | `None` | 错误回调函数 |
| `editor_url` | `str/None` | `None` | 自定义编辑器网址 |
| `image_uploader` | `Callable/None` | `None` | 图片上传回调函数  |
| `image_upload_mode` | `str` | `'local'` | 图片上传模式  |
| `chromedriver_path` | `str/None` | `None` | 自定义 ChromeDriver 路径  |

### 图片上传模式详解 

| 模式 | 值 | 行为 |
|------|-----|------|
| 仅本地 | `'local'` | 只上传本地路径的图片，网络图片保持不变（默认） |
| 仅网络 | `'remote'` | 只上传网络URL图片，本地图片保持不变 |
| 全部 | `'all'` | 上传所有图片（本地+网络+DataURL） |

---

## 🔧 高级用法

### 1. 自定义编辑器地址

```python
from mdnice import to_wechat

# 使用自定义编辑器
html = to_wechat(
    'article.md',
    editor_url='https://your-domain.com/markdown-nice/'
)
```

**智能容错机制：**
1. 自定义地址 (`editor_url`)
2. 默认地址 (`https://xiaoqiangclub.github.io/md/`)
3. 备用地址 (`https://whaoa.github.io/markdown-nice/`)

### 2. 自定义 ChromeDriver 路径 

适用于需要使用特定版本驱动的场景：

```python
from mdnice import MarkdownConverter

# 方式1：使用转换器类
converter = MarkdownConverter(
    chromedriver_path='/path/to/chromedriver'
)
html = converter.convert('article.md')

# 方式2：查看驱动缓存位置
import platform
from pathlib import Path

if platform.system() == 'Windows':
    cache_dir = Path.home() / '.cache' / 'selenium'
elif platform.system() == 'Darwin':
    cache_dir = Path.home() / 'Library' / 'Caches' / 'selenium'
else:
    cache_dir = Path.home() / '.cache' / 'selenium'

print(f"ChromeDriver 缓存位置: {cache_dir}")
```

### 3. 错误通知回调

```python
from mdnice import to_wechat

def error_handler(error_msg: str, context: dict):
    """自定义错误处理"""
    print(f"❌ 错误：{error_msg}")
    print(f"📍 阶段：{context.get('stage')}")
    # 发送通知...

html = to_wechat(
    'article.md',
    on_error=error_handler,
    retry_count=2
)
```

### 4. 批量处理不同平台

```python
from mdnice import convert

files = ['article1.md', 'article2.md', 'article3.md']
platforms = ['wechat', 'zhihu', 'juejin']

for platform in platforms:
    convert(
        files,
        platform=platform,
        theme='rose',
        output_dir=f'output/{platform}',
        retry_count=2
    )
```

### 5. 图片上传高级用法 

```python
from mdnice import to_wechat
import requests

class ImageUploader:
    """图片上传器类"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.uploaded_count = 0
    
    def upload(self, image: str) -> str:
        """上传图片"""
        # 处理网络图片
        if image.startswith('http'):
            response = requests.get(image)
            data = response.content
        else:
            # 处理本地图片
            with open(image, 'rb') as f:
                data = f.read()
        
        # 上传到图床
        url = self._upload_to_cdn(data)
        self.uploaded_count += 1
        return url
    
    def _upload_to_cdn(self, data: bytes) -> str:
        """实际上传逻辑"""
        # ... 你的CDN上传代码 ...
        return "https://cdn.com/image.jpg"

# 使用
uploader = ImageUploader(api_token='YOUR_TOKEN')
html = to_wechat(
    'article.md',
    image_uploader=uploader.upload,
    image_upload_mode='all'
)
print(f"上传了 {uploader.uploaded_count} 张图片")
```

---

## ❓ 常见问题

### Q1: 首次运行很慢？

**A:** 这是正常现象。Selenium Manager 首次运行时会自动下载 ChromeDriver（约几秒到几十秒，取决于网络速度）。下载完成后会缓存到本地，后续运行会很快。

你会看到类似日志：

```
INFO: Selenium Manager: driver found in cache
```

### Q2: ChromeDriver 下载失败？

**A:** 可能的原因和解决方案：

#### 方案1：检查网络

```bash
# 测试网络连接
ping google.com
```

#### 方案2：使用代理

```bash
# Linux/macOS
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port

# Windows (PowerShell)
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
```

#### 方案3：手动下载驱动

```python
from mdnice import MarkdownConverter

# 下载驱动：https://chromedriver.chromium.org/
# 然后指定路径
converter = MarkdownConverter(
    chromedriver_path='/path/to/chromedriver'
)
html = converter.convert('article.md')
```

#### 方案4：使用 webdriver-manager

```bash
pip install webdriver-manager
```

然后它会帮你处理下载。

### Q3: 如何查看 ChromeDriver 缓存位置？

**A:** Selenium Manager 的缓存位置：

```python
import platform
from pathlib import Path

if platform.system() == 'Windows':
    cache = Path.home() / '.cache' / 'selenium'
elif platform.system() == 'Darwin':
    cache = Path.home() / 'Library' / 'Caches' / 'selenium'
else:
    cache = Path.home() / '.cache' / 'selenium'

print(f"缓存位置: {cache}")
```

### Q4: 离线环境如何使用？

**A:** 对于无法联网的环境：

1. **在有网络的机器上预下载**：
   ```bash
   python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit()"
   ```

2. **复制缓存目录到目标机器**：
   - Windows: `C:\Users\<用户名>\.cache\selenium`
   - Linux: `~/.cache/selenium`
   - macOS: `~/Library/Caches/selenium`

3. **或手动指定驱动路径**：
   ```python
   converter = MarkdownConverter(
       chromedriver_path='/path/to/chromedriver'
   )
   ```

### Q5: 清除驱动缓存

**A:** 如果遇到版本不匹配问题：

```python
import shutil
from pathlib import Path

cache_dir = Path.home() / '.cache' / 'selenium'
if cache_dir.exists():
    shutil.rmtree(cache_dir)
    print("✅ 缓存已清除，重新运行将自动下载匹配版本")
```

### Q6: 图片上传失败怎么处理？

**A:** 图片上传失败不会影响整体转换，失败的图片会保持原样。建议：

1. 检查上传函数是否正确
2. 验证图床API是否可用
3. 查看错误日志
4. 使用 `on_error` 回调获取详细错误信息

```python
def safe_uploader(image: str) -> str:
    try:
        # 上传逻辑
        return upload(image)
    except Exception as e:
        print(f"上传失败: {e}")
        return image  # 失败则返回原路径
```

### Q7: 支持哪些图片格式？

**A:** 支持以下格式：

- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.webp`
- `.svg`

### Q8: Windows 下路径问题？

**A:** 使用原始字符串或 Path 对象：

```python
# 方式1: 原始字符串
html = to_wechat(r'D:\Documents\article.md')

# 方式2: 正斜杠
html = to_wechat('D:/Documents/article.md')

# 方式3: Path 对象（推荐）
from pathlib import Path
html = to_wechat(Path('D:/Documents/article.md'))
```

### Q9: 如何部署自己的编辑器？

**A:** 参考 [markdown-nice 部署文档](https://github.com/whaoa/markdown-nice)：

```bash
git clone https://github.com/whaoa/markdown-nice.git
cd markdown-nice
npm install
npm run build
# 部署 build 目录到你的服务器
```

### Q10: 支持哪些 Markdown 语法？

**A:** 支持所有标准 Markdown 及扩展语法：

- ✅ 标题（H1-H6）
- ✅ **粗体**、*斜体*、~~删除线~~
- ✅ 列表（有序、无序、任务列表）
- ✅ 代码块（支持语法高亮）
- ✅ 引用、表格
- ✅ 图片、链接
- ✅ 数学公式（LaTeX）
- ✅ 脚注、目录

---

## 📝 更新日志

### v0.0.1 (2025-11-18)

**🎉 首次发布**

#### 新增

- ✨ 支持微信公众号、知乎、稀土掘金三大平台
- ✨ 内置20种精美主题
- ✨ 批量转换功能
- ✨ 智能重试机制
- ✨ 错误通知回调
- ✨ 自定义编辑器地址支持
- ✨ 智能地址切换机制（自定义→默认→备用）
- ✨ **图片自动上传功能** 
  - 支持本地图片上传
  - 支持网络图片重新上传
  - 支持3种上传模式（local/remote/all）
  - 自动识别图片类型（本地/网络/DataURL）
- ✨ **零配置驱动管理** 
  - Selenium 4.6+ 自动下载和管理 ChromeDriver
  - 支持自定义驱动路径（高级用户）
  - 友好的错误提示和故障排查
- ✨ 平台专用函数：`to_wechat()`, `to_zhihu()`, `to_juejin()`
- 📝 完整的类型注解
- 📝 中文文档和日志

#### 特性

- 🎨 20种主题随意切换
- 🔄 自动容错和降级
- 📤 灵活的图片上传策略
- 🌐 多编辑器地址支持
- 📦 批量处理能力
- ⚙️ 高度可配置
- 🚀 开箱即用，零配置

#### 技术栈

- Python 3.8+
- Selenium 4.6+（自动驱动管理）
- Type Hints（完整类型注解）
- Poetry（依赖管理）



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
- [Selenium](https://www.selenium.dev/) - 强大的浏览器自动化框架（4.6+ 自动驱动管理）
- [Poetry](https://python-poetry.org/) - 现代化的 Python 依赖管理工具

感谢所有贡献者和使用者的支持！⭐

---

## 📄 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。

<!-- 
---

## ⭐ Star History

如果这个项目对你有帮助，请给一个 Star ⭐️

[![Star History Chart](https://api.star-history.com/svg?repos=xiaoqiangclub/mdnice&type=Date)](https://star-history.com/#xiaoqiangclub/mdnice&Date)

---

<div align="center">

**Made with ❤️ by [xiaoqiang](https://github.com/xiaoqiangclub)**

**欢迎关注微信公众号：XiaoqiangClub**

[⬆ 回到顶部](#-mdnice)

</div>
 -->