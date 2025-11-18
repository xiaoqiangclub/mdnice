# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：基础使用示例
# 文件路径：examples/basic_usage.py

from mdnice import to_wechat, to_zhihu, to_juejin


def example_1_basic_conversion():
    """示例1: 基础转换"""
    print("=" * 80)
    print("示例1: 基础转换")
    print("=" * 80)

    # 创建测试 Markdown 内容
    test_markdown = """
# 测试标题

这是一段测试内容。

## 子标题

- 列表项 1
- 列表项 2
- 列表项 3

**粗体文本** 和 *斜体文本*

```python
print("Hello, World!")
"""
    # 转换为微信公众号格式
    html = to_wechat(
        test_markdown,
        theme='rose',
        output_dir='output/wechat'
    )
    print(f"✅ 微信格式转换成功，HTML长度: {len(html)}\n")


def example_2_different_platforms():

    """示例2: 不同平台转换"""
    print("=" * 80)
    print("示例2: 转换为不同平台格式")
    print("=" * 80)
    test_content = "# 测试\n\n这是测试内容。"

    # 微信公众号
    to_wechat(test_content, theme='rose', output_dir='output/wechat')
    print("✅ 微信公众号格式已生成")

    # 知乎
    to_zhihu(test_content, theme='geekBlack', output_dir='output/zhihu')
    print("✅ 知乎格式已生成")

    # 掘金
    to_juejin(test_content, theme='scienceBlue', output_dir='output/juejin')
    print("✅ 掘金格式已生成\n")


def example_3_custom_theme():
    """示例3: 自定义主题"""
    print("=" * 80)
    print("示例3: 使用不同主题")
    print("=" * 80)
    test_content = "# 测试\n\n这是测试内容。"

    # 使用指定主题
    to_wechat(test_content, theme='rose', output_dir='output/theme1')
    print("✅ 蔷薇紫主题")

    # 从列表随机选择
    to_wechat(
        test_content,
        theme=['rose', 'geekBlack', 'scienceBlue'],
        output_dir='output/theme2'
    )
    print("✅ 随机主题")

    # 完全随机
    to_wechat(test_content, theme='random', output_dir='output/theme3')
    print("✅ 完全随机主题\n")


def example_4_with_images():

    """示例4: 包含图片的 Markdown"""
    print("=" * 80)
    print("示例4: 包含图片的 Markdown")
    print("=" * 80)
    markdown_with_images = """
# 图片测试

这是一张网络图片：

![网络图片](https://picsum.photos/200/300)

这是另一张图片：

![示例](https://via.placeholder.com/150)
"""

    html = to_wechat(
        markdown_with_images,
        theme='rose',
        output_dir='output/images'
    )
    print(f"✅ 转换成功，HTML长度: {len(html)}\n")


if __name__ == "__main__":
    # 运行所有示例
    print("\n🚀 开始运行示例...\n")

    try:
        example_1_basic_conversion()
        example_2_different_platforms()
        example_3_custom_theme()
        example_4_with_images()

        print("🎉 所有示例运行完成！")
        print("\n💡 提示：生成的 HTML 文件保存在 output/ 目录中")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        print("\n💡 可能的原因：")
        print("   1. 未安装 Chrome 浏览器")
        print("   2. 网络连接问题")
        print("   3. ChromeDriver 下载失败")
        print("\n💡 解决方案：")
        print("   1. 确保已安装 Chrome 浏览器")
        print("   2. 检查网络连接")
        print("   3. 升级 Selenium: pip install --upgrade selenium")
