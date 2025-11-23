# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：图床上传工具集合 提供常见图床的上传接口实现
# 文件路径：mdnice/image_uploaders.py

"""
支持的图床：
- SM.MS (免费，5MB限制)
- ImgURL (免费)
- 路过图床 (免费)
- 七牛云 (需要账号)
- 阿里云 OSS (需要账号)
- 又拍云 (需要账号)
- GitHub (作为图床)
- 本地存储
- 微信公众号
"""

import os
import json
import base64
import hashlib
import requests
import tempfile
from pathlib import Path
from typing import Optional, Union, Tuple
from datetime import datetime
from enum import Enum
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    Image = None  # 部分功能需要 Pillow


# ============================================================================
# 类型定义
# ============================================================================

class WechatUploadType(Enum):
    """微信上传类型枚举"""
    TEMPORARY = "temporary"  # 临时素材（3天有效期）
    PERMANENT = "permanent"  # 永久素材
    NEWS_IMAGE = "news_image"  # 图文消息图片


# ============================================================================
# 辅助函数
# ============================================================================

def _image_to_bytes(image: Union[str, bytes, 'Image.Image'], format: str = 'JPEG') -> Tuple[bytes, str]:
    """
    将各种图片输入转换为字节数据

    :param image: 图片输入（路径、URL、bytes、PIL.Image等）
    :param format: 输出格式（JPEG、PNG等）
    :return: (图片字节数据, 文件名)
    """
    file_data = b''

    try:
        # 处理 PIL.Image 对象
        if Image and isinstance(image, Image.Image):
            output = BytesIO()
            # 处理透明通道
            if image.mode in ('RGBA', 'LA', 'P') and format.upper() == 'JPEG':
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                background.save(output, format=format, quality=95)
            else:
                image.save(output, format=format, quality=95)
            file_data = output.getvalue()
            filename = f'image.{format.lower()}'
            return file_data, filename

        # 处理字节数据
        elif isinstance(image, bytes):
            file_data = image
            filename = f'image.{format.lower()}'
            return file_data, filename

        # 处理字符串（路径或URL或Base64）
        elif isinstance(image, str):
            # Base64 编码（data:image/... 格式）
            if image.startswith('data:image/'):
                header, data = image.split(',', 1)
                file_data = base64.b64decode(data)
                # 从 header 提取格式
                if 'jpeg' in header or 'jpg' in header:
                    ext = 'jpg'
                elif 'png' in header:
                    ext = 'png'
                elif 'gif' in header:
                    ext = 'gif'
                else:
                    ext = format.lower()
                filename = f'image.{ext}'
                return file_data, filename

            # 纯 Base64 编码
            elif len(image) > 100 and not image.startswith(('http://', 'https://', '/')):
                try:
                    file_data = base64.b64decode(image)
                    filename = f'image.{format.lower()}'
                    return file_data, filename
                except:
                    pass

            # 网络图片 URL
            if image.startswith(('http://', 'https://')):
                response = requests.get(image, timeout=10)
                response.raise_for_status()
                file_data = response.content
                # 尝试从 URL 获取文件名
                filename = image.split('/')[-1].split('?')[0]
                if '.' not in filename:
                    filename = f'remote_{hash(image)}.jpg'
                return file_data, filename

            # 本地文件路径
            else:
                with open(image, 'rb') as f:
                    file_data = f.read()
                filename = Path(image).name
                return file_data, filename

        else:
            raise ValueError(f"不支持的图片类型: {type(image)}")

    except Exception as e:
        raise ValueError(f"图片转换失败: {e}")


# ============================================================================
# 免费图床
# ============================================================================

class SMUploader:
    """
    SM.MS 图床上传器

    官网：https://sm.ms/
    国内优化：https://smms.app/

    特点：
    - 免费使用
    - 单个文件最大 5MB
    - 需要注册获取 API Token
    - 国内访问较快

    获取 Token：https://sm.ms/home/apitoken
    国内获取 Token：https://smms.app/home/apitoken
    """

    def __init__(self,
                 api_token: Optional[str] = None,
                 api_domain: str = 'https://smms.app') -> None:
        """
        初始化上传器

        :param api_token: SM.MS API Token（可选，但建议提供以提高配额）
        :param api_domain: API 域名（默认 https://smms.app，也可使用 https://sm.ms）
        """
        self.api_domain = api_domain.rstrip('/')
        self.api_url = f'{self.api_domain}/api/v2/upload'
        self.api_token = api_token
        self.history_url = f'{self.api_domain}/api/v2/upload_history'

        # 提示使用的域名
        domain_name = 'smms.app (国内优化)' if 'smms.app' in self.api_domain else 'sm.ms (国际)'
        print(f"  ℹ️ SM.MS 使用域名: {domain_name}")

    def upload(self, image_path: str) -> str:
        """
        上传图片到 SM.MS

        :param image_path: 图片路径（本地路径或URL）
        :return: 图床URL
        """
        # 初始化变量（避免类型检查警告）
        file_data = b''

        try:
            # 处理网络图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                # 处理本地图片
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 检查文件大小（SM.MS 限制 5MB）
            if len(file_data) > 5 * 1024 * 1024:
                raise ValueError(
                    f"文件大小超过 5MB: {len(file_data) / 1024 / 1024:.2f}MB")

            # 准备上传
            files = {'smfile': (filename, file_data)}
            headers = {}

            if self.api_token:
                headers['Authorization'] = self.api_token

            # 上传
            response = requests.post(
                self.api_url,
                files=files,
                headers=headers,
                timeout=30
            )

            result = response.json()

            # 处理结果
            if result.get('success'):
                url = result['data']['url']
                print(f"  ✅ SM.MS 上传成功: {url}")
                return url
            elif result.get('code') == 'image_repeated':
                # 图片已存在
                url = result['images']
                print(f"  ℹ️ 图片已存在: {url}")
                return url
            else:
                error_msg = result.get('message', '未知错误')
                raise Exception(f"SM.MS 上传失败: {error_msg}")

        except Exception as e:
            print(f"  ❌ SM.MS 上传失败: {e}")
            raise


class ImgURLUploader:
    """
    ImgURL 图床上传器

    官网：https://www.imgurl.org/
    特点：
    - 免费使用
    - 单个文件最大 10MB
    - 需要注册获取 API Token
    - 支持相册管理

    获取 Token：https://www.imgurl.org/vip/manage/api
    """

    def __init__(self, api_token: str, api_uid: str):
        """
        初始化上传器

        :param api_token: ImgURL API Token
        :param api_uid: ImgURL 用户 UID
        """
        self.api_url = 'https://www.imgurl.org/api/v2/upload'
        self.api_token = api_token
        self.api_uid = api_uid

    def upload(self, image_path: str) -> str:
        """
        上传图片到 ImgURL

        :param image_path: 图片路径
        :return: 图床URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()

            # 检查文件大小
            if len(file_data) > 10 * 1024 * 1024:
                raise ValueError(f"文件大小超过 10MB")

            # Base64 编码
            image_base64 = base64.b64encode(file_data).decode('utf-8')

            # 上传
            data = {
                'uid': self.api_uid,
                'token': self.api_token,
                'image': image_base64
            }

            response = requests.post(self.api_url, data=data, timeout=30)
            result = response.json()

            if result.get('code') == 200:
                url = result['data']['url']
                print(f"  ✅ ImgURL 上传成功: {url}")
                return url
            else:
                error_msg = result.get('msg', '未知错误')
                raise Exception(f"ImgURL 上传失败: {error_msg}")

        except Exception as e:
            print(f"  ❌ ImgURL 上传失败: {e}")
            raise


class LuoGuoUploader:
    """
    路过图床上传器

    官网：https://imgtu.com/
    特点：
    - 免费使用
    - 单个文件最大 10MB
    - 无需注册即可使用
    - 国内访问快
    """

    def __init__(self):
        """初始化上传器"""
        self.api_url = 'https://imgtu.com/api/v1/upload'

    def upload(self, image_path: str) -> str:
        """
        上传图片到路过图床

        :param image_path: 图片路径
        :return: 图床URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 上传
            files = {'source': (filename, file_data)}

            response = requests.post(
                self.api_url,
                files=files,
                timeout=30
            )

            result = response.json()

            if result.get('status_code') == 200:
                url = result['image']['url']
                print(f"  ✅ 路过图床上传成功: {url}")
                return url
            else:
                error_msg = result.get('error', {}).get('message', '未知错误')
                raise Exception(f"路过图床上传失败: {error_msg}")

        except Exception as e:
            print(f"  ❌ 路过图床上传失败: {e}")
            raise


# ============================================================================
# 云服务商图床
# ============================================================================

class QiniuUploader:
    """
    七牛云上传器

    官网：https://www.qiniu.com/
    特点：
    - 10GB 免费存储
    - 10GB/月 免费流量
    - 稳定可靠
    - 需要实名认证

    依赖：pip install qiniu
    """

    def __init__(self, access_key: str, secret_key: str, bucket: str, domain: str):
        """
        初始化上传器

        :param access_key: 七牛云 AccessKey
        :param secret_key: 七牛云 SecretKey
        :param bucket: 存储空间名称
        :param domain: CDN 域名（需要自己配置）
        """
        try:
            from qiniu import Auth, put_data
            self.auth = Auth(access_key, secret_key)
            self.bucket = bucket
            self.domain = domain
            self.put_data = put_data
        except ImportError:
            raise ImportError("请先安装七牛云SDK: pip install qiniu")

    def upload(self, image_path: str) -> str:
        """
        上传图片到七牛云

        :param image_path: 图片路径
        :return: CDN URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 生成唯一文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            key = f"images/{timestamp}_{file_hash}_{filename}"

            # 生成上传凭证
            token = self.auth.upload_token(self.bucket, key)

            # 上传
            ret, info = self.put_data(token, key, file_data)

            if info.status_code == 200:
                url = f"http://{self.domain}/{key}"
                print(f"  ✅ 七牛云上传成功: {url}")
                return url
            else:
                raise Exception(f"七牛云上传失败: {info}")

        except Exception as e:
            print(f"  ❌ 七牛云上传失败: {e}")
            raise


class AliyunOSSUploader:
    """
    阿里云 OSS 上传器

    官网：https://www.aliyun.com/product/oss
    特点：
    - 40GB 免费存储（6个月）
    - 10GB/月 免费流量
    - 大厂服务，稳定可靠

    依赖：pip install oss2
    """

    def __init__(self, access_key_id: str, access_key_secret: str,
                 endpoint: str, bucket_name: str):
        """
        初始化上传器

        :param access_key_id: AccessKey ID
        :param access_key_secret: AccessKey Secret
        :param endpoint: Endpoint（如 oss-cn-hangzhou.aliyuncs.com）
        :param bucket_name: Bucket 名称
        """
        try:
            import oss2
            auth = oss2.Auth(access_key_id, access_key_secret)
            self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
            self.endpoint = endpoint
            self.bucket_name = bucket_name
        except ImportError:
            raise ImportError("请先安装阿里云OSS SDK: pip install oss2")

    def upload(self, image_path: str) -> str:
        """
        上传图片到阿里云 OSS

        :param image_path: 图片路径
        :return: CDN URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 生成对象名
            timestamp = datetime.now().strftime('%Y%m%d/%H%M%S')
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            object_name = f"images/{timestamp}_{file_hash}_{filename}"

            # 上传
            result = self.bucket.put_object(object_name, file_data)

            if result.status == 200:
                # 生成URL（这里使用外网访问地址）
                url = f"https://{self.bucket_name}.{self.endpoint}/{object_name}"
                print(f"  ✅ 阿里云OSS上传成功: {url}")
                return url
            else:
                raise Exception(f"阿里云OSS上传失败: {result}")

        except Exception as e:
            print(f"  ❌ 阿里云OSS上传失败: {e}")
            raise


class UpyunUploader:
    """
    又拍云上传器

    官网：https://www.upyun.com/
    特点：
    - 10GB 免费存储
    - 15GB/月 免费流量
    - 国内访问快

    依赖：pip install upyun
    """

    def __init__(self, bucket: str, username: str, password: str, domain: str):
        """
        初始化上传器

        :param bucket: 服务名称
        :param username: 操作员账号
        :param password: 操作员密码
        :param domain: 加速域名
        """
        try:
            import upyun
            self.up = upyun.UpYun(bucket, username, password, timeout=30)
            self.domain = domain
        except ImportError:
            raise ImportError("请先安装又拍云SDK: pip install upyun")

    def upload(self, image_path: str) -> str:
        """
        上传图片到又拍云

        :param image_path: 图片路径
        :return: CDN URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 生成路径
            timestamp = datetime.now().strftime('%Y%m%d/%H%M%S')
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            remote_path = f"/images/{timestamp}_{file_hash}_{filename}"

            # 上传
            result = self.up.put(remote_path, file_data)

            if result:
                url = f"http://{self.domain}{remote_path}"
                print(f"  ✅ 又拍云上传成功: {url}")
                return url
            else:
                raise Exception("又拍云上传失败")

        except Exception as e:
            print(f"  ❌ 又拍云上传失败: {e}")
            raise


# ============================================================================
# 特殊图床
# ============================================================================

class GitHubUploader:
    """
    GitHub 作为图床

    特点：
    - 完全免费
    - 不限流量
    - 需要 GitHub 账号
    - 国内访问可能较慢（可配合 CDN）

    推荐配合 jsdelivr CDN 使用
    """

    def __init__(self, token: str, repo: str, branch: str = 'main',
                 use_jsdelivr: bool = True):
        """
        初始化上传器

        :param token: GitHub Personal Access Token
        :param repo: 仓库名（格式：username/repo）
        :param branch: 分支名
        :param use_jsdelivr: 是否使用 jsdelivr CDN
        """
        self.api_url = 'https://api.github.com/repos'
        self.token = token
        self.repo = repo
        self.branch = branch
        self.use_jsdelivr = use_jsdelivr

    def upload(self, image_path: str) -> str:
        """
        上传图片到 GitHub

        :param image_path: 图片路径
        :return: 图片URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # Base64 编码
            content_base64 = base64.b64encode(file_data).decode('utf-8')

            # 生成路径
            timestamp = datetime.now().strftime('%Y%m%d')
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            path = f"images/{timestamp}/{file_hash}_{filename}"

            # 上传
            url = f"{self.api_url}/{self.repo}/contents/{path}"
            headers = {
                'Authorization': f'token {self.token}',
                'Content-Type': 'application/json'
            }
            data = {
                'message': f'Upload {filename}',
                'content': content_base64,
                'branch': self.branch
            }

            response = requests.put(
                url, json=data, headers=headers, timeout=30)
            result = response.json()

            if response.status_code == 201:
                # 使用 jsdelivr CDN
                if self.use_jsdelivr:
                    cdn_url = f"https://cdn.jsdelivr.net/gh/{self.repo}@{self.branch}/{path}"
                    print(f"  ✅ GitHub上传成功（jsdelivr CDN）: {cdn_url}")
                    return cdn_url
                else:
                    raw_url = result['content']['download_url']
                    print(f"  ✅ GitHub上传成功: {raw_url}")
                    return raw_url
            else:
                error_msg = result.get('message', '未知错误')
                raise Exception(f"GitHub上传失败: {error_msg}")

        except Exception as e:
            print(f"  ❌ GitHub上传失败: {e}")
            raise


class LocalStorageUploader:
    """
    本地存储上传器（复制到本地目录）

    适用场景：
    - 本地预览
    - 静态网站部署
    - 自己搭建的服务器
    """

    def __init__(self, storage_dir: str, base_url: str):
        """
        初始化上传器

        :param storage_dir: 本地存储目录
        :param base_url: 访问的基础URL
        """
        self.storage_dir = Path(storage_dir)
        self.base_url = base_url.rstrip('/')

        # 创建目录
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, image_path: str) -> str:
        """
        复制图片到本地目录

        :param image_path: 图片路径
        :return: 访问URL
        """
        # 初始化变量
        file_data = b''

        try:
            # 读取图片
            if image_path.startswith('http'):
                response = requests.get(image_path, timeout=10)
                file_data = response.content
                filename = f"remote_{hash(image_path)}.jpg"
            else:
                with open(image_path, 'rb') as f:
                    file_data = f.read()
                filename = Path(image_path).name

            # 生成保存路径
            timestamp = datetime.now().strftime('%Y%m%d')
            file_hash = hashlib.md5(file_data).hexdigest()[:8]

            # 创建日期目录
            date_dir = self.storage_dir / timestamp
            date_dir.mkdir(exist_ok=True)

            # 保存文件
            save_path = date_dir / f"{file_hash}_{filename}"
            with open(save_path, 'wb') as f:
                f.write(file_data)

            # 生成URL
            relative_path = f"{timestamp}/{file_hash}_{filename}"
            url = f"{self.base_url}/{relative_path}"

            print(f"  ✅ 本地存储成功: {save_path}")
            return url

        except Exception as e:
            print(f"  ❌ 本地存储失败: {e}")
            raise


class WechatUploader:
    """
    微信公众号图床上传器

    官网：https://mp.weixin.qq.com/
    文档：https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html

    支持三种上传方式：
    1. 临时素材（默认）：有效期3天，返回 media_id
       API: https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html

    2. 永久素材：永久保存，返回 media_id 和 url
       API: https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html

    3. 图文消息图片：用于图文消息内容，返回 url
       API: https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html

    支持两种 Token 获取方式（自动选择）：
    - 方式1：使用 app_id + app_secret 直接获取（需要IP在白名单）
    - 方式2：从服务器获取（适用于IP白名单限制的场景）

    特点：
    - 🔐 需要公众号认证
    - 📦 临时素材：图片大小限制 2MB
    - 📦 永久素材：图片大小限制 10MB
    - 📦 图文图片：图片大小限制 1MB
    - 📝 支持 JPG、PNG、GIF 格式
    - ⏰ 临时素材有效期 3 天
    - 💾 永久素材数量限制 100000 个

    依赖：pip install Pillow
    """

    # API 端点
    TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    UPLOAD_TEMP_URL = "https://api.weixin.qq.com/cgi-bin/media/upload"
    UPLOAD_PERMANENT_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    UPLOAD_NEWS_IMAGE_URL = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"

    # Token 缓存过期时间（提前5分钟刷新）
    TOKEN_EXPIRE_MARGIN = 300

    def __init__(
            self,
            app_id: str,
            app_secret: str,
            upload_type: WechatUploadType = WechatUploadType.NEWS_IMAGE,
            access_token_file: Optional[str] = None,
            server_url: Optional[str] = None,
            server_token: Optional[str] = None,
            verbose: bool = True,
            proxies: Optional[dict] = None,
    ):
        """
        初始化微信公众号图床上传器

        :param app_id: 公众号 AppID（必需）
        :param app_secret: 公众号 AppSecret（必需）
        :param upload_type: 上传类型（TEMPORARY/PERMANENT/NEWS_IMAGE），默认 TEMPORARY
        :param access_token_file: access_token 缓存文件路径，默认保存在系统临时目录
        :param server_url: 从服务器获取 access_token 的 URL（可选）
        :param server_token: 服务器认证令牌（可选）
        :param verbose: 是否显示详细日志
        :param proxies: 代理配置
        """
        if not Image:
            raise ImportError("微信上传器需要 Pillow: pip install Pillow")

        # 保存配置
        self.app_id = app_id
        self.app_secret = app_secret
        self.upload_type = upload_type
        self.verbose = verbose
        self.proxies = proxies

        # 服务器获取 token 配置
        self.server_url = server_url
        self.server_token = server_token

        # 设置 token 缓存文件路径
        if access_token_file:
            self.access_token_file = access_token_file
        else:
            # 默认保存在系统临时目录
            temp_dir = tempfile.gettempdir()
            cache_name = f"wechat_upload_token_{self.app_id}.json"
            self.access_token_file = os.path.join(temp_dir, cache_name)

        # Token 缓存
        self._access_token = None
        self._token_expires_at = 0

    def upload(self, image) -> str:
        """
        上传图片到微信公众号

        :param image: 图片输入，支持：
                     - PIL.Image.Image 对象
                     - 本地文件路径 (str)
                     - 网络图片 URL (str, http/https)
                     - Base64 编码 (str, data:image/... 或纯 Base64)
                     - 图片字节流 (bytes)
        :return: media_id 或 url（根据上传类型）
        """
        try:
            # 获取 access_token
            access_token = self._get_access_token()
            if not access_token:
                raise Exception("❌ 获取 access_token 失败")

            # 使用 _image_to_bytes 函数转换图片
            file_data, filename = _image_to_bytes(image, format='JPEG')

            # 根据上传类型检查文件大小
            max_size_mb = self._get_max_size()
            file_size_mb = len(file_data) / 1024 / 1024
            if file_size_mb > max_size_mb:
                raise ValueError(
                    f"❌ 文件大小超过 {max_size_mb}MB 限制: {file_size_mb:.2f}MB")

            # 确保图片格式符合微信要求
            file_data, filename = self._ensure_valid_format(file_data, filename)

            # 根据上传类型选择不同的上传方式
            if self.upload_type == WechatUploadType.TEMPORARY:
                return self._upload_temporary(access_token, file_data, filename)
            elif self.upload_type == WechatUploadType.PERMANENT:
                return self._upload_permanent(access_token, file_data, filename)
            elif self.upload_type == WechatUploadType.NEWS_IMAGE:
                return self._upload_news_image(access_token, file_data, filename)
            else:
                raise ValueError(f"❌ 不支持的上传类型: {self.upload_type}")

        except Exception as e:
            if self.verbose:
                print(f"  ❌ 微信图片上传失败: {e}")
            raise

    def _get_max_size(self) -> int:
        """获取不同上传类型的最大文件大小限制（MB）"""
        if self.upload_type == WechatUploadType.TEMPORARY:
            return 2  # 临时素材 2MB
        elif self.upload_type == WechatUploadType.PERMANENT:
            return 10  # 永久素材 10MB
        elif self.upload_type == WechatUploadType.NEWS_IMAGE:
            return 1  # 图文消息图片 1MB
        return 2

    def _ensure_valid_format(self, file_data: bytes, filename: str) -> tuple:
        """确保图片格式符合微信要求（只支持 JPG、PNG、GIF）"""
        try:
            img_buffer = BytesIO(file_data)
            img = Image.open(img_buffer)

            # 获取或转换图片格式
            img_format = img.format if img.format else 'JPEG'

            if img_format.upper() not in ['JPEG', 'JPG', 'PNG', 'GIF']:
                # 转换为 JPEG
                if self.verbose:
                    print(f"  ℹ️  将 {img_format} 格式转换为 JPEG")

                output = BytesIO()
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 处理透明通道
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    background.save(output, format='JPEG', quality=95)
                else:
                    img.save(output, format='JPEG', quality=95)

                file_data = output.getvalue()
                filename = os.path.splitext(filename)[0] + '.jpg'

            return file_data, filename

        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  图片格式检查失败: {e}")
            return file_data, filename

    def _upload_temporary(
            self,
            access_token: str,
            file_data: bytes,
            filename: str
    ) -> str:
        """上传临时素材"""
        try:
            url = f"{self.UPLOAD_TEMP_URL}?access_token={access_token}&type=image"

            # 获取 MIME 类型
            mime_type = self._get_mime_type(filename)
            files = {'media': (filename, file_data, mime_type)}

            if self.verbose:
                print(f"  📤 正在上传临时素材到微信公众号...")

            response = requests.post(
                url, files=files, proxies=self.proxies, timeout=30)
            response.raise_for_status()

            result = response.json()

            if 'errcode' in result and result['errcode'] != 0:
                raise Exception(
                    f"{result.get('errmsg', '未知错误')} (errcode: {result['errcode']})")

            media_id = result.get('media_id')
            if self.verbose:
                print(f"  ✅ 微信临时素材上传成功！")
                print(f"     Media ID: {media_id}")
                print(f"     有效期: 3天")

            return media_id

        except Exception as e:
            if self.verbose:
                print(f"  ❌ 上传临时素材失败: {e}")
            raise

    def _upload_permanent(
            self,
            access_token: str,
            file_data: bytes,
            filename: str
    ) -> str:
        """上传永久素材"""
        try:
            url = f"{self.UPLOAD_PERMANENT_URL}?access_token={access_token}&type=image"

            # 获取 MIME 类型
            mime_type = self._get_mime_type(filename)
            files = {'media': (filename, file_data, mime_type)}

            if self.verbose:
                print(f"  📤 正在上传永久素材到微信公众号...")

            response = requests.post(
                url, files=files, proxies=self.proxies, timeout=30)
            response.raise_for_status()

            result = response.json()

            if 'errcode' in result and result['errcode'] != 0:
                raise Exception(
                    f"{result.get('errmsg', '未知错误')} (errcode: {result['errcode']})")

            media_id = result.get('media_id')
            image_url = result.get('url')

            if self.verbose:
                print(f"  ✅ 微信永久素材上传成功！")
                if media_id:
                    print(f"     Media ID: {media_id}")
                if image_url:
                    print(f"     URL: {image_url}")

            # 返回 URL（如果有），否则返回 media_id
            return image_url if image_url else media_id

        except Exception as e:
            if self.verbose:
                print(f"  ❌ 上传永久素材失败: {e}")
            raise

    def _upload_news_image(
            self,
            access_token: str,
            file_data: bytes,
            filename: str
    ) -> str:
        """上传图文消息图片"""
        try:
            url = f"{self.UPLOAD_NEWS_IMAGE_URL}?access_token={access_token}"

            # 获取 MIME 类型
            mime_type = self._get_mime_type(filename)
            files = {'media': (filename, file_data, mime_type)}

            if self.verbose:
                print(f"  📤 正在上传图文消息图片到微信公众号...")

            response = requests.post(
                url, files=files, proxies=self.proxies, timeout=30)
            response.raise_for_status()

            result = response.json()

            if 'errcode' in result and result['errcode'] != 0:
                raise Exception(
                    f"{result.get('errmsg', '未知错误')} (errcode: {result['errcode']})")

            image_url = result.get('url')
            if self.verbose:
                print(f"  ✅ 微信图文消息图片上传成功！")
                print(f"     URL: {image_url}")

            return image_url

        except Exception as e:
            if self.verbose:
                print(f"  ❌ 上传图文消息图片失败: {e}")
            raise

    def _get_mime_type(self, filename: str) -> str:
        """根据文件名获取 MIME 类型"""
        ext = filename.rsplit('.', 1)[-1].lower()
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif'
        }
        return mime_types.get(ext, 'image/jpeg')

    def _get_access_token(self) -> Optional[str]:
        """
        获取 access_token（自动选择最佳方式）

        优先级：
        1. 内存缓存（未过期）
        2. 文件缓存（未过期）
        3. 从服务器获取（如果配置了 server_url）
        4. 从微信 API 获取

        :return: access_token 或 None
        """
        import time

        # 1. 检查内存缓存
        if self._access_token and time.time() < self._token_expires_at:
            if self.verbose:
                print(f"  ℹ️  使用内存缓存的 access_token")
            return self._access_token

        # 2. 尝试从文件加载
        token = self._load_token_from_file()
        if token:
            return token

        # 3. 如果配置了服务器 URL，优先从服务器获取
        if self.server_url:
            token = self._get_token_from_server()
            if token:
                return token

            if self.verbose:
                print(f"  ⚠️  从服务器获取 token 失败，尝试直接从微信 API 获取...")

        # 4. 从微信 API 获取
        return self._refresh_access_token()

    def _get_token_from_server(self, retries: int = 2) -> Optional[str]:
        """
        从服务器获取 access_token

        :param retries: 重试次数
        :return: access_token 或 None
        """
        import time

        if not self.server_url:
            return None

        for i in range(retries + 1):
            try:
                if self.verbose:
                    if i == 0:
                        print(f"  🌐 正在从服务器获取 access_token...")
                    else:
                        print(f"  🔄 重试从服务器获取 access_token ({i}/{retries})...")

                headers = {'Content-Type': 'application/json'}
                data = {}

                # 如果有 server_token，添加到请求中
                if self.server_token:
                    data['token'] = self.server_token

                response = requests.post(
                    self.server_url,
                    headers=headers,
                    json=data if data else None,
                    proxies=self.proxies,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()

                # 检查错误信息
                if result.get("detail"):
                    if self.verbose:
                        print(f"  ⚠️  服务器返回错误: {result['detail']}")
                    if i < retries:
                        time.sleep(1)
                        continue
                    return None

                # 提取 token
                access_token = result.get('access_token')
                expires_in = result.get('expires_in', 7200)

                if not access_token:
                    if self.verbose:
                        print(f"  ⚠️  服务器响应中未找到 access_token")
                    if i < retries:
                        time.sleep(1)
                        continue
                    return None

                # 缓存 token
                self._access_token = access_token
                self._token_expires_at = time.time() + expires_in - self.TOKEN_EXPIRE_MARGIN

                # 保存到文件
                self._save_token_to_file(access_token, expires_in)

                if self.verbose:
                    print(f"  ✅ 从服务器获取 access_token 成功")
                    print(f"     有效期: {expires_in}秒")

                return access_token

            except Exception as e:
                if self.verbose:
                    print(f"  ⚠️  从服务器获取失败: {e}")
                if i < retries:
                    time.sleep(1)
                    continue

        return None

    def _refresh_access_token(self) -> Optional[str]:
        """使用 AppID 和 AppSecret 从微信 API 获取 access_token"""
        import time

        try:
            if self.verbose:
                print(f"  🔄 正在从微信 API 获取 access_token...")

            url = f"{self.TOKEN_URL}?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"

            response = requests.get(url, proxies=self.proxies, timeout=10)
            response.raise_for_status()

            result = response.json()

            if 'errcode' in result:
                error_msg = result.get('errmsg', '未知错误')
                if self.verbose:
                    print(f"  ❌ 获取 access_token 失败: {error_msg}")
                return None

            access_token = result.get('access_token')
            expires_in = result.get('expires_in', 7200)

            if not access_token:
                if self.verbose:
                    print(f"  ❌ 响应中未找到 access_token")
                return None

            # 缓存 token
            self._access_token = access_token
            self._token_expires_at = time.time() + expires_in - self.TOKEN_EXPIRE_MARGIN

            # 保存到文件
            self._save_token_to_file(access_token, expires_in)

            if self.verbose:
                print(f"  ✅ 从微信 API 获取 access_token 成功")
                print(f"     有效期: {expires_in}秒")

            return access_token

        except Exception as e:
            if self.verbose:
                print(f"  ❌ 从微信 API 获取 access_token 失败: {e}")
            return None

    def _load_token_from_file(self) -> Optional[str]:
        """从文件加载 access_token"""
        import time

        try:
            if not os.path.exists(self.access_token_file):
                return None

            with open(self.access_token_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            access_token = data.get('access_token')
            expires_at = data.get('expire_time', 0)

            # 检查是否过期
            if time.time() < expires_at:
                self._access_token = access_token
                self._token_expires_at = expires_at
                if self.verbose:
                    print(f"  ✅ 从缓存文件加载 access_token 成功")
                return access_token
            else:
                if self.verbose:
                    print(f"  ⚠️  缓存的 access_token 已过期")
                return None

        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  加载缓存文件失败: {e}")
            return None

    def _save_token_to_file(self, access_token: str, expires_in: int):
        """保存 access_token 到文件"""
        import time

        try:
            # 确保目录存在
            dir_path = os.path.dirname(self.access_token_file)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            data = {
                'access_token': access_token,
                'expire_time': time.time() + expires_in - self.TOKEN_EXPIRE_MARGIN,
                'expires_in': expires_in,
                'updated_at': time.time(),
            }

            with open(self.access_token_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            if self.verbose:
                print(f"  💾 access_token 已缓存到: {self.access_token_file}")

        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  保存 access_token 缓存失败: {e}")


# ============================================================================
# 便捷函数
# ============================================================================

def create_smms_uploader(api_token: Optional[str] = None,
                         api_domain: str = 'https://smms.app') -> callable:
    """
    创建 SM.MS 上传函数

    :param api_token: API Token（可选）
    :param api_domain: API 域名（默认 https://smms.app 国内优化，也可使用 https://sm.ms）
    :return: 上传函数
    """
    uploader = SMUploader(api_token, api_domain)
    return uploader.upload


def create_qiniu_uploader(access_key: str, secret_key: str,
                          bucket: str, domain: str) -> callable:
    """
    创建七牛云上传函数

    :param access_key: AccessKey
    :param secret_key: SecretKey
    :param bucket: 存储空间
    :param domain: CDN域名
    :return: 上传函数
    """
    uploader = QiniuUploader(access_key, secret_key, bucket, domain)
    return uploader.upload


def create_github_uploader(token: str, repo: str, branch: str = 'main',
                           use_jsdelivr: bool = True) -> callable:
    """
    创建 GitHub 上传函数

    :param token: GitHub Token
    :param repo: 仓库（username/repo）
    :param branch: 分支
    :param use_jsdelivr: 使用 jsdelivr CDN
    :return: 上传函数
    """
    uploader = GitHubUploader(token, repo, branch, use_jsdelivr)
    return uploader.upload


def create_local_uploader(storage_dir: str, base_url: str) -> callable:
    """
    创建本地存储上传函数

    :param storage_dir: 存储目录
    :param base_url: 访问URL
    :return: 上传函数
    """
    uploader = LocalStorageUploader(storage_dir, base_url)
    return uploader.upload


def create_wechat_uploader(
        app_id: str,
        app_secret: str,
        upload_type: WechatUploadType = WechatUploadType.NEWS_IMAGE,
        server_url: Optional[str] = None,
        server_token: Optional[str] = None,
        **kwargs
) -> callable:
    """
    创建微信公众号图床上传函数

    :param app_id: 公众号 AppID（必需）
    :param app_secret: 公众号 AppSecret（必需）
    :param upload_type: 上传类型（TEMPORARY/PERMANENT/NEWS_IMAGE），默认 TEMPORARY
    :param server_url: 从服务器获取 access_token 的 URL（可选）
    :param server_token: 服务器认证令牌（可选）
    :param kwargs: 其他参数传递给 WechatUploader
    :return: 上传函数

    示例：
        >>> from mdnice.image_uploaders import create_wechat_uploader, WechatUploadType
        >>>
        >>> # 自动选择最佳 Token 获取方式
        >>> wechat_upload = create_wechat_uploader(
        ...     app_id="wx1234567890",
        ...     app_secret="abcdef1234567890",
        ...     server_url="https://your-server.com/api/token",  # 可选
        ...     upload_type=WechatUploadType.PERMANENT
        ... )
        >>>
        >>> # 上传图片
        >>> url = wechat_upload('/path/to/image.jpg')
    """
    uploader = WechatUploader(
        app_id=app_id,
        app_secret=app_secret,
        upload_type=upload_type,
        server_url=server_url,
        server_token=server_token,
        **kwargs
    )

    return uploader.upload