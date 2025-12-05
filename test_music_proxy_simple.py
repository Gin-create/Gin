import urllib.request
import urllib.parse
import os

# 测试代理路由是否正常工作
# 模拟从API获取的原始音乐URL
api_music_url = "http://music.163.com/song/media/outer/url?id=167655"

# 构建代理请求URL
proxy_url = f"http://localhost:5000/proxy-music?url={urllib.parse.quote(api_music_url)}"

print(f"测试代理路由: {proxy_url}")
print(f"原始音乐URL: {api_music_url}")

# 发送请求获取音乐文件
try:
    print("正在请求音乐文件...")
    with urllib.request.urlopen(proxy_url, timeout=10) as response:
        # 获取响应状态码
        status_code = response.status
        print(f"响应状态码: {status_code}")
        
        # 获取响应头
        headers = dict(response.headers)
        print(f"响应头: {headers}")
        
        # 读取响应内容
        content = response.read()
        content_length = len(content)
        print(f"响应内容长度: {content_length} 字节")
        
        # 如果响应内容非空，保存到文件
        if content_length > 0:
            test_file = "test_music_proxy_response.mp3"
            with open(test_file, 'wb') as f:
                f.write(content)
            print(f"音乐文件已保存到: {test_file}")
            print(f"文件大小: {os.path.getsize(test_file)} 字节")
        else:
            print("响应内容为空")
            
except Exception as e:
    print(f"请求失败: {str(e)}")
