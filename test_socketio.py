import socketio
import time

# 创建Socket.IO客户端
sio = socketio.Client()

# 连接事件回调
@sio.event
def connect():
    print('连接成功！')
    # 发送测试消息
    sio.emit('send_message', {"message": "测试消息 - Socket.IO连接正常"})

# 接收消息事件回调
@sio.event
def receive_message(data):
    print(f'收到消息: {data}')

# 连接错误事件回调
@sio.event
def connect_error(e):
    print(f'连接失败: {e}')

# 断开连接事件回调
@sio.event
def disconnect():
    print('断开连接')

# 连接到服务器
try:
    sio.connect('http://localhost:5001')
    # 保持连接2秒
    time.sleep(2)
    # 断开连接
    sio.disconnect()
except Exception as e:
    print(f'测试失败: {e}')
