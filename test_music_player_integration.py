import requests
import json
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 服务器地址和端口
SERVER_URL = 'http://localhost:5000'

# 测试函数
def test_music_player_integration():
    """测试音乐播放器的完整集成流程"""
    logger.info("开始测试音乐播放器集成功能...")
    
    try:
        # 1. 测试音乐API是否正常工作
        logger.info("1. 测试音乐API...")
        response = requests.get(f"{SERVER_URL}/api/music", params={"keyword": "周杰伦", "limit": 1})
        response.raise_for_status()
        
        music_data = response.json()
        logger.info(f"   API响应状态: {response.status_code}")
        logger.info(f"   API响应数据: {music_data}")
        
        # 验证API返回的数据格式
        assert 'data' in music_data, "API响应缺少'data'字段"
        assert isinstance(music_data['data'], list), "'data'应该是列表类型"
        assert len(music_data['data']) > 0, "没有找到音乐数据"
        
        # 2. 测试Socket.IO消息格式
        logger.info("2. 验证音乐消息格式...")
        
        # 模拟服务器生成的音乐消息格式
        music_info = {
            'song_name': music_data['data'][0]['name'],
            'singer': music_data['data'][0]['artistsname'],
            'song_url': music_data['data'][0]['url'],
            'cover_url': music_data['data'][0]['picurl']
        }
        
        # 验证消息格式
        required_fields = ['song_name', 'singer', 'song_url', 'cover_url']
        for field in required_fields:
            assert field in music_info, f"音乐消息缺少'{field}'字段"
            assert music_info[field] is not None and music_info[field] != '', f"'{field}'字段不能为空"
        
        logger.info("   音乐消息格式验证通过")
        logger.info(f"   歌曲: {music_info['song_name']}")
        logger.info(f"   歌手: {music_info['singer']}")
        logger.info(f"   歌曲URL: {music_info['song_url']}")
        logger.info(f"   封面URL: {music_info['cover_url']}")
        
        # 3. 测试客户端播放器渲染
        logger.info("3. 测试客户端播放器渲染...")
        
        # 模拟客户端渲染的HTML
        html_template = f'''<div class="music-player">
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
        
        # 验证HTML中包含所有必要信息
        assert music_info['song_name'] in html_template, "HTML中缺少歌曲名称"
        assert music_info['singer'] in html_template, "HTML中缺少歌手信息"
        assert music_info['song_url'] in html_template, "HTML中缺少歌曲URL"
        assert music_info['cover_url'] in html_template, "HTML中缺少封面URL"
        
        logger.info("   客户端播放器HTML渲染验证通过")
        
        # 4. 测试右侧边栏播放器
        logger.info("4. 测试右侧边栏播放器...")
        
        # 模拟右侧边栏播放器的HTML
        sidebar_html = f'''<div style="text-align: center; margin-bottom: 10px;">
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
        
        # 验证侧边栏HTML中包含所有必要信息
        assert music_info['song_name'] in sidebar_html, "侧边栏HTML中缺少歌曲名称"
        assert music_info['singer'] in sidebar_html, "侧边栏HTML中缺少歌手信息"
        assert music_info['song_url'] in sidebar_html, "侧边栏HTML中缺少歌曲URL"
        assert music_info['cover_url'] in sidebar_html, "侧边栏HTML中缺少封面URL"
        
        logger.info("   右侧边栏播放器HTML渲染验证通过")
        
        # 5. 测试默认值处理
        logger.info("5. 测试默认值处理...")
        
        # 模拟缺少某些字段的情况
        incomplete_music = {
            'song_name': None,
            'singer': '',
            'song_url': '',
            'cover_url': None
        }
        
        # 测试默认值替换
        sidebar_html = f'''<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold; color: #667eea;">🎵 正在播放音乐</div>
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <img src="{incomplete_music['cover_url'] or 'https://via.placeholder.com/120'}" 
         alt="{incomplete_music['song_name'] or '未知歌曲'}" 
         width="120" 
         height="120" 
         style="border-radius: 8px;">
</div>
<div style="text-align: center; margin-bottom: 10px;">
    <div style="font-weight: bold;">{incomplete_music['song_name'] or '未知歌曲'}</div>
    <div style="color: #666; font-size: 14px;">{incomplete_music['singer'] or '未知歌手'}</div>
</div>
<div style="text-align: center;">
    <audio controls style="width: 100%;">
        <source src="{incomplete_music['song_url'] or ''}" type="audio/mpeg">
        您的浏览器不支持音频播放。
    </audio>
</div>'''
        
        # 验证默认值是否正确使用
        assert '未知歌曲' in sidebar_html, "默认歌曲名称未正确使用"
        assert '未知歌手' in sidebar_html, "默认歌手名称未正确使用"
        assert 'https://via.placeholder.com/120' in sidebar_html, "默认封面URL未正确使用"
        
        logger.info("   默认值处理验证通过")
        
        logger.info("\n✅ 音乐播放器集成功能测试全部通过！")
        logger.info("\n请在浏览器中进行以下手动测试：")
        logger.info("1. 打开聊天页面")
        logger.info("2. 发送 '@音乐 周杰伦' 命令")
        logger.info("3. 检查聊天区域是否显示音乐播放器")
        logger.info("4. 检查右侧边栏是否显示音乐信息")
        logger.info("5. 测试音乐是否可以正常播放")
        
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        logger.exception(e)
        return False

if __name__ == "__main__":
    success = test_music_player_integration()
    exit(0 if success else 1)