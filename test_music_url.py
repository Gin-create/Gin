import urllib.request
import urllib.parse
import urllib.error
import ssl

# 测试原始网易云音乐URL
def test_original_url():
    original_url = "http://music.163.com/song/media/outer/url?id=167655"
    print(f"测试原始URL: {original_url}")
    
    # 创建请求
    req = urllib.request.Request(original_url)
    req.add_header('Referer', 'http://music.163.com/')
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    # 忽略SSL证书验证
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            print(f"原始URL响应状态码: {response.status}")
            print(f"原始URL内容类型: {response.headers.get('Content-Type', '未知')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"原始URL HTTP错误: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"原始URL网络错误: {e.reason}")
        return False
    except Exception as e:
        print(f"原始URL其他错误: {str(e)}")
        return False

# 测试代理URL
def test_proxy_url():
    original_url = "http://music.163.com/song/media/outer/url?id=167655"
    encoded_url = urllib.parse.quote(original_url)
    proxy_url = f"http://localhost:5000/proxy-music?url={encoded_url}"
    print(f"\n测试代理URL: {proxy_url}")
    
    # 创建请求
    req = urllib.request.Request(proxy_url)
    
    # 忽略SSL证书验证
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            print(f"代理URL响应状态码: {response.status}")
            print(f"代理URL内容类型: {response.headers.get('Content-Type', '未知')}")
            print(f"代理URL响应头: {dict(response.headers)}")
            return True
    except urllib.error.HTTPError as e:
        print(f"代理URL HTTP错误: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"代理URL网络错误: {e.reason}")
        return False
    except Exception as e:
        print(f"代理URL其他错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 测试原始URL
    test_original_url()
    
    # 测试代理URL
    test_proxy_url()
