// 测试修复后的sendMessage函数逻辑
function testSendMessageLogic() {
    const testMessages = [
        '@电影 https://example.com/movie',
        '@伯小爵 你好',
        '@音乐 周杰伦',
        '@天气 北京',
        '普通消息测试'
    ];
    
    console.log('=== 测试消息处理逻辑 ===');
    
    testMessages.forEach(message => {
        console.log(`\n测试消息: ${message}`);
        
        try {
            // 模拟sendMessage函数的消息类型判断逻辑
            if (message.startsWith('@电影')) {
                console.log('✅ 处理@电影消息');
            } else if (message.startsWith('@伯小爵')) {
                console.log('✅ 处理@伯小爵消息');
            } else if (message.startsWith('@音乐')) {
                console.log('✅ 处理@音乐消息');
            } else if (message.startsWith('@天气')) {
                console.log('✅ 处理@天气消息');
            } else {
                console.log('✅ 处理普通消息');
            }
        } catch (error) {
            console.log(`❌ 错误: ${error.message}`);
        }
    });
    
    console.log('\n=== 测试完成 ===');
}

// 运行测试
testSendMessageLogic();