# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18T09:57:00.672Z
# 文件描述：自定义编辑器示例
# 文件路径：examples/custom_editor.py


from mdnice import to_wechat

# 使用自定义编辑器地址
print("=" * 80)
print("自定义编辑器示例")
print("=" * 80)

html = to_wechat(
    'article.md',
    theme='rose',
    output_dir='output',
    editor_url='https://your-domain.com/markdown-nice/',  # 你自己部署的编辑器
    retry_count=2  # 失败后会自动切换到默认和备用地址
)

print(f"✅ 转换成功！HTML长度: {len(html)}\n")


# 错误通知回调示例
def error_handler(error_msg: str, context: dict):
    """自定义错误处理"""
    print(f"❌ 捕获到错误：{error_msg}")
    print(f"📍 错误阶段：{context.get('stage')}")
    # 这里可以发送邮件、钉钉通知等
    # send_notification(error_msg)


html = to_wechat(
    'article.md',
    on_error=error_handler
)
