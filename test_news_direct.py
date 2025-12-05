# 直接测试新闻功能的核心逻辑
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所需模块
import urllib
import urllib.request
import urllib.error
import ssl
import json
import time

# 模拟app.py中的新闻功能代码
def test_news_function():
    print("开始测试新闻功能...")
    
    # 新闻API配置
    api_key = "a440759fd3d87545"
    news_url = "https://v2.xxapi.cn/api/weibohot"
    
    try:
        # 设置请求头
        req = urllib.request.Request(news_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('api-key', api_key)
        req.add_header('Host', 'v2.xxapi.cn')
        
        # 忽略SSL证书验证并设置SSL/TLS版本
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 强制使用TLS 1.2
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.min_version = ssl.TLSVersion.TLSv1_2
        
        # 发送请求
        print("发送HTTP请求...")
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            # 读取响应内容
            response_data = response.read()
            
            # 确保响应编码正确
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            print(f"HTTP请求完成，响应状态: {response.status}")
            
            # 解析JSON响应
            news_data = json.loads(response_text)
            print("JSON响应解析成功")
            print(f"响应结构: {list(news_data.keys())}")
            
            if news_data.get('code') == 200:
                print("新闻功能测试成功!")
                print(f"获取到 {len(news_data.get('data', []))} 条新闻")
                # 打印前5条新闻
                for i, news in enumerate(news_data.get('data', [])[:5]):
                    print(f"{i+1}. {news.get('title', '无标题')}")
            else:
                print(f"新闻API返回错误: {news_data.get('msg', '未知错误')}")
                
    except Exception as e:
        print(f"新闻功能测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_news_function()
