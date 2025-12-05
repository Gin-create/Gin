# 测试eventlet猴子补丁是否导致requests库递归错误
import eventlet
import requests
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_eventlet_requests():
    try:
        logger.info("应用eventlet猴子补丁")
        eventlet.monkey_patch()
        
        logger.info("测试requests库...")
        
        # 测试音乐API调用
        api_url = "https://43.240.193.23/api/dm-randmusic"
        api_key = "828a388ecd2ece83964472c5cd61d4fc"
        params = {
            "sort": "热歌榜",
            "format": "json"
        }
        headers = {
            "api-key": api_key,
            "Host": "api.qqsuu.cn"
        }
        
        logger.info(f"发送请求到 {api_url}")
        response = requests.get(
            api_url,
            params=params,
            headers=headers,
            timeout=15,
            verify=False
        )
        
        logger.info(f"响应状态: {response.status_code}")
        logger.info(f"响应内容: {response.text[:200]}...")
        
        # 尝试解析JSON
        json_data = response.json()
        logger.info(f"JSON解析成功: {json_data}")
        
        return True
    except RecursionError as e:
        logger.error(f"递归错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        logger.error(f"其他错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("开始测试eventlet猴子补丁与requests库")
    result = test_eventlet_requests()
    logger.info(f"测试结果: {'成功' if result else '失败'}")