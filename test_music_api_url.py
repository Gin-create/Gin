import urllib.request
import ssl
import json
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_music_api():
    try:
        # 创建上下文以忽略SSL验证
        context = ssl._create_unverified_context()
        
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
            "Host": "api.qqsuu.cn",  # 必须设置正确的Host头
            "User-Agent": "Mozilla/5.0"
        }
        
        # 创建请求对象
        req = urllib.request.Request(api_url, headers=headers)
        
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            # 读取响应内容
            response_data = response.read()
            
            # 确保响应编码正确
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            logger.info(f"音乐API响应状态: {response.status}")
            logger.info(f"音乐API响应内容: {response_text}")
            
            # 解析JSON数据
            music_data = json.loads(response_text)
            
            if music_data.get('code') == 1:
                data = music_data.get('data', {})
                logger.info(f"歌曲名称: {data.get('name')}")
                logger.info(f"歌手: {data.get('artistsname')}")
                logger.info(f"歌曲URL: {data.get('url')}")
                logger.info(f"封面URL: {data.get('picurl')}")
                
                # 测试歌曲URL是否可访问
                test_song_url(data.get('url'))
            else:
                logger.error(f"API返回错误: {music_data.get('msg')}")
                
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")

def test_song_url(song_url):
    if not song_url:
        logger.error("歌曲URL为空")
        return
    
    try:
        logger.info(f"测试歌曲URL: {song_url}")
        
        # 创建请求对象
        req = urllib.request.Request(song_url)
        
        # 发送GET请求，获取完整响应内容
        with urllib.request.urlopen(req, timeout=10) as response:
            logger.info(f"歌曲URL响应状态: {response.status}")
            logger.info(f"歌曲URL响应头: {dict(response.headers)}")
            
            # 读取响应内容
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response.read().decode(encoding)
            logger.info(f"歌曲URL响应内容: {response_text}")
            
            logger.info(f"歌曲URL可以正常访问")
            
    except Exception as e:
        logger.error(f"歌曲URL测试失败: {str(e)}")

if __name__ == "__main__":
    test_music_api()