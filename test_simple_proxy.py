import urllib.request
import urllib.parse
import urllib.error
import ssl

# 测试代理路由
def test_proxy():
    # 原始网易云音乐URL
    original_url = "http://music.163.com/song/media/outer/url?id=167655"
    
    # 构造代理URL
    encoded_url = urllib.parse.quote(original_url)
    proxy_url = f"http://localhost:5000/proxy-music?url={encoded_url}"
    print(f"测试代理URL: {proxy_url}")
    
    # 创建请求
    req = urllib.request.Request(proxy_url)
    
    # 忽略SSL证书验证
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            print(f"响应状态码: {response.status}")
            print(f"响应内容类型: {response.headers.get('Content-Type', '未知')}")
            print(f"响应内容长度: {response.headers.get('Content-Length', '未知')}")
            
            # 读取部分内容进行测试
            content = response.read(1024)  # 只读取前1024字节
            print(f"响应内容前100字节: {content[:100]}")
            
            # 检查是否是音频数据
            if response.headers.get('Content-Type', '').startswith('audio/'):
                print("✅ 代理路由正常工作，返回音频数据")
            else:
                print("❌ 代理路由返回非音频数据")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}")
    except Exception as e:
        print(f"❌ 其他错误: {str(e)}")

if __name__ == "__main__":
    test_proxy()
