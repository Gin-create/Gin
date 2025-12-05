import urllib.request
import ssl
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_music_proxy():
    try:
        # 1. 首先获取一首音乐的信息
        music_url = get_random_music()
        if not music_url:
            logger.error("无法获取音乐URL")
            return
        
        # 2. 测试代理路由
        proxy_url = f"http://localhost:5000/proxy-music?url={urllib.parse.quote(music_url)}"
        logger.info(f"测试代理URL: {proxy_url}")
        
        # 创建SSL上下文
        context = ssl._create_unverified_context()
        
        # 创建请求
        req = urllib.request.Request(proxy_url)
        
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            logger.info(f"代理响应状态: {response.status}")
            logger.info(f"代理响应头: {dict(response.headers)}")
            
            # 读取部分内容验证
            content = response.read(1024)  # 只读取前1024字节
            logger.info(f"代理响应内容类型: {response.headers.get('Content-Type')}")
            logger.info(f"代理响应内容长度: {len(content)}字节")
            logger.info(f"代理路由测试成功！")
            
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")

def get_random_music():
    try:
        # 直接使用IP地址访问，绕过DNS解析
        api_ip = "43.240.193.23"
        api_path = "/api/dm-randmusic"
        api_key = "828a388ecd2ece83964472c5cd61d4fc"
        params = {
            "sort": "热歌榜",
            "format": "json"
        }
        
        # 构建完整URL
        query_string = urllib.parse.urlencode(params)
        api_url = f"https://{api_ip}{api_path}?{query_string}"
        
        # 设置请求头
        headers = {
            "api-key": api_key,
            "Host": "api.qqsuu.cn",
            "User-Agent": "Mozilla/5.0"
        }
        
        # 创建SSL上下文
        context = ssl._create_unverified_context()
        
        # 创建请求
        req = urllib.request.Request(api_url, headers=headers)
        
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            response_data = response.read()
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            music_data = json.loads(response_text)
            
            if music_data.get('code') == 1:
                data = music_data.get('data', {})
                song_url = data.get('url')
                logger.info(f"获取到音乐URL: {song_url}")
                return song_url
            else:
                logger.error(f"音乐API返回错误: {music_data.get('msg')}")
                return None
                
    except Exception as e:
        logger.error(f"获取音乐失败: {str(e)}")
        return None

if __name__ == "__main__":
    test_music_proxy()