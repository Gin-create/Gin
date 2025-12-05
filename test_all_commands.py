import socketio
import requests
import time

# 创建一个Socket.IO客户端
sio = socketio.Client()

# 登录信息
login_url = 'http://localhost:5002/login'
login_data = {
    'username': 'gin',
    'password': '123456'
}

# 创建会话
session = requests.Session()

# 登录
def login():
    print("正在登录...")
    response = session.post(login_url, data=login_data)
    print(f"登录状态码: {response.status_code}")
    print(f"登录Cookies: {session.cookies.get_dict()}")
    return response.status_code == 200

# 连接事件
sio.on('connect')
def on_connect():
    print("Socket.IO连接成功")
    
    # 测试所有@指令
    test_commands = [
        '@电影 https://example.com/movie',
        '@伯小爵 你好',
        '@音乐 周杰伦',
        '@天气 北京',
        '@新闻',
        '@提醒 测试'
    ]
    
    for command in test_commands:
        print(f"\n发送指令: {command}")
        sio.emit('send_message', {'message': command})
        time.sleep(2)  # 等待2秒接收响应

# 接收消息事件
sio.on('receive_message')
def on_receive_message(data):
    print(f"\n接收消息:")
    print(f"  类型: {data.get('type')}")
    print(f"  用户名: {data.get('username')}")
    print(f"  消息内容: {data.get('message')}")
    
    # 打印特定类型消息的附加信息
    if data.get('type') == 'movie':
        print(f"  电影URL: {data.get('movie_url')}")
    elif data.get('type') == 'music':
        music_info = data.get('music_info', {})
        print(f"  音乐信息: {music_info}")
    elif data.get('type') == 'weather':
        print(f"  城市: {data.get('city')}")
    elif data.get('type') == 'news':
        news_list = data.get('news_list', [])
        print(f"  新闻数量: {len(news_list)}")
        if news_list:
            print(f"  第一条新闻: {news_list[0]}")
    elif data.get('type') == 'mention':
        print(f"  提及用户: {data.get('mentioned_user')}")
    elif data.get('type') == 'ai':
        print(f"  AI响应: {data.get('message')}")

# 连接错误事件
sio.on('connect_error')
def on_connect_error(error):
    print(f"连接错误: {error}")

# 断开连接事件
sio.on('disconnect')
def on_disconnect():
    print("Socket.IO连接断开")

# 主函数
if __name__ == '__main__':
    if login():
        print("登录成功，正在连接Socket.IO...")
        
        # 使用会话Cookies连接Socket.IO
        cookies = '; '.join([f'{k}={v}' for k, v in session.cookies.get_dict().items()])
        sio.connect('http://localhost:5002', headers={'Cookie': cookies})
        
        # 保持连接15秒
        time.sleep(15)
        sio.disconnect()
        print("测试完成")
    else:
        print("登录失败")