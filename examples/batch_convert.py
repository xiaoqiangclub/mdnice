# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：批量转换示例
# 文件路径：examples/batch_convert.py

from mdnice import to_wechat, to_zhihu, to_juejin, convert
from pathlib import Path


def example_1_batch_files():
    """示例1: 批量转换多个文件"""
    print("=" * 80)
    print("示例1: 批量转换多个Markdown文件")
    print("=" * 80)

    files = [
        'article1.md',
        'article2.md',
        'article3.md'
    ]

    html_list = to_wechat(
        files,
        theme='random',
        output_dir='output/batch'
    )

    print(f"✅ 批量转换完成，共 {len(html_list)} 个文件\n")


def example_2_multi_platform():
    """示例2: 一文多发"""
    print("=" * 80)
    print("示例2: 同一文章转换为多个平台格式")
    print("=" * 80)

    article = 'article.md'

    # 转换为微信格式
    to_wechat(article, theme='rose', output_dir='output/multi/wechat')
    print("✅ 微信公众号格式")

    # 转换为知乎格式
    to_zhihu(article, theme='geekBlack', output_dir='output/multi/zhihu')
    print("✅ 知乎格式")

    # 转换为掘金格式
    to_juejin(article, theme='scienceBlue', output_dir='output/multi/juejin')
    print("✅ 掘金格式\n")


def example_3_batch_with_themes():
    """示例3: 批量转换使用不同主题"""
    print("=" * 80)
    print("示例3: 批量转换，每个文件随机主题")
    print("=" * 80)

    files = ['a.md', 'b.md', 'c.md']
    themes = ['rose', 'geekBlack', 'scienceBlue']

    # 方式1: 完全随机
    to_wechat(files, theme='random', output_dir='output/random1')
    print("✅ 完全随机主题")

    # 方式2: 从指定列表随机
    to_wechat(files, theme=themes, output_dir='output/random2')
    print("✅ 从列表随机主题\n")


def example_4_batch_with_image_upload():
    """示例4: 批量转换并上传图片"""
    print("=" * 80)
    print("示例4: 批量转换，统一上传图片到图床")
    print("=" * 80)

    def batch_uploader(image_path: str) -> str:
        """批量上传图片"""
        from pathlib import Path
        import time

        filename = Path(image_path).name if not image_path.startswith(
            'http') else 'remote.jpg'

        # 模拟上传
        time.sleep(0.1)

        return f"https://batch-cdn.com/{filename}"

    files = ['article1.md', 'article2.md', 'article3.md']

    html_list = to_wechat(
        files,
        theme='random',
        output_dir='output/batch_upload',
        image_uploader=batch_uploader,
        image_upload_mode='local'
    )

    print(f"✅ 批量转换+图片上传完成，共 {len(html_list)} 个文件\n")


def example_5_directory_conversion():
    """示例5: 转换整个目录的Markdown文件"""
    print("=" * 80)
    print("示例5: 转换目录下所有Markdown文件")
    print("=" * 80)

    # 获取目录下所有.md文件
    md_dir = Path('articles')
    if md_dir.exists():
        md_files = list(md_dir.glob('*.md'))

        if md_files:
            html_list = to_wechat(
                md_files,
                theme='random',
                output_dir='output/directory'
            )
            print(f"✅ 转换完成，共 {len(html_list)} 个文件")
        else:
            print("⚠️ 目录中没有Markdown文件")
    else:
        print("⚠️ articles 目录不存在\n")


def example_6_error_handling():
    """示例6: 批量转换的错误处理"""
    print("=" * 80)
    print("示例6: 批量转换时的错误处理")
    print("=" * 80)

    def error_handler(error_msg: str, context: dict):
        """错误处理回调"""
        print(f"  ⚠️ 捕获错误: {error_msg}")
        print(f"  📍 阶段: {context.get('stage')}")
        # 可以在这里发送通知、记录日志等

    files = ['good.md', 'not_exist.md', 'another.md']

    try:
        html_list = to_wechat(
            files,
            theme='rose',
            output_dir='output/error_handling',
            on_error=error_handler,
            retry_count=2
        )
        print(f"✅ 部分转换完成，成功 {len(html_list)} 个文件\n")
    except Exception as e:
        print(f"❌ 转换失败: {e}\n")


if __name__ == "__main__":
    # 运行示例
    example_1_batch_files()
    example_2_multi_platform()
    example_3_batch_with_themes()
    example_4_batch_with_image_upload()
    example_5_directory_conversion()
    example_6_error_handling()

    print("🎉 批量转换示例完成！")
