#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('music_api_test.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('MusicAPITest')


def test_music_api():
    """测试音乐API调用功能"""
    try:
        logger.info("开始测试音乐API调用")
        
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
        full_url = f"https://{api_ip}{api_path}?{query_string}"
        
        logger.info(f"API URL: {full_url}")
        
        # 设置请求头
        req = urllib.request.Request(full_url)
        req.add_header("api-key", api_key)
        req.add_header("Host", "api.qqsuu.cn")  # 必须设置Host头
        req.add_header("User-Agent", "Mozilla/5.0")
        
        logger.info(f"请求头: {dict(req.headers)}")
        
        # 忽略SSL证书验证
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # 发送请求
        logger.info("发送HTTP请求...")
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            logger.info(f"HTTP响应状态: {response.status}")
            
            # 读取响应内容
            response_data = response.read()
            
            # 确保响应编码正确
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            logger.info(f"响应内容长度: {len(response_text)} 字节")
            logger.info(f"响应内容: {response_text}")
            
            # 解析JSON数据
            music_data = json.loads(response_text)
            logger.info(f"JSON解析成功，数据结构: {json.dumps(music_data, ensure_ascii=False, indent=2)}")
            
            # 检查响应格式
            if music_data.get('code') == 1:
                logger.info("音乐API调用成功!")
                logger.info(f"歌曲名: {music_data.get('song')}")
                logger.info(f"歌手: {music_data.get('singer')}")
                logger.info(f"歌曲URL: {music_data.get('url')}")
                logger.info(f"专辑封面: {music_data.get('cover')}")
                return True
            else:
                logger.error(f"音乐API返回错误: {music_data.get('msg', '未知错误')}")
                return False
                
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        logger.error(f"HTTP请求失败: {str(e)}", exc_info=True)
        return False
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"测试过程中发生未知错误: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("=== 音乐API测试开始 ===")
    
    success = test_music_api()
    
    if success:
        logger.info("=== 音乐API测试成功 ===")
        sys.exit(0)
    else:
        logger.error("=== 音乐API测试失败 ===")
        sys.exit(1)