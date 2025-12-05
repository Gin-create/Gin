import socketio
import time

# 创建SocketIO客户端
sio = socketio.Client()
connected = False
received_message = None

try:
    @sio.event
    def connect():
        global connected
        print("已连接到服务器")
        connected = True
        
        # 连接成功后发送@新闻命令
        print("发送@新闻命令...")
        sio.emit('send_message', {
            'username': '测试用户',
            'message': '@新闻'
        })
    
    @sio.event
    def receive_message(data):
        global received_message
        print(f"收到消息: {data['message']}")
        received_message = data['message']
    
    @sio.event
    def disconnect():
        print("已断开与服务器的连接")
    
    @sio.event
    def connect_error(err):
        print(f"连接失败: {err}")
    
    # 连接到服务器
    print("正在连接到服务器...")
    sio.connect('http://localhost:5001')
    
    # 等待最多10秒获取新闻
    timeout = 10
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if received_message:
            if "新闻" in received_message and "成功" in received_message:
                print("\n✅ 新闻功能测试成功！")
                print(f"📰 新闻内容: {received_message}")
            elif "抱歉" in received_message or "失败" in received_message:
                print(f"\n❌ 新闻功能测试失败: {received_message}")
            else:
                print(f"\n⚠️  收到消息但内容不符合预期: {received_message}")
            break
        time.sleep(0.5)
    
    if not received_message:
        print("\n⏰ 超时: 未在10秒内收到新闻消息")
        
finally:
    # 断开连接
    if sio.connected:
        sio.disconnect()