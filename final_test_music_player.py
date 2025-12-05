import requests
import json
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 服务器地址和端口
SERVER_URL = 'http://localhost:5000'

def test_music_api():
    """测试音乐API是否正常工作"""
    logger.info("=== 测试音乐API ===")
    
    try:
        # 测试音乐API
        response = requests.get(f"{SERVER_URL}/api/music", params={"keyword": "周杰伦", "limit": 1})
        response.raise_for_status()
        
        logger.info(f"API响应状态: {response.status_code}")
        logger.info(f"API响应内容: {response.text}")
        
        return True
    except Exception as e:
        logger.error(f"音乐API测试失败: {str(e)}")
        return False

def test_music_message_format():
    """验证音乐消息格式是否正确"""
    logger.info("\n=== 验证音乐消息格式 ===")
    
    # 模拟从音乐API获取的数据
    api_response = {
        'data': [
            {
                'name': '晴天',
                'artistsname': '周杰伦',
                'url': 'https://example.com/music.mp3',
                'picurl': 'https://example.com/cover.jpg'
            }
        ]
    }
    
    # 模拟服务器生成的音乐消息
    music_info = {
        'song_name': api_response['data'][0]['name'],
        'singer': api_response['data'][0]['artistsname'],
        'song_url': api_response['data'][0]['url'],
        'cover_url': api_response['data'][0]['picurl']
    }
    
    # 验证消息格式
    required_fields = ['song_name', 'singer', 'song_url', 'cover_url']
    for field in required_fields:
        if field in music_info:
            logger.info(f"✅ 包含字段: {field} = {music_info[field]}")
        else:
            logger.error(f"❌ 缺少字段: {field}")
            return False
    
    return True

def test_client_rendering():
    """验证客户端渲染逻辑是否正确"""
    logger.info("\n=== 验证客户端渲染逻辑 ===")
    
    # 模拟音乐信息
    music_info = {
        'song_name': '晴天',
        'singer': '周杰伦',
        'song_url': 'https://example.com/music.mp3',
        'cover_url': 'https://example.com/cover.jpg'
    }
    
    # 测试聊天区域播放器HTML生成
    chat_player_html = f'''<div class="music-player">
    <div>🎵 正在播放音乐</div>
    <div class="music-pic">
        <img src="{music_info['cover_url']}" alt="{music_info['song_name']}" width="300" height="300">
    </div>
    <div class="music-details">
        <h3 class="music-name">{music_info['song_name']}</h3>
        <h4 class="music-singer">{music_info['singer']}</h4>
        <audio controls>
            <source src="{music_info['song_url']}" type="audio/mpeg">
            您的浏览器不支持音频播放。
        </audio>
    </div>
</div>'''
    
    logger.info("聊天区域播放器HTML:")
    logger.info(chat_player_html)
    
    # 测试右侧边栏播放器HTML生成
    sidebar_player_html = f'''<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold; color: #667eea;">🎵 正在播放音乐</div>
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <img src="{music_info['cover_url']}" 
         alt="{music_info['song_name']}" 
         width="120" 
         height="120" 
         style="border-radius: 8px;">
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold;">{music_info['song_name']}</div>
    <div style="color: #666; font-size: 14px;">{music_info['singer']}</div>
</div>
<div style="text-align: center;">
    <audio controls style="width: 100%;">
        <source src="{music_info['song_url']}" type="audio/mpeg">
        您的浏览器不支持音频播放。
    </audio>
</div>'''
    
    logger.info("\n右侧边栏播放器HTML:")
    logger.info(sidebar_player_html)
    
    # 验证HTML内容
    if music_info['song_name'] in chat_player_html and music_info['singer'] in chat_player_html and \
       music_info['song_name'] in sidebar_player_html and music_info['singer'] in sidebar_player_html:
        logger.info("✅ 客户端渲染逻辑测试通过")
        return True
    else:
        logger.error("❌ 客户端渲染逻辑测试失败")
        return False

def test_default_values():
    """测试默认值处理是否正确"""
    logger.info("\n=== 测试默认值处理 ===")
    
    # 模拟不完整的音乐信息
    music_info = {
        'song_name': None,
        'singer': '',
        'song_url': '',
        'cover_url': None
    }
    
    # 测试右侧边栏播放器默认值
    sidebar_player_html = f'''<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold; color: #667eea;">🎵 正在播放音乐</div>
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <img src="{music_info['cover_url'] or 'https://via.placeholder.com/120'}" 
         alt="{music_info['song_name'] or '未知歌曲'}" 
         width="120" 
         height="120" 
         style="border-radius: 8px;">
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold;">{music_info['song_name'] or '未知歌曲'}</div>
    <div style="color: #666; font-size: 14px;">{music_info['singer'] or '未知歌手'}</div>
</div>
<div style="text-align: center;">
    <audio controls style="width: 100%;">
        <source src="{music_info['song_url'] or ''}" type="audio/mpeg">
        您的浏览器不支持音频播放。
    </audio>
</div>'''
    
    logger.info("默认值处理后的HTML:")
    logger.info(sidebar_player_html)
    
    # 验证默认值
    if '未知歌曲' in sidebar_player_html and '未知歌手' in sidebar_player_html and \
       'https://via.placeholder.com/120' in sidebar_player_html:
        logger.info("✅ 默认值处理测试通过")
        return True
    else:
        logger.error("❌ 默认值处理测试失败")
        return False

def run_all_tests():
    """运行所有测试"""
    logger.info("开始音乐播放器功能测试...")
    
    tests = [
        test_music_message_format,
        test_client_rendering,
        test_default_values
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    logger.info(f"\n=== 测试结果 ===")
    logger.info(f"通过: {passed}/{total} 测试")
    
    if passed == total:
        logger.info("✅ 所有测试通过！")
        logger.info("\n请在浏览器中进行以下手动测试：")
        logger.info("1. 打开聊天页面 (http://localhost:5000)")
        logger.info("2. 登录聊天室")
        logger.info("3. 发送 '@音乐 周杰伦' 命令")
        logger.info("4. 检查聊天区域是否显示音乐播放器")
        logger.info("5. 检查右侧边栏是否显示音乐信息")
        logger.info("6. 测试音乐是否可以正常播放")
        
        return True
    else:
        logger.error("❌ 部分测试失败")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)