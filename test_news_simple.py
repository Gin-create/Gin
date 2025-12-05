import json
import urllib
import urllib.request
import urllib.error
import ssl
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_news_function():
    """直接测试新闻功能的核心逻辑"""
    try:
        logger.info("开始测试新闻功能...")
        
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
        # 强制使用TLS 1.2，解决版本不匹配问题
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.min_version = ssl.TLSVersion.TLSv1_2
        
        logger.info("发送HTTP请求...")
        
        # 发送请求
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            # 读取响应内容
            response_data = response.read()
            
            # 确保响应编码正确
            encoding = response.headers.get_content_charset('utf-8')
            response_text = response_data.decode(encoding)
            
            logger.info(f"HTTP请求完成，响应状态: {response.status}")
            
            # 解析JSON响应
            news_data = json.loads(response_text)
            logger.info("JSON响应解析成功")
            logger.info(f"响应结构: {list(news_data.keys())}")
            
            # 检查API响应状态
            if news_data.get('code') == 200:
                logger.info("新闻功能测试成功!")
                logger.info(f"获取到 {len(news_data.get('data', []))} 条新闻")
                
                # 打印前5条新闻标题
                for i, news in enumerate(news_data.get('data', [])[:5]):
                    logger.info(f"{i+1}. {news.get('title', '无标题')}")
                
                return True
            else:
                logger.error(f"新闻API返回错误: {news_data.get('msg', '未知错误')}")
                return False
    except Exception as e:
        logger.error(f"测试错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_news_function()
    if success:
        print("\n新闻功能测试通过!")
    else:
        print("\n新闻功能测试失败!")
