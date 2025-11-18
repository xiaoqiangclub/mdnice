# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：图片上传功能示例
# 文件路径：examples/image_upload.py


from mdnice import to_wechat
from pathlib import Path
import time


def example_1_upload_local_images():
    """示例1: 上传本地图片"""
    print("=" * 80)
    print("示例1: 上传本地图片到图床")
    print("=" * 80)

    def my_uploader(image_path: str) -> str:
        """自定义图片上传函数"""
        print(f"    📤 上传: {Path(image_path).name}")

        # 模拟上传过程
        time.sleep(0.2)

        # 返回模拟的图床URL
        filename = Path(image_path).name
        return f"https://cdn.example.com/images/{filename}"

    html = to_wechat(
        'test.md',
        theme='rose',
        output_dir='output/upload_local',
        image_uploader=my_uploader,
        image_upload_mode='local'  # 只上传本地图片
    )

    print(f"✅ 转换完成，HTML长度: {len(html)}\n")


def example_2_upload_remote_images():
    """示例2: 上传网络图片"""
    print("=" * 80)
    print("示例2: 下载网络图片并上传到自己的CDN")
    print("=" * 80)

    def download_and_reupload(image_url: str) -> str:
        """下载网络图片并重新上传"""
        import requests

        if not image_url.startswith('http'):
            return image_url

        print(f"    📥 下载: {image_url[:60]}...")

        try:
            # 下载图片
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            # 模拟上传到自己的CDN
            # upload_to_cdn(response.content)

            cdn_url = f"https://my-cdn.com/images/{hash(image_url)}.jpg"
            print(f"    ✅ 已上传到CDN")
            return cdn_url

        except Exception as e:
            print(f"    ❌ 失败: {e}")
            return image_url  # 失败则保持原样

    html = to_wechat(
        'test.md',
        theme='geekBlack',
        output_dir='output/upload_remote',
        image_uploader=download_and_reupload,
        image_upload_mode='remote'  # 只上传网络图片
    )

    print(f"✅ 转换完成，HTML长度: {len(html)}\n")


def example_3_upload_all_images():
    """示例3: 上传所有图片"""
    print("=" * 80)
    print("示例3: 上传所有图片（本地+网络）")
    print("=" * 80)

    def universal_uploader(image: str) -> str:
        """通用上传器"""
        import requests

        # 网络图片
        if image.startswith('http'):
            print(f"    📥 下载网络图片...")
            response = requests.get(image, timeout=10)
            image_data = response.content
            filename = f"remote_{hash(image)}.jpg"

        # 本地图片
        else:
            print(f"    📂 读取本地图片: {Path(image).name}")
            with open(image, 'rb') as f:
                image_data = f.read()
            filename = Path(image).name

        # 统一上传
        # uploaded_url = upload_to_image_host(image_data, filename)

        return f"https://img.example.com/{filename}"

    html = to_wechat(
        'test.md',
        theme='scienceBlue',
        output_dir='output/upload_all',
        image_uploader=universal_uploader,
        image_upload_mode='all'  # 上传所有图片
    )

    print(f"✅ 转换完成，HTML长度: {len(html)}\n")


def example_4_smms_integration():
    """示例4: 集成SM.MS图床"""
    print("=" * 80)
    print("示例4: 使用SM.MS图床")
    print("=" * 80)

    def upload_to_smms(image_path: str) -> str:
        """上传到SM.MS图床"""
        import requests

        # SM.MS API配置
        api_url = 'https://sm.ms/api/v2/upload'
        api_token = 'YOUR_SMMS_API_TOKEN'  # 替换为你的token

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

            # 上传到SM.MS
            files = {'smfile': (filename, file_data)}
            headers = {'Authorization': api_token}

            response = requests.post(
                api_url,
                files=files,
                headers=headers,
                timeout=30
            )

            result = response.json()

            if result.get('success'):
                print(f"    ✅ 上传成功: {result['data']['url']}")
                return result['data']['url']
            else:
                raise Exception(result.get('message', '上传失败'))

        except Exception as e:
            print(f"    ❌ 上传失败: {e}")
            raise

    # 取消注释以使用
    # html = to_wechat(
    #     'test.md',
    #     theme='rose',
    #     output_dir='output/smms',
    #     image_uploader=upload_to_smms,
    #     image_upload_mode='all'
    # )

    print("ℹ️ 请先配置SM.MS API Token后使用\n")


if __name__ == "__main__":
    # 运行示例
    example_1_upload_local_images()
    example_2_upload_remote_images()
    example_3_upload_all_images()
    example_4_smms_integration()

    print("🎉 图片上传示例完成！")
