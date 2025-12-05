import socketio
import requests
import time

# 创建一个Socket.IO客户端
sio = socketio.Client()

# 登录信息
login_url = 'http://localhost:5001/login'
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
    
    # 发送测试消息
    test_messages = [
        '普通消息测试',
        '@电影 https://example.com/movie',
        '@伯小爵 你好',
        '@音乐 周杰伦',
        '@天气 北京'
    ]
    
    for message in test_messages:
        print(f"发送消息: {message}")
        sio.emit('send_message', {'message': message})
        time.sleep(1)

# 接收消息事件
sio.on('receive_message')
def on_receive_message(data):
    print(f"接收消息: {data}")

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
        sio.connect('http://localhost:5001', headers={'Cookie': '; '.join([f'{k}={v}' for k, v in session.cookies.get_dict().items()])})
        
        # 保持连接
        sio.wait()
    else:
        print("登录失败")