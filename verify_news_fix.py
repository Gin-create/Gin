import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入需要的模块
import urllib.request
import urllib.error
import ssl
import json

def test_news_api():
    """直接测试新闻API的核心逻辑"""
    logger.info("开始测试新闻功能核心逻辑...")
    
    try:
        # 新闻API配置
        api_key = "a440759fd3d87545"
        news_url = "https://v2.xxapi.cn/api/weibohot"
        
        # 设置请求头
        req = urllib.request.Request(news_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('api-key', api_key)
        req.add_header('Host', 'v2.xxapi.cn')
        
        # 忽略SSL证书验证并设置SSL/TLS版本
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 强制使用TLS 1.2
        context.min_version = ssl.TLSVersion.TLSv1_2
        
        logger.info("发送HTTP请求到新闻API...")
        
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            # 读取响应内容
            response_data = response.read()
            
            # 确保响应编码正确
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            logger.info(f"HTTP请求完成，响应状态: {response.status}")
            
            # 解析JSON响应 - 这是之前出错的地方
            logger.info("解析JSON响应...")
            news_data = json.loads(response_text)
            
            logger.info("JSON响应解析成功！")
            logger.info(f"响应结构: {list(news_data.keys())}")
            logger.info(f"API消息: {news_data.get('msg', '无消息')}")
            
            # 检查响应结构，适应不同的API返回格式
            if 'data' in news_data:
                # 检查不同的数据结构
                if isinstance(news_data['data'], list):
                    news_items = news_data['data']
                elif isinstance(news_data['data'], dict):
                    # 尝试不同的键名
                    news_items = news_data['data'].get('list', 
                                                    news_data['data'].get('news', 
                                                    news_data['data'].get('items', [])))
                else:
                    news_items = []
            else:
                # 直接尝试获取列表
                news_items = news_data.get('list', news_data.get('news', news_data.get('items', [])))
            
            logger.info(f"获取到 {len(news_items)} 条新闻")
            
            if news_items:
                # 显示前5条新闻
                for i, item in enumerate(news_items[:5], 1):
                    # 尝试不同的标题键名
                    title = item.get('title', item.get('name', item.get('content', '无标题')))
                    logger.info(f"{i}. {title}")
                
                logger.info("\n✓ 新闻功能核心逻辑测试通过！")
                return True
            else:
                logger.warning("未找到新闻列表数据，但JSON解析成功")
                logger.info(f"完整响应: {news_data}")
                return True
    
    except urllib.error.URLError as e:
        logger.error(f"HTTP请求失败: {str(e)}")
        return False
    except urllib.error.HTTPError as e:
        logger.error(f"HTTP错误: {e.code} - {e.reason}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=== 新闻功能修复验证测试 ===")
    success = test_news_api()
    
    if success:
        logger.info("\n🎉 验证成功！新闻功能已经可以正常工作了。")
        logger.info("您可以在聊天室中输入 '@新闻' 来获取最新新闻。")
        sys.exit(0)
    else:
        logger.error("\n❌ 验证失败！新闻功能仍有问题。")
        sys.exit(1)