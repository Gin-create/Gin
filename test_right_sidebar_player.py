#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试右侧边栏音乐播放器功能
"""

import sys
import time
import logging
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 服务器配置
SERVER_URL = 'http://localhost:5000'

class MusicPlayerTest:
    def __init__(self):
        self.session = requests.Session()
        
    def test_login(self):
        """测试登录功能"""
        logger.info("测试登录功能...")
        try:
            # 访问登录页面获取CSRF令牌
            login_page = self.session.get(f'{SERVER_URL}/login')
            if login_page.status_code != 200:
                logger.error(f"访问登录页面失败: {login_page.status_code}")
                return False
            
            # 解析HTML获取表单数据
            soup = BeautifulSoup(login_page.text, 'html.parser')
            
            # 提交登录表单
            login_data = {
                'username': 'test_user',
                'password': 'test_password'
            }
            
            response = self.session.post(f'{SERVER_URL}/login', data=login_data)
            if response.status_code != 200:
                logger.error(f"登录失败: {response.status_code}")
                return False
            
            logger.info("登录成功!")
            return True
            
        except Exception as e:
            logger.error(f"登录测试失败: {str(e)}")
            return False
    
    def test_music_command(self):
        """测试音乐命令"""
        logger.info("测试音乐命令...")
        try:
            # 发送音乐命令
            music_command = '@音乐 随机'
            
            # 这里需要使用Socket.io协议来发送消息，我们使用简单的HTTP请求模拟
            # 实际上应该使用socket.io-client库
            
            logger.info(f"模拟发送音乐命令: {music_command}")
            logger.info("请在浏览器中手动测试右侧音乐播放器...")
            logger.info("查看浏览器控制台是否有JavaScript错误")
            
            return True
            
        except Exception as e:
            logger.error(f"音乐命令测试失败: {str(e)}")
            return False
    
    def test_chat_page(self):
        """测试聊天页面"""
        logger.info("测试聊天页面...")
        try:
            # 访问聊天页面
            chat_page = self.session.get(f'{SERVER_URL}/chat')
            if chat_page.status_code != 200:
                logger.error(f"访问聊天页面失败: {chat_page.status_code}")
                return False
            
            # 检查页面内容
            if 'DaiP智能聊天室' not in chat_page.text:
                logger.error("聊天页面内容不正确")
                return False
            
            # 检查是否包含音乐播放器相关代码
            music_related = [
                'music-player',
                '@音乐',
                '正在播放音乐'
            ]
            
            for keyword in music_related:
                if keyword in chat_page.text:
                    logger.info(f"页面包含音乐相关关键词: {keyword}")
            
            logger.info("聊天页面测试通过!")
            return True
            
        except Exception as e:
            logger.error(f"聊天页面测试失败: {str(e)}")
            return False

def main():
    logger.info("=== 右侧边栏音乐播放器测试 ===")
    
    test = MusicPlayerTest()
    
    if not test.test_login():
        sys.exit(1)
    
    if not test.test_chat_page():
        sys.exit(1)
    
    test.test_music_command()
    
    logger.info("\n=== 测试建议 ===")
    logger.info("1. 请在浏览器中打开 http://localhost:5000/chat")
    logger.info("2. 登录后发送 @音乐 命令")
    logger.info("3. 检查右侧音乐播放器是否显示正常")
    logger.info("4. 打开浏览器开发者工具，查看控制台是否有JavaScript错误")
    logger.info("5. 查看网络请求，检查音乐数据是否正确返回")
    
    logger.info("\n=== 可能的问题原因 ===")
    logger.info("1. 右侧音乐播放器可能由另一个JavaScript文件控制")
    logger.info("2. 可能存在未被捕获的JavaScript错误")
    logger.info("3. 可能是浏览器缓存导致的旧代码问题")
    logger.info("4. 可能存在独立的音乐播放状态管理逻辑")

if __name__ == "__main__":
    main()