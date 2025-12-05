# 测试OpenAI客户端是否导致递归错误
import os
import sys
import logging
from config import AI_CONFIG
from openai import OpenAI

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_openai_client():
    try:
        logger.info("初始化OpenAI客户端")
        client = OpenAI(
            api_key=AI_CONFIG['api_key'],
            base_url=AI_CONFIG['api_url']
        )
        
        logger.info("测试OpenAI客户端是否正常工作")
        logger.info(f"客户端配置: api_key={AI_CONFIG['api_key'][:8]}..., base_url={AI_CONFIG['base_url']}")
        
        # 测试API调用
        logger.info("调用OpenAI API...")
        response = client.chat.completions.create(
            model=AI_CONFIG['model_name'],
            messages=[
                {
                    "role": "system",
                    "content": "你是伯小爵，一个友好的AI助手。请用简洁、友好的语言回答用户的问题。"
                },
                {
                    "role": "user",
                    "content": "你好"
                }
            ],
            stream=False
        )
        
        logger.info("API调用成功")
        logger.info(f"响应: {response}")
        
        return True
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("开始测试OpenAI客户端")
    result = test_openai_client()
    logger.info(f"测试结果: {'成功' if result else '失败'}")