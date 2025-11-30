document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const messageArea = document.getElementById('message-area');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const logoutButton = document.getElementById('logout-button');
    const emojiBtn = document.getElementById('emoji-btn');
    const emojiPicker = document.getElementById('emoji-picker');
    const movieBtn = document.getElementById('movie-btn');
    const aiBtn = document.getElementById('ai-btn');
    
    // 获取当前用户名（从HTML中解析）
    const currentUsername = document.querySelector('.user-info span').textContent.replace('当前用户: ', '');
    
    // 建立Socket.io连接
    const socket = io();
    
    // 自动调整输入框高度
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // 发送消息
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // 检查是否是@电影消息
            if (message.startsWith('@电影')) {
                // 提取URL并发送电影消息
                const url = message.substring(4).trim();
                if (url) {
                    socket.emit('send_message', { 
                        message: message,
                        type: 'movie',
                        movie_url: `https://jx.m3u8.tv/jiexi/?url=${encodeURIComponent(url)}`
                    });
                } else {
                    socket.emit('send_message', { message: message });
                }
            } else if (message.startsWith('@伯小爵')) {
                // 发送AI助手消息
                socket.emit('send_message', { 
                    message: message,
                    type: 'ai',
                    ai_mention: true
                });
            } else {
                socket.emit('send_message', { message: message });
            }
            
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            // 隐藏表情选择器
            emojiPicker.style.display = 'none';
        }
    }
    
    // 点击发送按钮
    sendButton.addEventListener('click', sendMessage);
    
    // 按Enter发送消息（Shift+Enter换行）
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // 表情选择器
    emojiBtn.addEventListener('click', function() {
        emojiPicker.style.display = emojiPicker.style.display === 'block' ? 'none' : 'block';
    });
    
    // 选择表情
    document.querySelectorAll('.emoji-grid span').forEach(emoji => {
        emoji.addEventListener('click', function() {
            messageInput.value += this.textContent;
            messageInput.focus();
        });
    });
    
    // 点击其他地方关闭表情选择器
    document.addEventListener('click', function(event) {
        if (!emojiBtn.contains(event.target) && !emojiPicker.contains(event.target)) {
            emojiPicker.style.display = 'none';
        }
    });
    
    // 电影按钮快捷操作
    movieBtn.addEventListener('click', function() {
        messageInput.value = '@电影 ';
        messageInput.focus();
    });
    
    // 伯小爵AI助手快捷操作
    aiBtn.addEventListener('click', function() {
        messageInput.value = '@伯小爵 ';
        messageInput.focus();
    });
    
    // 退出登录
    logoutButton.addEventListener('click', function() {
        if (confirm('确定要退出聊天室吗？')) {
            window.location.href = '/logout';
        }
    });
    
    // 处理接收到的消息
    socket.on('receive_message', function(data) {
        const messageElement = document.createElement('div');
        messageElement.className = `message-item ${data.username === currentUsername ? 'self' : 'other'}`;
        
        // 消息头部
        const headerElement = document.createElement('div');
        headerElement.className = 'message-header';
        headerElement.innerHTML = `
            <span class="message-user">${data.username}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        `;
        
        // 消息内容
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        
        // 根据消息类型处理内容
        if (data.type === 'movie' && data.movie_url) {
            contentElement.innerHTML = `
                <div>🎬 正在播放电影</div>
                <div class="movie-player">
                    <iframe src="${data.movie_url}" width="400" height="400" allowfullscreen></iframe>
                </div>
            `;
        } else if (data.type === 'ai' || data.ai_response) {
            contentElement.classList.add('ai-response');
            contentElement.textContent = data.message;
        } else if (data.type === 'mention' && data.mentioned_user) {
            // 高亮@提及的用户
            let formattedMessage = data.message.replace(
                `@${data.mentioned_user}`,
                `<span class="message-mention">@${data.mentioned_user}</span>`
            );
            contentElement.innerHTML = formattedMessage;
            
            // 如果提及的是当前用户，添加提醒
            if (data.mentioned_user === currentUsername) {
                contentElement.style.backgroundColor = '#fff3cd';
                // 可以添加声音提醒或其他效果
            }
        } else {
            contentElement.textContent = data.message;
        }
        
        // 组装消息元素
        messageElement.appendChild(headerElement);
        messageElement.appendChild(contentElement);
        messageArea.appendChild(messageElement);
        
        // 滚动到底部
        scrollToBottom();
    });
    
    // 用户加入通知
    socket.on('user_joined', function(data) {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.textContent = `${data.username} 加入了聊天室`;
        messageArea.appendChild(notification);
        scrollToBottom();
        updateOnlineUsers(data.online_users);
    });
    
    // 用户离开通知
    socket.on('user_left', function(data) {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.textContent = `${data.username} 离开了聊天室`;
        messageArea.appendChild(notification);
        scrollToBottom();
        updateOnlineUsers(data.online_users);
    });
    
    // 更新在线用户列表
    socket.on('update_online_users', function(data) {
        updateOnlineUsers(data.online_users);
    });
    
    // 更新在线用户列表UI
    function updateOnlineUsers(users) {
        const usersContainer = document.querySelector('.users');
        usersContainer.innerHTML = '';
        
        users.forEach(user => {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';
            userElement.innerHTML = `
                <span class="user-status online"></span>
                <span class="user-name">${user}</span>
                ${user === currentUsername ? '<span class="self-tag">(我)</span>' : ''}
            `;
            usersContainer.appendChild(userElement);
        });
        
        // 更新用户数量
        document.querySelector('.user-list-header h3').textContent = `在线用户 (${users.length})`;
    }
    
    // 滚动到消息底部
    function scrollToBottom() {
        messageArea.scrollTop = messageArea.scrollHeight;
    }
    
    // 初始化滚动到底部
    scrollToBottom();
    
    // 处理WebSocket连接断开
    socket.on('disconnect', function() {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.style.color = '#dc3545';
        notification.textContent = '与服务器连接已断开，请刷新页面重试';
        messageArea.appendChild(notification);
        scrollToBottom();
    });
    
    // 处理WebSocket连接错误
    socket.on('connect_error', function(error) {
        console.error('连接错误:', error);
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.style.color = '#dc3545';
        notification.textContent = '连接服务器时出错，请稍后重试';
        messageArea.appendChild(notification);
        scrollToBottom();
    });
});