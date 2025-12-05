import requests
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_proxy_route():
    """测试代理路由的基本功能"""
    logger.info("测试代理路由的基本功能")
    
    # 使用一个简单的测试URL，比如百度首页
    test_url = "http://www.baidu.com"
    proxy_url = f"http://localhost:5000/proxy-music?url={test_url}"
    
    logger.info(f"测试URL: {test_url}")
    logger.info(f"代理URL: {proxy_url}")
    
    try:
        # 发送请求
        response = requests.get(proxy_url, timeout=5, verify=False)
        
        logger.info(f"代理路由响应状态码: {response.status_code}")
        logger.info(f"响应内容类型: {response.headers.get('Content-Type')}")
        logger.info(f"响应内容长度: {len(response.content)} 字节")
        
        # 打印前500个字符的响应内容
        logger.info(f"响应内容预览: {response.content[:500]}")
        
        return True
    except requests.exceptions.Timeout:
        logger.error("请求超时")
    except requests.exceptions.ConnectionError:
        logger.error("连接错误")
    except Exception as e:
        logger.error(f"发生错误: {e}")
    
    return False

if __name__ == "__main__":
    success = test_proxy_route()
    if success:
        logger.info("代理路由测试成功")
        sys.exit(0)
    else:
        logger.error("代理路由测试失败")
        sys.exit(1)