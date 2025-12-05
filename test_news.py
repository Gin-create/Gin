import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('已连接到服务器')
    sio.emit('send_message', {'username': 'test_user', 'message': '@新闻'})

@sio.event
def receive_message(data):
    print(f'收到消息: {data}')
    if data.get('type') == 'news':
        print('新闻功能测试成功!')
    elif '错误' in data.get('message', ''):
        print(f"新闻功能测试失败: {data.get('message')}")
    sio.disconnect()

@sio.event
def disconnect():
    print('已断开连接')

try:
    sio.connect('http://localhost:5001')
    time.sleep(10)  # 等待10秒，超时后自动断开
    print('测试超时')
except Exception as e:
    print(f'测试错误: {e}')
