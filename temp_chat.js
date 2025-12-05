document.addEventListener('DOMContentLoaded', function() {
    // 鑾峰彇DOM鍏冪礌
    const messageArea = document.getElementById('message-area');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const logoutButton = document.getElementById('logout-button');
    const emojiBtn = document.getElementById('emoji-btn');
    const emojiPicker = document.getElementById('emoji-picker');
    const movieBtn = document.getElementById('movie-btn');
    const bojueBtn = document.getElementById('ai-btn');
    
    // 瀛樺偍AI鍝嶅簲娑堟伅鍏冪礌鐨勬槧灏?    const aiResponseElements = {};
    
    // 鑾峰彇褰撳墠鐢ㄦ埛鍚嶏紙浠嶩TML涓В鏋愶級
    const currentUsername = document.querySelector('.user-info span').textContent.replace('褰撳墠鐢ㄦ埛: ', '');
    
    // 寤虹珛Socket.io杩炴帴
    const socket = io();
    
    // 鑷姩璋冩暣杈撳叆妗嗛珮搴?    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // 鍙戦€佹秷鎭?    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // 妫€鏌ユ槸鍚︽槸@鐢靛奖娑堟伅
            if (message.startsWith('@鐢靛奖')) {
                // 鎻愬彇URL骞跺彂閫佺數褰辨秷鎭?                const url = message.substring(4).trim();
                if (url) {
                    socket.emit('send_message', { 
                        message: message,
                        type: 'movie',
                        movie_url: `https://jx.m3u8.tv/jiexi/?url=${encodeURIComponent(url)}`
                    });
                } else {
                    socket.emit('send_message', { message: message });
                }
            } else if (message.startsWith('@浼皬鐖?)) {
                // 鍙戦€佷集灏忕埖AI鍔╂墜娑堟伅
                socket.emit('send_message', { 
                    message: message,
                    type: 'ai',
                    ai_mention: true
                });
            } else if (message.startsWith('@闊充箰')) {
                // 鍙戦€侀煶涔愬懡浠?                socket.emit('send_message', { 
                    message: message,
                    type: 'music'
                });
            } else if (message.startsWith('@澶╂皵')) {
                // 鍙戦€佸ぉ姘旀煡璇㈠懡浠?                const city = message.substring(4).trim();
                if (city) {
                    socket.emit('send_message', { 
                        message: message,
                        type: 'weather',
                        city: city
                    });
                } else {
                    socket.emit('send_message', { message: message });
                }
            } else {
                socket.emit('send_message', { message: message });
            }
            
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            // 闅愯棌琛ㄦ儏閫夋嫨鍣?            emojiPicker.style.display = 'none';
        }
    }
    
    // 鐐瑰嚮鍙戦€佹寜閽?    sendButton.addEventListener('click', sendMessage);
    
    // 鎸塃nter鍙戦€佹秷鎭紙Shift+Enter鎹㈣锛?    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // 琛ㄦ儏閫夋嫨鍣?    emojiBtn.addEventListener('click', function() {
        emojiPicker.style.display = emojiPicker.style.display === 'block' ? 'none' : 'block';
    });
    
    // 閫夋嫨琛ㄦ儏
    document.querySelectorAll('.emoji-grid span').forEach(emoji => {
        emoji.addEventListener('click', function() {
            messageInput.value += this.textContent;
            messageInput.focus();
        });
    });
    
    // 鐐瑰嚮鍏朵粬鍦版柟鍏抽棴琛ㄦ儏閫夋嫨鍣?    document.addEventListener('click', function(event) {
        if (!emojiBtn.contains(event.target) && !emojiPicker.contains(event.target)) {
            emojiPicker.style.display = 'none';
        }
    });
    
    // 鐢靛奖鎸夐挳蹇嵎鎿嶄綔
    movieBtn.addEventListener('click', function() {
        messageInput.value = '@鐢靛奖 ';
        messageInput.focus();
    });
    
    // 浼皬鐖礎I鍔╂墜蹇嵎鎿嶄綔
    bojueBtn.addEventListener('click', function() {
        messageInput.value = '@浼皬鐖?';
        messageInput.focus();
    });
    
    // 閫€鍑虹櫥褰?    logoutButton.addEventListener('click', function() {
        if (confirm('纭畾瑕侀€€鍑鸿亰澶╁鍚楋紵')) {
            window.location.href = '/logout';
        }
    });
    
    // 澶勭悊鎺ユ敹鍒扮殑娑堟伅
    socket.on('receive_message', function(data) {
        // 澶勭悊娴佸紡AI鍝嶅簲鐨勪笉鍚岄樁娈?        if (data.type === 'ai_start') {
            // AI寮€濮嬪搷搴旓紝鍒涘缓娑堟伅瀹瑰櫒
            const messageElement = document.createElement('div');
            messageElement.className = 'message-item other ai-message';
            messageElement.setAttribute('data-message-id', data.message_id);
            
            // 娑堟伅澶撮儴
            const headerElement = document.createElement('div');
            headerElement.className = 'message-header';
            headerElement.innerHTML = `
                <span class="message-user">${data.username}</span>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
                <span class="typing-indicator">杈撳叆涓?..</span>
            `;
            
            // 娑堟伅鍐呭瀹瑰櫒
            const contentElement = document.createElement('div');
            contentElement.className = 'message-content ai-response';
            contentElement.textContent = '';
            
            // 缁勮娑堟伅鍏冪礌
            messageElement.appendChild(headerElement);
            messageElement.appendChild(contentElement);
            messageArea.appendChild(messageElement);
            
            // 瀛樺偍娑堟伅鍏冪礌寮曠敤
            aiResponseElements[data.message_id] = {
                element: messageElement,
                content: contentElement,
                header: headerElement
            };
            
            // 婊氬姩鍒板簳閮?            scrollToBottom();
            return;
        } 
        else if (data.type === 'ai_stream') {
            // AI娴佸紡鍝嶅簲鍐呭鏇存柊
            if (aiResponseElements[data.message_id]) {
                const { content } = aiResponseElements[data.message_id];
                // 杩藉姞鏂板唴瀹癸紝鏀寔鍩烘湰鐨凪arkdown鏍煎紡
                let formattedContent = escapeHtml(data.content);
                // 绠€鍗曠殑鎹㈣鏀寔
                formattedContent = formattedContent.replace(/\n/g, '<br>');
                // 绠€鍗曠殑鍔犵矖鏀寔
                formattedContent = formattedContent.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
                // 绠€鍗曠殑鏂滀綋鏀寔
                formattedContent = formattedContent.replace(/\*(.+?)\*/g, '<em>$1</em>');
                
                // 濡傛灉鍐呭涓嶄负绌猴紝娣诲姞鍒版秷鎭腑
                if (content.innerHTML === '') {
                    content.innerHTML = formattedContent;
                } else {
                    content.innerHTML += formattedContent;
                }
                
                // 婊氬姩鍒板簳閮?                scrollToBottom();
            }
            return;
        }
        else if (data.type === 'ai_end') {
            // AI鍝嶅簲瀹屾垚
            if (aiResponseElements[data.message_id]) {
                const { element, header } = aiResponseElements[data.message_id];
                // 绉婚櫎杈撳叆涓寚绀哄櫒
                const typingIndicator = header.querySelector('.typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                // 鏍囪涓哄凡瀹屾垚
                element.classList.add('ai-complete');
                // 娓呯悊寮曠敤锛堝彲閫夛級
                // delete aiResponseElements[data.message_id];
            }
            return;
        }
        else if (data.type === 'ai_error') {
            // AI鍝嶅簲閿欒
            if (aiResponseElements[data.message_id]) {
                const { element, content, header } = aiResponseElements[data.message_id];
                // 绉婚櫎杈撳叆涓寚绀哄櫒
                const typingIndicator = header.querySelector('.typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                // 鏄剧ず閿欒娑堟伅
                content.textContent = data.error;
                content.style.color = '#dc3545';
                // 鏍囪涓洪敊璇?                element.classList.add('ai-error');
            }
            return;
        }
        
        // 澶勭悊甯歌娑堟伅
        const messageElement = document.createElement('div');
        messageElement.className = `message-item ${data.username === currentUsername ? 'self' : 'other'}`;
        
        // 娑堟伅澶撮儴
        const headerElement = document.createElement('div');
        headerElement.className = 'message-header';
        headerElement.innerHTML = `
            <span class="message-user">${data.username}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        `;
        
        // 娑堟伅鍐呭
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        
        // 鏍规嵁娑堟伅绫诲瀷澶勭悊鍐呭
        if (data.type === 'movie' && data.movie_url) {
            contentElement.innerHTML = `
                <div>馃幀 姝ｅ湪鎾斁鐢靛奖</div>
                <div class="movie-player">
                    <iframe src="${data.movie_url}" width="400" height="400" allowfullscreen></iframe>
                </div>
            `;
        } else if (data.type === 'music' && data.music_info) {
            const music = data.music_info;
            contentElement.innerHTML = `
                <div>馃幍 姝ｅ湪鎾斁闊充箰</div>
                <div class="music-player">
                    <div class="music-info">
                        <div class="music-pic">
                            <img src="${music.cover_url}" alt="${music.song_name}" width="300" height="300">
                        </div>
                        <div class="music-details">
                            <h3 class="music-name">${music.song_name}</h3>
                            <h4 class="music-singer">${music.singer}</h4>
                            <audio controls width="300" referrerpolicy="no-referrer">
                        <source src="/proxy-music?url=${encodeURIComponent(music.song_url || '')}" type="audio/mpeg">
                        鎮ㄧ殑娴忚鍣ㄤ笉鏀寔闊抽鎾斁銆?                      </audio>
                        </div>
                    </div>
                </div>
            `;
        } else if (data.type === 'ai' || data.ai_response) {
            contentElement.classList.add('ai-response');
            contentElement.textContent = data.message;
        } else if (data.type === 'weather' && data.city) {
            // 鍒涘缓澶╂皵iframe
            const weatherIframeUrl = `/weather.html?city=${encodeURIComponent(data.city)}`;
            contentElement.innerHTML = `
                <div>馃尋锔?${data.city} 澶╂皵淇℃伅</div>
                <div class="weather-card">
                    <iframe src="${weatherIframeUrl}" width="400" height="400" frameborder="0" scrolling="auto"></iframe>
                </div>
            `;
        } else if (data.type === 'news' && data.news_list) {
            // 鍒涘缓鏂伴椈鍖哄煙
            contentElement.innerHTML = createNewsHTML(data.news_list);
        } else if (data.type === 'mention' && data.mentioned_user) {
            // 楂樹寒@鎻愬強鐨勭敤鎴?            let formattedMessage = escapeHtml(data.message).replace(
                new RegExp(`@${escapeRegex(data.mentioned_user)}`),
                `<span class="message-mention">@${data.mentioned_user}</span>`
            );
            contentElement.innerHTML = formattedMessage;
            
            // 濡傛灉鎻愬強鐨勬槸褰撳墠鐢ㄦ埛锛屾坊鍔犳彁閱?            if (data.mentioned_user === currentUsername) {
                contentElement.style.backgroundColor = '#fff3cd';
                // 鍙互娣诲姞澹伴煶鎻愰啋鎴栧叾浠栨晥鏋?            }
        } else {
            contentElement.textContent = data.message;
        }
        
        // 缁勮娑堟伅鍏冪礌
        messageElement.appendChild(headerElement);
        messageElement.appendChild(contentElement);
        messageArea.appendChild(messageElement);
        
        // 婊氬姩鍒板簳閮?        scrollToBottom();
        
        // 澶勭悊鍙充晶杈规爮闊充箰鎾斁鍣?        if (data.type === 'music' && data.music_info) {
            updateMusicPlayer(data.music_info);
        }
    });
    
    // HTML杞箟鍑芥暟
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // 姝ｅ垯琛ㄨ揪寮忚浆涔夊嚱鏁?    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // 鍒涘缓鏂伴椈淇℃伅鐨凥TML缁撴瀯
function createNewsHTML(newsList) {
    // 鍙樉绀哄墠10鏉℃柊闂?    const topNews = newsList.slice(0, 10);
    
    return `
        <div class="news-container">
            <h3>馃摪 寰崥鐑悳</h3>
            <div class="news-list" style="width: 400px; height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
                <ol style="list-style-type: decimal; padding-left: 20px; margin: 0;">
                    ${topNews.map(news => `
                        <li style="margin-bottom: 10px; padding: 5px; border-bottom: 1px dotted #eee;">
                            <a href="${news.url}" target="_blank" style="text-decoration: none; color: #333; font-weight: 500;">
                                ${news.title}
                            </a>
                            <span style="display: block; font-size: 12px; color: #999; margin-top: 2px;">
                                鐑害: ${news.hot}
                            </span>
                        </li>
                    `).join('')}
                </ol>
            </div>
        </div>
    `;
}
    
    // 鐢ㄦ埛鍔犲叆閫氱煡
    socket.on('user_joined', function(data) {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.textContent = `${data.username} 鍔犲叆浜嗚亰澶╁`;
        messageArea.appendChild(notification);
        scrollToBottom();
        updateOnlineUsers(data.online_users);
    });
    
    // 鐢ㄦ埛绂诲紑閫氱煡
    socket.on('user_left', function(data) {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.textContent = `${data.username} 绂诲紑浜嗚亰澶╁`;
        messageArea.appendChild(notification);
        scrollToBottom();
        updateOnlineUsers(data.online_users);
    });
    
    // 鏇存柊鍦ㄧ嚎鐢ㄦ埛鍒楄〃
    socket.on('update_online_users', function(data) {
        updateOnlineUsers(data.online_users);
    });
    
    // 鏇存柊鍦ㄧ嚎鐢ㄦ埛鍒楄〃UI
    function updateOnlineUsers(users) {
        const usersContainer = document.querySelector('.users');
        usersContainer.innerHTML = '';
        
        users.forEach(user => {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';
            userElement.innerHTML = `
                <span class="user-status online"></span>
                <span class="user-name">${user}</span>
                ${user === currentUsername ? '<span class="self-tag">(鎴?</span>' : ''}
            `;
            usersContainer.appendChild(userElement);
        });
        
        // 鏇存柊鐢ㄦ埛鏁伴噺
        document.querySelector('.user-list-header h3').textContent = `鍦ㄧ嚎鐢ㄦ埛 (${users.length})`;
    }
    
    // 婊氬姩鍒版秷鎭簳閮?    function scrollToBottom() {
        messageArea.scrollTop = messageArea.scrollHeight;
    }
    
    // 鏇存柊鍙充晶杈规爮闊充箰鎾斁鍣?    function updateMusicPlayer(music) {
        // 灏濊瘯鏌ユ壘鐜版湁鐨勯煶涔愭挱鏀惧櫒
        let musicPlayer = document.querySelector('.music-player-sidebar');
        
        if (!musicPlayer) {
            // 濡傛灉涓嶅瓨鍦紝鍒涘缓鏂扮殑鎾斁鍣?            musicPlayer = document.createElement('div');
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
            document.body.appendChild(musicPlayer);
        }
        
        // 鏇存柊鎾斁鍣ㄥ唴瀹?        musicPlayer.innerHTML = `
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="font-weight: bold; color: #667eea;">馃幍 姝ｅ湪鎾斁闊充箰</div>
            </div>
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="${music.cover_url || 'https://via.placeholder.com/120'}" 
                     alt="${music.song_name}" 
                     width="120" 
                     height="120" 
                     style="border-radius: 8px;">
            </div>
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="font-weight: bold;">${music.song_name || '鏈煡姝屾洸'}</div>
                <div style="color: #666; font-size: 14px;">${music.singer || '鏈煡姝屾墜'}</div>
            </div>
            <div style="text-align: center;">
                <audio controls style="width: 100%;" referrerpolicy="no-referrer">
                    <source src="/proxy-music?url=${encodeURIComponent(music.song_url || '')}" type="audio/mpeg">
                    鎮ㄧ殑娴忚鍣ㄤ笉鏀寔闊抽鎾斁銆?                </audio>
            </div>
        `;
    }
    
    // 鍒濆鍖栨粴鍔ㄥ埌搴曢儴
    scrollToBottom();
    
    // 澶勭悊WebSocket杩炴帴鏂紑
    socket.on('disconnect', function() {
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.style.color = '#dc3545';
        notification.textContent = '涓庢湇鍔″櫒杩炴帴宸叉柇寮€锛岃鍒锋柊椤甸潰閲嶈瘯';
        messageArea.appendChild(notification);
        scrollToBottom();
    });
    
    // 澶勭悊WebSocket杩炴帴閿欒
    socket.on('connect_error', function(error) {
        console.error('杩炴帴閿欒:', error);
        const notification = document.createElement('div');
        notification.className = 'welcome-message';
        notification.style.color = '#dc3545';
        notification.textContent = '杩炴帴鏈嶅姟鍣ㄦ椂鍑洪敊锛岃绋嶅悗閲嶈瘯';
        messageArea.appendChild(notification);
        scrollToBottom();
    });
});
