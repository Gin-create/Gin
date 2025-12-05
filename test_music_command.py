import socketio
import time
import json

# 创建SocketIO客户端
sio = socketio.Client()

# 测试结果
music_response_received = False
music_response = None

# 事件处理
@sio.event
def connect():
    print('✅ 连接到服务器')
    # 发送音乐命令测试
    print('📤 发送@音乐命令...')
    sio.emit('send_message', {'message': '@音乐'})

@sio.event
def disconnect():
    print('❌ 与服务器断开连接')

@sio.event
def receive_message(data):
    global music_response_received, music_response
    print('📥 收到消息:', json.dumps(data, ensure_ascii=False, indent=2))
    if '伯小爵' in data.get('username', ''):
        music_response_received = True
        music_response = data
        # 收到响应后断开连接
        sio.disconnect()

# 连接到服务器
if __name__ == '__main__':
    try:
        print('🔄 正在连接到服务器...')
        sio.connect('http://127.0.0.1:5000')
        
        # 设置超时
        timeout = 10
        start_time = time.time()
        
        while not music_response_received and (time.time() - start_time) < timeout:
            time.sleep(0.5)
        
        if not music_response_received:
            print('⏰ 超时: 未收到音乐响应')
            sio.disconnect()
        else:
            # 检查响应内容
            message = music_response.get('message', '')
            if 'maximum recursion depth exceeded' in message:
                print('❌ 测试失败: 仍然存在递归错误')
            elif '抱歉，获取音乐失败' in message:
                print('❌ 测试失败: 获取音乐失败')
            elif '音乐' in message:
                print('✅ 测试成功: 音乐命令正常工作')
            else:
                print('⚠️  测试结果不明确')
                
    except Exception as e:
        print('❌ 错误:', e)