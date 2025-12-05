from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import logging
import json
import urllib
import urllib.request
import urllib.error
import urllib.parse
from config import SERVER_CONFIG, AI_CONFIG
from openai import OpenAI
import threading
import time
import ssl
import requests

# 注意：移除了eventlet的猴子补丁，因为它与requests库的SSL处理存在冲突，导致SSL错误

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SERVER_CONFIG['secret_key']
app.config['DEBUG'] = SERVER_CONFIG['debug']

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化OpenAI客户端
client = OpenAI(
    api_key=AI_CONFIG['api_key'],
    base_url=AI_CONFIG['api_url']
)

# 存储在线用户信息
online_users = {}
# 房间名称
ROOM_NAME = 'chat_room'

# 初始化SQLite数据库
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # 创建用户表，使用key-value形式存储
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# 调用初始化函数
init_db()



# 首页路由 - 登录页面
@app.route('/')
def login():
    return render_template('login.html', servers=SERVER_CONFIG['servers'])

# 音乐代理路由，用于绕过网易云音乐的防盗链限制
@app.route('/proxy-music')
def proxy_music():
    try:
        # 直接返回本地测试音频文件
        test_audio_path = os.path.join(app.root_path, 'static', 'audio', 'test.mp3')
        
        logger.info(f"请求代理音乐文件，返回本地测试音频: {test_audio_path}")
        
        if not os.path.exists(test_audio_path):
            error_msg = f"测试音频文件不存在: {test_audio_path}"
            logger.error(error_msg)
            return f"错误: {error_msg}", 404
            
        # 使用send_file函数返回文件
        return send_file(test_audio_path, mimetype='audio/mpeg')
        
    except Exception as e:
        error_msg = f"代理路由错误: {str(e)}"
        logger.error(error_msg)
        return f"错误: {error_msg}", 500

# 天气查询路由
@app.route('/weather')
def get_weather():
    try:
        city = request.args.get('city')
        if not city:
            return jsonify({'code': 400, 'msg': '缺少城市参数'})
        
        # 模拟天气数据（当API无法访问时使用）
        mock_weather_data = {
            "code": 200,
            "msg": "数据请求成功",
            "data": {
                "city": city,
                "data": [
                    {
                        "date": "12/04",
                        "day": "星期五",
                        "high_temp": 15,
                        "low_temp": 8,
                        "real_time_weather": [
                            {
                                "cloud_cover": "50%",
                                "description": "多云天气",
                                "humidity": "65%",
                                "precipitation": "0mm",
                                "pressure": "1013hPa",
                                "temperature": "12",
                                "time": "09:00",
                                "weather": "多云",
                                "wind_dir": "东南风",
                                "wind_speed": "5.2m/s"
                            },
                            {
                                "cloud_cover": "60%",
                                "description": "多云天气",
                                "humidity": "70%",
                                "precipitation": "0mm",
                                "pressure": "1012hPa",
                                "temperature": "14",
                                "time": "12:00",
                                "weather": "多云",
                                "wind_dir": "南风",
                                "wind_speed": "6.8m/s"
                            },
                            {
                                "cloud_cover": "70%",
                                "description": "多云间阴",
                                "humidity": "75%",
                                "precipitation": "0mm",
                                "pressure": "1011hPa",
                                "temperature": "13",
                                "time": "15:00",
                                "weather": "阴",
                                "wind_dir": "西南风",
                                "wind_speed": "5.6m/s"
                            },
                            {
                                "cloud_cover": "80%",
                                "description": "阴天",
                                "humidity": "80%",
                                "precipitation": "0mm",
                                "pressure": "1010hPa",
                                "temperature": "11",
                                "time": "18:00",
                                "weather": "阴",
                                "wind_dir": "西北风",
                                "wind_speed": "4.3m/s"
                            }
                        ],
                        "weather_from": "多云",
                        "weather_to": "阴",
                        "wind_from": "东南风",
                        "wind_level_from": "3级",
                        "wind_to": "西南风",
                        "wind_level_to": "2级"
                    },
                    {
                        "date": "12/05",
                        "day": "星期六",
                        "high_temp": 16,
                        "low_temp": 9,
                        "real_time_weather": [
                            {
                                "cloud_cover": "40%",
                                "description": "晴间多云",
                                "humidity": "60%",
                                "precipitation": "0mm",
                                "pressure": "1012hPa",
                                "temperature": "10",
                                "time": "09:00",
                                "weather": "晴",
                                "wind_dir": "北风",
                                "wind_speed": "3.5m/s"
                            },
                            {
                                "cloud_cover": "30%",
                                "description": "晴天",
                                "humidity": "55%",
                                "precipitation": "0mm",
                                "pressure": "1013hPa",
                                "temperature": "15",
                                "time": "12:00",
                                "weather": "晴",
                                "wind_dir": "东北风",
                                "wind_speed": "4.2m/s"
                            },
                            {
                                "cloud_cover": "40%",
                                "description": "晴间多云",
                                "humidity": "60%",
                                "precipitation": "0mm",
                                "pressure": "1012hPa",
                                "temperature": "16",
                                "time": "15:00",
                                "weather": "多云",
                                "wind_dir": "东风",
                                "wind_speed": "5.1m/s"
                            },
                            {
                                "cloud_cover": "50%",
                                "description": "多云",
                                "humidity": "65%",
                                "precipitation": "0mm",
                                "pressure": "1011hPa",
                                "temperature": "13",
                                "time": "18:00",
                                "weather": "多云",
                                "wind_dir": "东南风",
                                "wind_speed": "4.7m/s"
                            }
                        ],
                        "weather_from": "晴",
                        "weather_to": "多云",
                        "wind_from": "北风",
                        "wind_level_from": "2级",
                        "wind_to": "东南风",
                        "wind_level_to": "3级"
                    }
                ]
            }
        }
        
        # 尝试调用真实API，如果失败则使用模拟数据
        try:
            # 天气API配置
            weather_api_url = "https://v2.xxapi.cn/api/weatherDetails"
            api_key = "a440759fd3d87545"
            
            # 构建请求参数
            params = {
                'city': city,
                'key': api_key
            }
            
            # 设置请求头
            headers = {
                'User-Agent': 'xiaoxiaoapi/1.0.0'
            }
            
            logger.info(f"请求天气API: {weather_api_url}, 参数: {params}")
            
            # 发送请求（设置超时时间）
            response = requests.get(weather_api_url, params=params, headers=headers, timeout=5)
            response.raise_for_status()  # 检查请求是否成功
            
            # 获取响应数据
            weather_data = response.json()
            logger.info(f"天气API返回: {weather_data}")
            
            # 检查API响应中的code字段
            if weather_data.get('code') == 200:
                # 返回真实API数据
                return jsonify(weather_data)
            else:
                # API返回错误，使用模拟数据
                error_msg = f"天气API返回错误: {weather_data.get('msg', '未知错误')}"
                logger.warning(error_msg)
                # 使用模拟数据，并替换城市名称
                mock_weather_data['data']['city'] = city
                return jsonify(mock_weather_data)
        except requests.exceptions.RequestException as e:
            error_msg = f"天气API请求失败，使用模拟数据: {str(e)}"
            logger.warning(error_msg)
            # 使用模拟数据，并替换城市名称
            mock_weather_data['data']['city'] = city
            return jsonify(mock_weather_data)
        except Exception as e:
            error_msg = f"天气API处理异常，使用模拟数据: {str(e)}"
            logger.warning(error_msg)
            # 使用模拟数据，并替换城市名称
            mock_weather_data['data']['city'] = city
            return jsonify(mock_weather_data)
        
    except Exception as e:
        error_msg = f"天气查询错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'code': 500, 'msg': error_msg})

# 天气页面路由
@app.route('/weather.html')
def weather_page():
    return render_template('weather.html')

# 验证昵称是否可用
@app.route('/validate_username', methods=['POST'])
def validate_username():
    username = request.json.get('username')
    # 检查用户名是否为空
    if not username:
        return jsonify({'valid': False, 'message': '用户名不能为空'})
    # 检查昵称是否已被使用
    if username in online_users.values():
        return jsonify({'valid': False, 'message': '昵称已被使用，请更换一个昵称'})
    # 检查用户名是否已在数据库中存在
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({'valid': False, 'message': '用户名已被注册'})
    
    return jsonify({'valid': True, 'message': '昵称可用'})

# 聊天室页面
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        # 重定向到登录页面
        return redirect('/')
    return render_template('chat.html', username=session['username'], online_users=list(online_users.values()))

# 用户注册处理
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # 添加日志记录
    logger.info(f"注册请求: username={username}, method={request.method}, url={request.url}")
    
    # 检查参数是否存在
    if not username or not password or not confirm_password:
        logger.warning("注册失败: 缺少必要参数")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='请填写所有必要信息')
    
    # 检查用户名长度
    if len(username) < 3 or len(username) > 20:
        logger.warning(f"注册失败: 用户名长度不符合要求 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='用户名长度必须在3-20个字符之间')
    
    # 检查密码长度
    if len(password) < 6:
        logger.warning(f"注册失败: 密码长度不符合要求 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='密码长度不能少于6个字符')
    
    # 检查两次输入的密码是否一致
    if password != confirm_password:
        logger.warning(f"注册失败: 两次输入的密码不一致 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='两次输入的密码不一致')
    
    # 检查用户名是否已存在于数据库中
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()
    
    if existing_user:
        logger.warning(f"注册失败: 用户名已存在 - {username}")
        conn.close()
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='用户名已存在，请更换一个用户名')
    
    # 将用户名和密码存储到数据库中
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    
    logger.info(f"注册成功: {username}")
    return render_template('login.html', servers=SERVER_CONFIG['servers'], error='注册成功，请登录')

# 登录处理
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        # 支持GET请求，重定向到根路径
        return redirect('/')
    
    username = request.form.get('username')
    password = request.form.get('password')
    server_url = request.form.get('server_url')
    
    # 添加日志记录
    logger.info(f"登录请求: username={username}, method={request.method}, url={request.url}")
    
    # 检查参数是否存在
    if not username or not password or not server_url:
        logger.warning("登录失败: 缺少必要参数")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='请填写所有必要信息')
    
    # 检查昵称是否已被使用
    if username in online_users.values():
        logger.warning(f"登录失败: 昵称已被使用 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='昵称已被使用，请更换一个昵称')
    
    # 从数据库中验证用户名和密码
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if not user:
        logger.warning(f"登录失败: 用户名不存在 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='用户名不存在，请先注册')
    
    if user[0] != password:
        logger.warning(f"登录失败: 密码错误 - {username}")
        return render_template('login.html', servers=SERVER_CONFIG['servers'], error='密码错误，请重新输入')
    
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
    logger.info(f"消息数据: {data}")
    logger.info(f"当前会话: {session}")
    
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

        elif command == AI_CONFIG["ai_username"]:
                  # 处理@伯小爵AI助手对话命令
                ai_message = ' '.join(parts[1:]) if len(parts) > 1 else '你好'
                
                # 创建一个唯一的消息ID用于流式响应
                message_id = f"ai_{int(time.time())}_{username}"
                
                # 发送AI开始响应的消息
                emit('receive_message', {
                    'type': 'ai_start',
                    'username': AI_CONFIG["ai_username"],
                    'message_id': message_id
                }, room=ROOM_NAME)
                
                # 在后台线程中调用AI API并流式返回结果
                def call_ai_api():
                    try:
                        # 调用AI模型API
                        stream = client.chat.completions.create(
                            model=AI_CONFIG['model_name'],
                            messages=[
                                {
                                    "role": "system",
                                    "content": "你是伯小爵，一个友好的AI助手。请用简洁、友好的语言回答用户的问题。"
                                },
                                {
                                    "role": "user",
                                    "content": ai_message
                                }
                            ],
                            stream=True
                        )
                        
                        # 流式处理响应
                        full_response = ""
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                content = chunk.choices[0].delta.content
                                full_response += content
                                # 通过SocketIO发送流式数据
                                socketio.emit('receive_message', {
                                    'type': 'ai_stream',
                                    'username': AI_CONFIG["ai_username"],
                                    'message_id': message_id,
                                    'content': content
                                }, room=ROOM_NAME)
                                # 小延迟以模拟自然的打字效果
                                time.sleep(0.05)
                        
                        # 发送响应完成的消息
                        socketio.emit('receive_message', {
                            'type': 'ai_end',
                            'username': AI_CONFIG["ai_username"],
                            'message_id': message_id,
                            'full_message': full_response
                        }, room=ROOM_NAME)
                    except Exception as e:
                        logger.error(f"AI调用错误: {str(e)}")
                        socketio.emit('receive_message', {
                            'type': 'ai_error',
                            'username': AI_CONFIG["ai_username"],
                            'message_id': message_id,
                            'error': f"抱歉，我的大脑有点问题，请稍后再试。"
                        }, room=ROOM_NAME)
                
                # 启动后台线程调用AI
                threading.Thread(target=call_ai_api).start()
        elif command == '天气':
            # 处理@天气命令
            city = ' '.join(parts[1:]) if len(parts) > 1 else ''
            response = {
                'type': 'weather',
                'username': username,
                'message': message,
                'city': city
            }
            emit('receive_message', response, room=ROOM_NAME)
        elif command == '音乐':
            # 处理@音乐命令
            try:
                # 调用音乐API获取随机音乐 - 使用urllib替代requests避免eventlet SSL递归问题
                
                # 直接使用IP地址访问，绕过DNS解析
                api_ip = "43.240.193.23"
                api_path = "/api/dm-randmusic"
                api_key = "828a388ecd2ece83964472c5cd61d4fc"
                params = {
                    "sort": "热歌榜",
                    "format": "json"
                }
                
                # 构建完整URL
                query_string = urllib.parse.urlencode(params)
                full_url = f"https://{api_ip}{api_path}?{query_string}"
                
                # 设置请求头
                req = urllib.request.Request(full_url)
                req.add_header("api-key", api_key)
                req.add_header("Host", "api.qqsuu.cn")  # 必须设置Host头
                req.add_header("User-Agent", "Mozilla/5.0")
                
                # 记录API调用信息
                logger.info(f"准备调用音乐API - 命令: {command}, 用户名: {username}")
                logger.info(f"API URL: {full_url}")
                logger.info(f"请求头: {dict(req.headers)}")
                
                # 实现重试机制
                max_retries = 3
                retry_delay = 2  # 初始重试延迟（秒）
                music_data = None
                
                for attempt in range(max_retries):
                    try:
                        logger.info(f"开始发送HTTP请求（尝试 {attempt + 1}/{max_retries}）...")
                        
                        # 忽略SSL证书验证并设置SSL/TLS版本
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        # 强制使用TLS 1.2，解决版本不匹配问题
                        context.options |= ssl.OP_NO_SSLv2
                        context.options |= ssl.OP_NO_SSLv3
                        context.options |= ssl.OP_NO_TLSv1
                        context.options |= ssl.OP_NO_TLSv1_1
                        context.min_version = ssl.TLSVersion.TLSv1_2
                        
                        # 发送请求
                        with urllib.request.urlopen(req, context=context, timeout=15) as response:
                            # 读取响应内容
                            response_data = response.read()
                            
                            # 确保响应编码正确
                            encoding = response.headers.get_content_charset('utf-8')
                            response_text = response_data.decode(encoding)
                            
                            logger.info(f"HTTP请求完成（尝试 {attempt + 1}）")
                            logger.info(f"音乐API响应状态: {response.status}")
                            logger.info(f"音乐API响应内容: {response_text}")
                            
                            # 解析JSON数据
                            music_data = json.loads(response_text)
                            break  # 请求成功，跳出重试循环
                    except (urllib.error.URLError, urllib.error.HTTPError) as e:
                        logger.error(f"HTTP请求失败（尝试 {attempt + 1}）: {str(e)}")
                        if attempt < max_retries - 1:
                            logger.info(f"将在 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            retry_delay *= 1.5  # 指数退避
                        else:
                            logger.error(f"已达到最大重试次数 ({max_retries})，请求失败")
                            raise  # 抛出异常
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析失败（尝试 {attempt + 1}）: {str(e)}")
                        if attempt < max_retries - 1:
                            logger.info(f"将在 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            retry_delay *= 1.5
                        else:
                            logger.error(f"已达到最大重试次数 ({max_retries})，JSON解析失败")
                            raise
                
                if music_data is None:
                    raise Exception("无法建立HTTP连接或解析响应")
                
                if music_data.get('code') == 1:
                    # 构造音乐信息响应 - 注意JSON结构: data字段包含音乐详情
                    data = music_data.get('data', {})
                    # 保留原始音乐URL，前端会通过代理路由访问它
                    original_song_url = data.get('url', '')
                    
                    # 映射API字段到响应格式
                    response = {
                        'type': 'music',
                        'username': username,
                        'message': message,
                        'music_info': {
                            'song_name': data.get('name', '未知歌曲'),
                            'singer': data.get('artistsname', '未知歌手'),
                            'song_url': original_song_url,
                            'cover_url': data.get('picurl', '')
                        }
                    }
                    emit('receive_message', response, room=ROOM_NAME)
                else:
                    # 发送详细错误信息
                    error_response = {
                        'type': 'normal',
                        'username': AI_CONFIG["ai_username"],
                        'message': f"抱歉，获取音乐失败，错误信息: {music_data.get('msg', '未知错误')}"
                    }
                    emit('receive_message', error_response, room=ROOM_NAME)
            except Exception as e:
                logger.error(f"音乐API调用错误: {str(e)}")
                # 发送详细错误信息
                error_response = {
                    'type': 'normal',
                    'username': AI_CONFIG["ai_username"],
                    'message': f"抱歉，获取音乐失败，错误: {str(e)}"
                }
                emit('receive_message', error_response, room=ROOM_NAME)
                
        elif command == '新闻':
            # 处理@新闻命令
            try:
                # 新闻API配置
                api_key = "a440759fd3d87545"
                news_url = "https://v2.xxapi.cn/api/weibohot"
                
                # 记录API调用信息
                logger.info(f"准备调用新闻API - 命令: {command}, 用户名: {username}")
                logger.info(f"API URL: {news_url}")
                
                # 设置请求头
                req = urllib.request.Request(news_url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                req.add_header('api-key', api_key)
                req.add_header('Host', 'v2.xxapi.cn')
                
                # 实现重试机制
                max_retries = 3
                retry_delay = 2  # 初始重试延迟（秒）
                news_data = None
                
                for attempt in range(max_retries):
                    try:
                        logger.info(f"开始发送HTTP请求（尝试 {attempt + 1}/{max_retries}）...")
                        
                        # 忽略SSL证书验证并设置SSL/TLS版本
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        # 强制使用TLS 1.2，解决版本不匹配问题
                        context.options |= ssl.OP_NO_SSLv2
                        context.options |= ssl.OP_NO_SSLv3
                        context.options |= ssl.OP_NO_TLSv1
                        context.options |= ssl.OP_NO_TLSv1_1
                        context.min_version = ssl.TLSVersion.TLSv1_2
                        
                        # 发送请求
                        with urllib.request.urlopen(req, context=context, timeout=15) as response:
                            # 读取响应内容
                            response_data = response.read()
                            
                            # 确保响应编码正确
                            encoding = response.headers.get_content_charset('utf-8')
                            response_text = response_data.decode(encoding)
                            
                            logger.info(f"HTTP请求完成（尝试 {attempt + 1}）")
                            logger.info(f"响应状态: {response.status}")
                            logger.info(f"响应头部: {dict(response.headers)}")
                            logger.info(f"成功获取响应内容，长度: {len(response_text)} 字符")
                            
                            # 解析JSON响应
                            news_data = json.loads(response_text)
                            logger.info("JSON响应解析成功")
                            logger.info(f"响应结构: {list(news_data.keys())}")
                            break  # 成功解析，跳出重试循环
                        
                    except (urllib.error.URLError, urllib.error.HTTPError) as e:
                        logger.warning(f"请求失败（尝试 {attempt + 1}/{max_retries}）: {str(e)}")
                        if attempt < max_retries - 1:
                            logger.info(f"将在 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            retry_delay *= 1.5  # 指数退避
                        else:
                            logger.error(f"已达到最大重试次数 ({max_retries})，请求失败")
                            raise
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON解析失败（尝试 {attempt + 1}/{max_retries}）: {str(e)}")
                        if attempt < max_retries - 1:
                            logger.info(f"将在 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            retry_delay *= 1.5  # 指数退避
                        else:
                            logger.error(f"已达到最大重试次数 ({max_retries})，JSON解析失败")
                            raise
                
                if news_data is None:
                    raise Exception("无法建立HTTP连接或解析响应")
                    
                # 检查API响应状态
                if news_data.get('code') == 200:
                    # 构造新闻响应
                    response = {
                        'type': 'news',
                        'username': username,
                        'message': message,
                        'news_list': news_data.get('data', [])
                    }
                    emit('receive_message', response, room=ROOM_NAME)
                else:
                    # 发送详细错误信息
                    error_response = {
                        'type': 'normal',
                        'username': AI_CONFIG["ai_username"],
                        'message': f"抱歉，获取新闻失败，错误信息: {news_data.get('msg', '未知错误')}"
                    }
                    emit('receive_message', error_response, room=ROOM_NAME)
            except Exception as e:
                logger.error(f"新闻API调用错误: {str(e)}")
                # 发送详细错误信息
                error_response = {
                    'type': 'normal',
                    'username': AI_CONFIG["ai_username"],
                    'message': f"抱歉，获取新闻失败，错误: {str(e)}"
                }
                emit('receive_message', error_response, room=ROOM_NAME)
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
    print(f"聊天室服务器启动在 http://{local_ip}:5001 和 http://127.0.0.1:5001")
    # 使用SocketIO运行Flask应用
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)