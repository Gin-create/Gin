import socketio
import time
import requests

# 创建一个会话对象，用于维护登录状态
session = requests.Session()

# 先进行登录，获取session
login_url = 'http://localhost:5001/login'
login_data = {
    'username': 'gin',
    'password': 'gin',
    'server_url': 'http://localhost:5001'
}

response = session.post(login_url, data=login_data)
print(f'登录状态码: {response.status_code}')
print(f'登录响应: {response.text[:200]}...')  # 只打印前200个字符，避免输出过长

# 获取cookies
cookies = session.cookies.get_dict()
print(f'登录Cookies: {cookies}')

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

# 接收ai_start事件处理函数
@sio.on('ai_start')
def handle_ai_start(data):
    print('收到ai_start事件:', data)

# 接收ai_stream事件处理函数
@sio.on('ai_stream')
def handle_ai_stream(data):
    print('收到ai_stream事件:', data)

# 接收ai_end事件处理函数
@sio.on('ai_end')
def handle_ai_end(data):
    print('收到ai_end事件:', data)

# 接收ai_error事件处理函数
@sio.on('ai_error')
def handle_ai_error(data):
    print('收到ai_error事件:', data)

# 运行测试
try:
    # 连接到服务器，使用登录后的cookies
    print('尝试连接到服务器...')
    
    # 构建Cookie头
    cookie_header = ''
    for key, value in cookies.items():
        cookie_header += f'{key}={value}; '
    
    # 使用headers参数传递Cookie
    sio.connect('http://localhost:5001', headers={'Cookie': cookie_header})
    
    # 保持连接5秒，以便接收响应
    time.sleep(5)
    
    # 断开连接
    sio.disconnect()
    print('测试完成')
except Exception as e:
    print(f'测试失败: {e}')