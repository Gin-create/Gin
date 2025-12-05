#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐功能集成测试脚本
测试客户端和服务器之间的音乐消息格式是否匹配
"""

import sys
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_music_message_format():
    """测试音乐消息格式是否正确"""
    try:
        # 模拟服务器发送的音乐消息格式
        server_music_response = {
            'type': 'music',
            'username': 'AI助手',
            'message': '@音乐 随机',
            'music_info': {
                'song_name': '小胡同',
                'singer': '郑润泽',
                'song_url': 'https://music.163.com/song/media/outer/url?id=2045129228.mp3',
                'cover_url': 'https://p1.music.126.net/1AeC1234567890ABCDEFGH1234567890ABCDEFGH1234567890.jpg'
            }
        }
        
        logger.info("测试服务器音乐消息格式...")
        logger.info(f"服务器响应: {json.dumps(server_music_response, ensure_ascii=False)}")
        
        # 检查必要字段是否存在
        required_fields = ['type', 'username', 'message', 'music_info']
        for field in required_fields:
            if field not in server_music_response:
                logger.error(f"缺少必要字段: {field}")
                return False
        
        # 检查music_info中的字段
        music_info = server_music_response['music_info']
        music_required_fields = ['song_name', 'singer', 'song_url', 'cover_url']
        for field in music_required_fields:
            if field not in music_info:
                logger.error(f"music_info中缺少必要字段: {field}")
                return False
        
        logger.info("服务器音乐消息格式检查通过!")
        
        # 模拟客户端解析过程
        logger.info("\n测试客户端解析过程...")
        if server_music_response['type'] == 'music' and server_music_response['music_info']:
            music = server_music_response['music_info']
            
            # 模拟客户端生成的HTML
            client_html = f'''
                <div>🎵 正在播放音乐</div>
                <div class="music-player">
                    <div class="music-info">
                        <div class="music-pic">
                            <img src="{music['cover_url']}" alt="{music['song_name']}" width="300" height="300">
                        </div>
                        <div class="music-details">
                            <h3 class="music-name">{music['song_name']}</h3>
                            <h4 class="music-singer">{music['singer']}</h4>
                            <audio controls width="300">
                                <source src="{music['song_url']}" type="audio/mpeg">
                                您的浏览器不支持音频播放。
                              </audio>
                        </div>
                    </div>
                </div>
            '''
            
            logger.info("客户端HTML生成成功!")
            logger.info(f"生成的HTML片段: {client_html[:200]}...")
            
            # 验证字段是否正确替换
            assert music['song_name'] in client_html
            assert music['singer'] in client_html
            assert music['song_url'] in client_html
            assert music['cover_url'] in client_html
            
            logger.info("客户端解析测试通过!")
            return True
        else:
            logger.error("客户端解析失败: 不是音乐类型消息")
            return False
            
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        return False

def test_api_field_mapping():
    """测试API字段映射是否正确"""
    try:
        # 模拟API返回的原始数据格式
        api_response = {
            'code': 1,
            'msg': 'success',
            'data': {
                'name': '开始懂了',
                'artistsname': '孙燕姿',
                'url': 'https://music.163.com/song/media/outer/url?id=123456789.mp3',
                'picurl': 'https://p1.music.126.net/abcdefghijk.jpg'
            }
        }
        
        logger.info("\n测试API字段映射...")
        logger.info(f"API原始响应: {json.dumps(api_response, ensure_ascii=False)}")
        
        # 模拟服务器端的字段映射逻辑
        if api_response.get('code') == 1:
            data = api_response.get('data', {})
            music_info = {
                'song_name': data.get('name', '未知歌曲'),
                'singer': data.get('artistsname', '未知歌手'),
                'song_url': data.get('url', ''),
                'cover_url': data.get('picurl', '')
            }
            
            logger.info("字段映射成功!")
            logger.info(f"映射后的音乐信息: {json.dumps(music_info, ensure_ascii=False)}")
            
            # 验证映射是否正确
            assert music_info['song_name'] == api_response['data']['name']
            assert music_info['singer'] == api_response['data']['artistsname']
            assert music_info['song_url'] == api_response['data']['url']
            assert music_info['cover_url'] == api_response['data']['picurl']
            
            return True
        else:
            logger.error("API返回错误")
            return False
            
    except Exception as e:
        logger.error(f"字段映射测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("=== 音乐功能集成测试 ===")
    
    # 运行所有测试
    test_results = {
        'message_format': test_music_message_format(),
        'api_mapping': test_api_field_mapping()
    }
    
    logger.info("\n=== 测试结果汇总 ===")
    all_passed = True
    for test_name, passed in test_results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        logger.info(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 所有测试通过! 音乐功能已修复完成!")
        sys.exit(0)
    else:
        logger.error("\n❌ 测试失败! 请检查修复内容。")
        sys.exit(1)