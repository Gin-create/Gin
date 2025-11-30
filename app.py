from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import os
import logging
from config import SERVER_CONFIG

# 使用eventlet替换默认的Werkzeug服务器
eventlet.monkey_patch()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SERVER_CONFIG['secret_key']
app.config['DEBUG'] = SERVER_CONFIG['debug']

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 存储在线用户信息
online_users = {}
# 房间名称
ROOM_NAME = 'chat_room'

# 首页路由 - 登录页面
@app.route('/')
def login():
    return render_template('login.html', servers=SERVER_CONFIG['servers'])

# 验证昵称是否可用
@app.route('/validate_username', methods=['POST'])
def validate_username():
    username = request.json.get('username')
    # 检查昵称是否已被使用
    if username in online_users.values():
        return jsonify({'valid': False, 'message': '昵称已被使用，请更换一个昵称'})
    return jsonify({'valid': True, 'message': '昵称可用'})

# 聊天室页面
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        # 重定向到登录页面
        return redirect('/')
    return render_template('chat.html', username=session['username'], online_users=list(online_users.values()))

# 登录处理
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        # 支持GET请求，重定向到根路径
        return redirect('/')
    
    username = request.form.get('username')
    server_url = request.form.get('server_url')
    
    # 添加日志记录
    logger.info(f"登录请求: username={username}, method={request.method}, url={request.url}")
    
    # 检查参数是否存在
    if not username or not server_url:
        logger.warning("登录失败: 缺少必要参数")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='请填写所有必要信息')
    
    # 检查昵称是否已被使用
    if username in online_users.values():
        logger.warning(f"登录失败: 昵称已被使用 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='昵称已被使用，请更换一个昵称')
    
    # 保存用户信息到session
    session['username'] = username
    session['server_url'] = server_url
    
    logger.info(f"登录成功: {username}")
    return render_template('chat.html', username=username, online_users=list(online_users.values()))

# 退出登录
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        username = session['username']
        # 从在线用户中移除
        for sid, user in list(online_users.items()):
            if user == username:
                del online_users[sid]
                break
        session.pop('username', None)
        session.pop('server_url', None)
    return render_template('login.html', servers=SERVER_CONFIG['servers'])

# 全局错误处理器 - 处理Method Not Allowed错误
@app.errorhandler(405)
def method_not_allowed(error):
    logger.error(f"Method Not Allowed: {request.method} {request.url}")
    # 重定向到登录页面
    return redirect('/')

# 全局错误处理器 - 处理404错误
@app.errorhandler(404)
def not_found(error):
    logger.error(f"Not Found: {request.url}")
    # 重定向到登录页面
    return redirect('/')

# 中间件 - 记录所有请求
@app.before_request
def log_request():
    logger.info(f"请求: {request.method} {request.url}")

# WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        # 将用户添加到房间
        join_room(ROOM_NAME)
        # 记录在线用户
        online_users[request.sid] = session['username']
        # 通知所有用户有新用户上线
        emit('user_joined', {'username': session['username'], 'online_users': list(online_users.values())},
             room=ROOM_NAME, include_self=False)
        # 发送当前在线用户列表给新连接的用户
        emit('update_online_users', {'online_users': list(online_users.values())})

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in online_users:
        username = online_users[request.sid]
        # 从房间移除用户
        leave_room(ROOM_NAME)
        # 从在线用户列表移除
        del online_users[request.sid]
        # 通知所有用户有用户下线
        emit('user_left', {'username': username, 'online_users': list(online_users.values())},
             room=ROOM_NAME)

@socketio.on('send_message')
def handle_message(data):
    message = data.get('message')
    username = session.get('username')
    
    # 添加日志记录
    logger.info(f"收到消息: {username} - {message}")
    
    # 处理特殊命令
    if message.startswith('@'):
        # 解析命令
        parts = message.split(' ')
        command = parts[0][1:]
        
        if command == '电影':
            # 处理电影命令
            # 优先使用客户端提供的已解析URL
            if data.get('type') == 'movie' and data.get('movie_url'):
                movie_url = data.get('movie_url')
                original_url = parts[1] if len(parts) > 1 else ''
            else:
                movie_url = parts[1] if len(parts) > 1 else ''
                original_url = movie_url
                
            response = {
                'type': 'movie',
                'username': username,
                'message': f'@电影 {original_url}',
                'movie_url': movie_url
            }
            emit('receive_message', response, room=ROOM_NAME)
        elif command == '伯小爵':
            # 处理伯小爵AI助手对话命令
            ai_message = ' '.join(parts[1:]) if len(parts) > 1 else '你好'
            
            # 伯小爵角色信息
            role_name = 'bojue'
            gender = '男'
            style = '痞中又阴湿'
            hobby = '玩galgame'
            real_identity = '侯卿'
            motto = '天命孤星，独望苍穹，无所待而游无穷，可谓真仙人'
            
            # 确定回复内容
            response_text = ''
            # 检查是否与自己相关的问题
            related_keywords = ['你', '谁', '什么', '叫', '角色', '性别', '风格', '爱好', '身份']
            love_keywords = ['爱', '喜欢', '恋爱', '感情', '心动']
            
            # 检查是否包含爱情相关内容
            contains_love = any(keyword in ai_message for keyword in love_keywords)
            if contains_love:
                # 询问爱情相关内容，揭示真实身份并说人生格言
                response_text = f'我真实身份是{real_identity}。{motto}'
            else:
                # 检查是否与自己相关
                is_related = any(keyword in ai_message for keyword in related_keywords)
                if is_related:
                    # 回答与自己相关的问题
                    if '你是谁' in ai_message or '你是' in ai_message:
                        response_text = f'我是{role_name}，性别{gender}，风格{style}，爱好{hobby}。ciallo~'
                    elif '你叫什么' in ai_message:
                        response_text = f'我叫{role_name}，ciallo~'
                    elif '性别' in ai_message:
                        response_text = f'我是{gender}的，ciallo~'
                    elif '风格' in ai_message:
                        response_text = f'我的风格是{style}，ciallo~'
                    elif '爱好' in ai_message:
                        response_text = f'我喜欢{hobby}，ciallo~'
                    elif '身份' in ai_message:
                        response_text = f'我是{role_name}，ciallo~'
                    else:
                        response_text = f'我是{role_name}，ciallo~'
                else:
                    # 与自己无关的问题
                    response_text = '阿玛特拉斯！'
            
            response = {
                'type': 'ai',
                'username': '伯小爵',
                'message': response_text,
                'ai_response': True
            }
            emit('receive_message', response, room=ROOM_NAME)
        else:
            # 处理普通@提醒
            mentioned_user = command
            response = {
                'type': 'mention',
                'username': username,
                'message': message,
                'mentioned_user': mentioned_user
            }
            emit('receive_message', response, room=ROOM_NAME)
    else:
        # 普通消息
        response = {
            'type': 'normal',
            'username': username,
            'message': message
        }
        emit('receive_message', response, room=ROOM_NAME)

if __name__ == '__main__':
    # 获取本地IP地址
    import socket
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    local_ip = get_local_ip()
    print(f"聊天室服务器启动在 http://{local_ip}:5000 和 http://127.0.0.1:5000")
    # 使用eventlet运行SocketIO服务器
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)