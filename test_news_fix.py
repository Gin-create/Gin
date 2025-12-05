import sys
import os

# 将当前目录添加到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接导入新闻功能函数
from app import get_news

# 测试新闻功能
try:
    news_html = get_news()
    print("\n新闻功能测试成功！")
    print(f"获取到的新闻HTML长度: {len(news_html)} 字符")
    print("\n新闻HTML内容预览:")
    print(news_html[:500] + "...")
except Exception as e:
    print(f"\n新闻功能测试失败！")
    print(f"错误信息: {str(e)}")
    import traceback
    traceback.print_exc()