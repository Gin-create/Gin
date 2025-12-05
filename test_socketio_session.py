import socketio
import requests
import time

# 创建一个会话对象，用于维护登录状态
session = requests.Session()

# 先进行登录，获取session
login_url = 'http://localhost:5001/login'

# 登录数据
login_data = {
    'username': 'gin',
    'password': '123456',
    'server_url': 'http://localhost:5001'
}

# 发送登录请求
response = session.post(login_url, data=login_data, allow_redirects=False)
print(f'登录状态码: {response.status_code}')
print(f'登录响应头: {dict(response.headers)}')
print(f'登录Cookies: {dict(session.cookies)}')

# 创建Socket.IO客户端实例
sio = socketio.Client(logger=True, engineio_logger=True)

# 连接事件处理函数
@sio.event
def connect():
    print('成功连接到服务器')
    # 连接成功后发送测试消息
    try:
        sio.emit('send_message', {'message': '测试消息'})
        print('已发送测试消息')
    except Exception as e:
        print(f'发送消息失败: {e}')

# 断开连接事件处理函数
@sio.event
def disconnect():
    print('与服务器断开连接')

# 接收消息事件处理函数
@sio.on('receive_message')
def receive_message(data):
    print('收到消息:', data)

# 运行测试
try:
    # 构建Cookie头
    cookie_header = ''
    for key, value in session.cookies.items():
        cookie_header += f'{key}={value}; '
    
    # 使用headers参数传递Cookie
    sio.connect('http://localhost:5001', headers={'Cookie': cookie_header})
    
    # 保持连接10秒，以便接收响应
    time.sleep(10)
    
    # 断开连接
    sio.disconnect()
    print('测试完成')
except Exception as e:
    print(f'测试失败: {e}')