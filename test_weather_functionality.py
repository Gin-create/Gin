import requests
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_weather_api():
    """测试天气API接口"""
    logger.info("=== 测试天气API接口 ===")
    
    # 测试城市列表
    cities = ["成都", "北京", "上海", "广州", "深圳"]
    
    for city in cities:
        logger.info(f"\n测试城市: {city}")
        
        try:
            # 构建请求URL
            url = f"http://localhost:5001/weather?city={city}"
            logger.info(f"请求URL: {url}")
            
            # 发送请求
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析响应
            data = response.json()
            logger.info(f"响应状态码: {response.status_code}")
            logger.info(f"响应数据: {data}")
            
            # 验证响应格式
            if data.get('code') == 200:
                logger.info(f"✅ 天气API请求成功，城市: {data.get('data', {}).get('city')}")
                logger.info(f"   天气数据数量: {len(data.get('data', {}).get('data', []))} 天")
            else:
                logger.error(f"❌ 天气API返回错误: {data.get('msg')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"❌ 处理响应失败: {str(e)}")
        
        # 避免请求过快
        time.sleep(1)

def test_weather_page():
    """测试天气页面"""
    logger.info("\n=== 测试天气页面 ===")
    
    city = "成都"
    url = f"http://localhost:5001/weather.html?city={city}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        logger.info(f"✅ 天气页面请求成功，状态码: {response.status_code}")
        logger.info(f"   页面大小: {len(response.text)} 字节")
        
        # 检查页面是否包含预期内容
        if '天气信息' in response.text and city in response.text:
            logger.info(f"✅ 天气页面包含预期内容")
        else:
            logger.warning(f"⚠️  天气页面内容可能不完整")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 天气页面请求失败: {str(e)}")

def test_integration():
    """综合测试"""
    logger.info("\n=== 综合测试 ===")
    
    try:
        # 测试服务器是否运行
        server_status = requests.get("http://localhost:5001", timeout=5)
        logger.info(f"✅ 服务器运行正常，状态码: {server_status.status_code}")
        
        # 运行所有测试
        test_weather_api()
        test_weather_page()
        
        logger.info("\n=== 所有测试完成 ===")
        
    except Exception as e:
        logger.error(f"❌ 综合测试失败: {str(e)}")

if __name__ == "__main__":
    test_integration()