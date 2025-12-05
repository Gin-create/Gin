import requests
import json

# 测试天气API调用
def test_weather_api():
    # API端点和参数
    city = "北京"
    weather_url = f"https://v2.xxapi.cn/api/tianqi?city={city}"
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'api-key': '16f4355035616f435503563b',
        'Host': 'v2.xxapi.cn'
    }
    
    try:
        print(f"正在请求天气API: {weather_url}")
        print(f"请求头: {headers}")
        
        # 发送请求
        response = requests.get(weather_url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)} 字符")
        
        # 解析JSON
        weather_data = response.json()
        print(f"\nJSON解析成功")
        print(f"响应结构: {list(weather_data.keys())}")
        
        # 打印完整响应
        print(f"\n完整响应内容:")
        print(json.dumps(weather_data, ensure_ascii=False, indent=2))
        
        # 检查API响应状态
        if weather_data.get('code') == 200:
            print(f"\nAPI调用成功")
            
            # 提取天气信息
            data = weather_data.get('data', {})
            print(f"\n天气信息:")
            print(f"城市: {data.get('city', '')}")
            print(f"日期: {data.get('date', '')}")
            print(f"天气: {data.get('weather', '')}")
            print(f"温度: {data.get('temp', '')}")
            print(f"风力: {data.get('wind', '')}")
            print(f"湿度: {data.get('humidity', '')}")
            print(f"空气质量: {data.get('air_quality', '')}")
        else:
            print(f"\nAPI调用失败: {weather_data.get('msg', '未知错误')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n请求失败: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"\nJSON解析失败: {str(e)}")
    except Exception as e:
        print(f"\n其他错误: {str(e)}")

if __name__ == "__main__":
    test_weather_api()