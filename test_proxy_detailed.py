import requests
import logging
import time
from urllib.parse import urlencode

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 音乐API配置
music_api_url = "https://43.240.193.23/api/dm-randmusic"
api_key = "dm-dm-randmusic-321"

# 获取随机音乐信息
def get_random_music():
    try:
        headers = {
            "api-key": api_key,
            "Host": "api.qqsuu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        params = {
            "sort": "热歌榜",
            "format": "json"
        }
        
        # 直接通过IP地址访问
        response = requests.get(music_api_url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"音乐API响应: {data}")
        
        if data.get('code') == 1:
            music_info = {
                "song_name": data.get('name', '未知歌曲'),
                "singer": data.get('artistsname', '未知歌手'),
                "song_url": data.get('url', ''),
                "cover_url": data.get('picurl', '')
            }
            return music_info
        else:
            logger.error(f"音乐API返回错误: {data.get('msg', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"请求音乐API时发生错误: {e}")
        return None
    except ValueError as e:
        logger.error(f"解析音乐API响应时发生错误: {e}")
        return None

# 测试代理路由
def test_proxy_route(original_url):
    try:
        # 构造代理URL
        proxy_url = f"http://localhost:5000/proxy-music?url={requests.utils.quote(original_url)}"
        logger.info(f"测试代理URL: {proxy_url}")
        
        # 发送请求到代理路由
        response = requests.get(proxy_url, verify=False)
        
        # 记录响应状态和头信息
        logger.info(f"代理响应状态码: {response.status_code}")
        logger.info(f"代理响应内容类型: {response.headers.get('Content-Type', '未知')}")
        logger.info(f"代理响应头: {dict(response.headers)}")
        
        # 检查响应内容
        if response.status_code == 200:
            # 检查是否是音频数据
            if response.headers.get('Content-Type', '').startswith('audio/'):
                logger.info("✅ 代理路由正常工作，返回音频数据")
                logger.info(f"音频数据大小: {len(response.content)} 字节")
                return True
            else:
                # 如果不是音频数据，查看返回的内容
                logger.warning(f"❌ 代理路由返回非音频数据，内容: {response.text[:100]}...")
                return False
        else:
            logger.error(f"❌ 代理路由返回错误状态码: {response.status_code}")
            logger.error(f"错误响应内容: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 请求代理路由时发生错误: {e}")
        return False

# 测试原始URL
def test_original_url(original_url):
    try:
        logger.info(f"测试原始URL: {original_url}")
        
        # 发送请求到原始URL
        response = requests.get(original_url, verify=False, headers={
            "Referer": "https://music.163.com/"
        })
        
        logger.info(f"原始URL响应状态码: {response.status_code}")
        logger.info(f"原始URL内容类型: {response.headers.get('Content-Type', '未知')}")
        
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"测试原始URL时发生错误: {e}")
        return False

if __name__ == "__main__":
    logger.info("开始测试音乐代理功能")
    
    # 获取随机音乐
    music_info = get_random_music()
    if not music_info:
        logger.error("无法获取音乐信息，测试结束")
        exit(1)
    
    logger.info(f"获取到音乐信息: {music_info}")
    song_url = music_info['song_url']
    
    if not song_url:
        logger.error("没有获取到歌曲URL，测试结束")
        exit(1)
    
    # 测试原始URL
    logger.info("\n=== 测试原始URL ===")
    test_original_url(song_url)
    
    # 测试代理路由
    logger.info("\n=== 测试代理路由 ===")
    test_proxy_route(song_url)
    
    logger.info("\n测试完成")
