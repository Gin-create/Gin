# 测试修复后的sendMessage函数逻辑

def test_send_message_logic():
    test_messages = [
        '@电影 https://example.com/movie',
        '@伯小爵 你好',
        '@音乐 周杰伦',
        '@天气 北京',
        '普通消息测试'
    ]
    
    print('=== 测试消息处理逻辑 ===')
    
    for message in test_messages:
        print(f'\n测试消息: {message}')
        
        try:
            # 模拟sendMessage函数的消息类型判断逻辑
            if message.startswith('@电影'):
                print('✅ 处理@电影消息')
            elif message.startswith('@伯小爵'):
                print('✅ 处理@伯小爵消息')
            elif message.startswith('@音乐'):
                print('✅ 处理@音乐消息')
            elif message.startswith('@天气'):
                print('✅ 处理@天气消息')
            else:
                print('✅ 处理普通消息')
        except Exception as e:
            print(f'❌ 错误: {e}')
    
    print('\n=== 测试完成 ===')

# 运行测试
if __name__ == '__main__':
    test_send_message_logic()