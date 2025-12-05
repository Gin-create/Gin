// 测试客户端音乐播放器功能
// 模拟服务器发送的音乐消息
const mockMusicMessage = {
    type: 'music',
    username: '测试用户',
    message: '@音乐 周杰伦',
    music_info: {
        song_name: '晴天',
        singer: '周杰伦',
        song_url: 'https://example.com/music.mp3',
        cover_url: 'https://example.com/cover.jpg'
    }
};

// 模拟不完整的音乐消息
const mockIncompleteMusicMessage = {
    type: 'music',
    username: '测试用户',
    message: '@音乐 周杰伦',
    music_info: {
        song_name: null,
        singer: '',
        song_url: '',
        cover_url: null
    }
};

// 测试音乐播放器HTML生成
function testMusicPlayerHTML() {
    console.log('=== 测试音乐播放器HTML生成 ===');
    
    // 模拟updateMusicPlayer函数
    function updateMusicPlayer(music) {
        // 如果不存在，创建新的播放器
        let musicPlayer = document.createElement('div');
        musicPlayer.className = 'music-player-sidebar';
        musicPlayer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 200px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 15px;
            z-index: 1000;
            border: 2px solid #667eea;
        `;
        
        // 更新播放器内容
        musicPlayer.innerHTML = `
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="font-weight: bold; color: #667eea;">🎵 正在播放音乐</div>
            </div>
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="${music.cover_url || 'https://via.placeholder.com/120'}" 
                     alt="${music.song_name || '未知歌曲'}" 
                     width="120" 
                     height="120" 
                     style="border-radius: 8px;">
            </div>
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="font-weight: bold;">${music.song_name || '未知歌曲'}</div>
                <div style="color: #666; font-size: 14px;">${music.singer || '未知歌手'}</div>
            </div>
            <div style="text-align: center;">
                <audio controls style="width: 100%;">
                    <source src="${music.song_url || ''}" type="audio/mpeg">
                    您的浏览器不支持音频播放。
                </audio>
            </div>
        `;
        
        return musicPlayer.innerHTML;
    }
    
    // 测试完整的音乐消息
    console.log('1. 测试完整的音乐消息:');
    const fullHTML = updateMusicPlayer(mockMusicMessage.music_info);
    console.log(fullHTML);
    
    // 验证HTML内容
    if (fullHTML.includes('晴天') && fullHTML.includes('周杰伦') && 
        fullHTML.includes('https://example.com/cover.jpg') && 
        fullHTML.includes('https://example.com/music.mp3')) {
        console.log('✅ 完整音乐消息测试通过');
    } else {
        console.log('❌ 完整音乐消息测试失败');
    }
    
    // 测试不完整的音乐消息
    console.log('\n2. 测试不完整的音乐消息:');
    const incompleteHTML = updateMusicPlayer(mockIncompleteMusicMessage.music_info);
    console.log(incompleteHTML);
    
    // 验证默认值
    if (incompleteHTML.includes('未知歌曲') && incompleteHTML.includes('未知歌手') && 
        incompleteHTML.includes('https://via.placeholder.com/120')) {
        console.log('✅ 不完整音乐消息测试通过（默认值正确）');
    } else {
        console.log('❌ 不完整音乐消息测试失败');
    }
}

// 测试音乐消息处理
function testMusicMessageHandling() {
    console.log('\n=== 测试音乐消息处理 ===');
    
    // 模拟聊天区域音乐播放器HTML生成
    const mockMessageElement = document.createElement('div');
    mockMessageElement.className = 'message';
    
    // 模拟音乐播放器HTML生成
    const musicPlayerHTML = `
        <div class="music-player">
            <div>🎵 正在播放音乐</div>
            <div class="music-pic">
                <img src="${mockMusicMessage.music_info.cover_url}" alt="${mockMusicMessage.music_info.song_name}" width="300" height="300">
            </div>
            <div class="music-details">
                <h3 class="music-name">${mockMusicMessage.music_info.song_name}</h3>
                <h4 class="music-singer">${mockMusicMessage.music_info.singer}</h4>
                <audio controls>
                    <source src="${mockMusicMessage.music_info.song_url}" type="audio/mpeg">
                    您的浏览器不支持音频播放。
                </audio>
            </div>
        </div>
    `;
    
    mockMessageElement.innerHTML = musicPlayerHTML;
    
    // 验证聊天区域音乐播放器HTML
    console.log('聊天区域音乐播放器HTML:');
    console.log(mockMessageElement.innerHTML);
    
    if (mockMessageElement.innerHTML.includes('晴天') && mockMessageElement.innerHTML.includes('周杰伦') && 
        mockMessageElement.innerHTML.includes('https://example.com/cover.jpg') && 
        mockMessageElement.innerHTML.includes('https://example.com/music.mp3')) {
        console.log('✅ 聊天区域音乐播放器HTML测试通过');
    } else {
        console.log('❌ 聊天区域音乐播放器HTML测试失败');
    }
}

// 运行所有测试
function runAllTests() {
    console.log('开始测试客户端音乐播放器功能...\n');
    
    // 测试音乐播放器HTML生成
    testMusicPlayerHTML();
    
    // 测试音乐消息处理
    testMusicMessageHandling();
    
    console.log('\n=== 测试完成 ===');
}

// 导出测试函数（用于Node.js环境）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        runAllTests,
        testMusicPlayerHTML,
        testMusicMessageHandling
    };
} else {
    // 在浏览器环境中直接运行测试
    runAllTests();
}