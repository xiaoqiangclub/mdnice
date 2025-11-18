# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：图床上传工具使用示例
# 文件路径：examples/use_image_uploaders.py

from mdnice import to_wechat
from mdnice.image_uploaders import (
    create_smms_uploader,
    create_local_uploader,
    SMUploader
)


def example_1_smms_basic():
    """示例1: 使用 SM.MS 图床（基础）"""
    print("=" * 80)
    print("示例1: 使用 SM.MS 图床（基础）")
    print("=" * 80)

    # 创建测试 Markdown（包含网络图片）
    test_markdown = """
# SM.MS 图床测试

这是一张测试图片：

![测试图片](https://picsum.photos/400/300)
"""

    # 创建上传函数（使用国内优化域名）
    upload_image = create_smms_uploader(
        api_token='YOUR_SMMS_API_TOKEN'  # 替换为你的 Token
    )

    # 转换（这里会上传网络图片）
    try:
        html = to_wechat(
            test_markdown,
            theme='rose',
            image_uploader=upload_image,
            image_upload_mode='remote',  # 上传网络图片
            output_dir='output/smms'
        )
        print(f"✅ 转换成功，HTML长度: {len(html)}\n")
    except Exception as e:
        print(f"❌ 转换失败: {e}\n")
        print("💡 请确保设置了正确的 API Token")


def example_2_smms_domain():
    """示例2: SM.MS 域名选择"""
    print("=" * 80)
    print("示例2: SM.MS 域名选择")
    print("=" * 80)

    test_markdown = "# 测试\n\n![图片](https://picsum.photos/200)"

    # 方式1: 使用国内优化域名（默认）
    print("\n使用国内优化域名...")
    uploader_cn = create_smms_uploader(
        api_token='YOUR_TOKEN',
        api_domain='https://smms.app'  # 国内优化（可省略，这是默认值）
    )

    # 方式2: 使用国际域名
    print("使用国际域名...")
    uploader_intl = create_smms_uploader(
        api_token='YOUR_TOKEN',
        api_domain='https://sm.ms'  # 国际域名
    )

    print("✅ 域名配置完成\n")


def example_3_smart_uploader():
    """示例3: 智能上传器（域名自动切换）"""
    print("=" * 80)
    print("示例3: 智能上传器（域名自动切换）")
    print("=" * 80)

    def smart_smms_uploader(image_path: str) -> str:
        """
        智能 SM.MS 上传器
        优先使用国内域名，失败后自动切换到国际域名
        """
        domains = [
            'https://smms.app',  # 国内优化
            'https://sm.ms'      # 国际域名
        ]

        for domain in domains:
            try:
                print(f"  🔄 尝试域名: {domain}")
                uploader = SMUploader(
                    api_token='YOUR_TOKEN',
                    api_domain=domain
                )
                return uploader.upload(image_path)
            except Exception as e:
                print(f"  ❌ {domain} 失败: {e}")
                continue

        raise Exception("所有域名均上传失败")

    test_markdown = "# 测试\n\n![图片](https://picsum.photos/300)"

    try:
        html = to_wechat(
            test_markdown,
            image_uploader=smart_smms_uploader,
            image_upload_mode='remote'
        )
        print(f"✅ 智能上传成功\n")
    except Exception as e:
        print(f"❌ 上传失败: {e}\n")


def example_4_local_storage():
    """示例4: 使用本地存储"""
    print("=" * 80)
    print("示例4: 使用本地存储")
    print("=" * 80)

    # 创建本地存储上传器
    upload_image = create_local_uploader(
        storage_dir='output/images',  # 本地存储目录
        base_url='http://localhost:8000/images'  # 访问 URL
    )

    test_markdown = """
# 本地存储测试

![测试图片](https://picsum.photos/400/200)
"""

    try:
        html = to_wechat(
            test_markdown,
            theme='rose',
            image_uploader=upload_image,
            image_upload_mode='remote',
            output_dir='output/local'
        )
        print(f"✅ 图片已保存到本地: output/images/\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")


def example_5_mock_uploader():
    """示例5: 模拟上传器（用于测试）"""
    print("=" * 80)
    print("示例5: 模拟上传器（用于测试）")
    print("=" * 80)

    def mock_uploader(image_path: str) -> str:
        """模拟上传器，仅打印不实际上传"""
        print(f"  📤 [模拟上传] {image_path}")
        # 返回模拟URL
        return f"https://mock-cdn.com/images/{hash(image_path)}.jpg"

    test_markdown = """
# 测试

![图片1](https://picsum.photos/200/300)
![图片2](https://via.placeholder.com/150)
"""

    html = to_wechat(
        test_markdown,
        image_uploader=mock_uploader,
        image_upload_mode='all',
        output_dir='output/mock'
    )
    print(f"✅ 模拟转换完成\n")


if __name__ == "__main__":
    print("\n🚀 图床上传工具示例\n")

    # example_1_smms_basic()  # 需要真实 API Token
    example_2_smms_domain()
    example_3_smart_uploader()
    example_4_local_storage()
    example_5_mock_uploader()

    print("\n🎉 示例运行完成！")
    print("\n💡 提示：")
    print("   - SM.MS 示例需要替换真实的 API Token")
    print("   - 获取 Token：https://sm.ms/home/apitoken")
