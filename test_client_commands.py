# 测试客户端sendMessage函数的@指令处理逻辑

# 辅助函数：模拟JavaScript的字符串方法
def startsWith(s, prefix):
    return s.startswith(prefix)

def substring(s, start, end=None):
    if end is None:
        return s[start:]
    return s[start:end]

def trim(s):
    return s.strip()

def encodeURIComponent(s):
    import urllib.parse
    return urllib.parse.quote(s)

# 模拟客户端的sendMessage函数逻辑
# 这里我们只测试消息类型判断和参数构造，不实际发送

def test_send_message_logic(message):
    print(f"\n测试消息: {message}")
    result = {}
    
    # 检查是否是@电影消息
    if startsWith(message, '@电影'):
        print("✓ 识别为@电影消息")
        # 提取URL并发送电影消息
        url = trim(substring(message, 4))
        if url:
            result = { 
                'message': message,
                'type': 'movie',
                'movie_url': f"https://jx.m3u8.tv/jiexi/?url={encodeURIComponent(url)}"
            }
        else:
            result = { 'message': message }
    elif startsWith(message, '@伯小爵'):
        print("✓ 识别为@伯小爵AI助手消息")
        result = { 
            'message': message,
            'type': 'ai',
            'ai_mention': True
        }
    elif startsWith(message, '@音乐'):
        print("✓ 识别为@音乐命令")
        result = { 
            'message': message,
            'type': 'music'
        }
    elif startsWith(message, '@天气'):
        print("✓ 识别为@天气查询命令")
        city = trim(substring(message, 4))
        if city:
            result = { 
                'message': message,
                'type': 'weather',
                'city': city
            }
        else:
            result = { 'message': message }
    elif startsWith(message, '@新闻'):
        print("✓ 识别为@新闻查询命令")
        result = { 
            'message': message,
            'type': 'news'
        }
    elif startsWith(message, '@'):
        print("✓ 识别为其他@提醒命令")
        result = { 
            'message': message,
            'type': 'mention'
        }
    else:
        print("✓ 识别为普通消息")
        result = { 'message': message }
    
    print(f"构造的发送参数: {result}")
    return result

# 测试所有@指令
test_commands = [
    '@电影 https://example.com/movie',
    '@伯小爵 你好',
    '@音乐 周杰伦',
    '@天气 北京',
    '@新闻',
    '@提醒 测试',
    '普通消息测试'
]

print("=== 测试客户端@指令处理逻辑 ===")
for command in test_commands:
    test_send_message_logic(command)

print("\n=== 测试完成 ===")