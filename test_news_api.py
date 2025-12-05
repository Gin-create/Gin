import requests
import json
import time

# 直接测试新闻API调用
def test_news_api():
    print('开始测试新闻API...')
    
    try:
        # 导入urllib模块
        import urllib.request
        import urllib.error
        import ssl
        
        # 新闻API配置
        api_key = "a440759fd3d87545"
        news_url = "https://v2.xxapi.cn/api/weibohot"
        
        # 创建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'api-key': api_key,
            'Host': 'v2.xxapi.cn'
        }
        
        # 创建请求对象
        req = urllib.request.Request(news_url, headers=headers)
        
        # 配置SSL上下文，禁用证书验证并强制使用TLS 1.2
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # 发送请求
        print(f"发送请求到: {news_url}")
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            # 读取响应内容
            response_data = response.read()
            encoding = response.info().get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            print(f"响应状态码: {response.getcode()}")
            print(f"响应内容: {response_text}")
            
            # 解析JSON
            news_data = json.loads(response_text)
            print(f"解析成功: {json.dumps(news_data, ensure_ascii=False, indent=2)}")
            
            # 提取新闻列表
            news_list = news_data.get('data', [])
            print(f"新闻列表长度: {len(news_list)}")
            
            return True
            
    except urllib.error.URLError as e:
        print(f"URL错误: {e}")
        if hasattr(e, 'reason'):
            print(f"错误原因: {e.reason}")
        elif hasattr(e, 'code'):
            print(f"错误代码: {e.code}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = test_news_api()
    if success:
        print("\n测试成功！新闻API调用正常")
    else:
        print("\n测试失败！新闻API调用异常")