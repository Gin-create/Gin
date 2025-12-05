// 用户名历史记录管理模块
const UsernameHistoryManager = {
    /**
     * 存储键名
     * @type {string}
     */
    STORAGE_KEY: 'usernameHistory',
    
    /**
     * 默认最大历史记录数量
     * @type {number}
     */
    DEFAULT_MAX_ITEMS: 10,
    
    /**
     * 检查存储是否可用
     * @returns {boolean} 存储是否可用
     */
    isStorageAvailable() {
        try {
            const storage = window.localStorage;
            if (!storage) return false;
            
            // 测试存储是否真正可用
            const testKey = 'test_' + Date.now();
            storage.setItem(testKey, testKey);
            storage.removeItem(testKey);
            return true;
        } catch (e) {
            return false;
        }
    },
    
    /**
     * 获取存储的历史记录
     * @param {number} [maxItems] - 最大返回数量，默认使用DEFAULT_MAX_ITEMS
     * @returns {Array<{username: string, timestamp: number}>} 历史记录数组
     */
    getHistory(maxItems = this.DEFAULT_MAX_ITEMS) {
        if (!this.isStorageAvailable()) return [];
        
        try {
            const history = localStorage.getItem(this.STORAGE_KEY);
            if (!history) return [];
            
            const parsed = JSON.parse(history);
            return Array.isArray(parsed) ? parsed.slice(0, maxItems) : [];
        } catch (error) {
            console.error('获取用户名历史记录失败:', error);
            return [];
        }
    },
    
    /**
     * 添加用户名到历史记录
     * @param {string} username - 用户名
     * @param {number} [maxItems] - 最大历史记录数量，默认使用DEFAULT_MAX_ITEMS
     * @returns {boolean} 是否添加成功
     */
    add(username, maxItems = this.DEFAULT_MAX_ITEMS) {
        if (!username || typeof username !== 'string' || username.trim() === '') {
            return false;
        }
        
        if (!this.isStorageAvailable()) return false;
        
        try {
            const trimmedUsername = username.trim();
            const history = this.getHistory();
            
            // 移除已存在的相同用户名
            const filteredHistory = history.filter(item => item.username !== trimmedUsername);
            
            // 创建新记录
            const newRecord = {
                username: trimmedUsername,
                timestamp: Date.now()
            };
            
            // 将新记录添加到开头
            const updatedHistory = [newRecord, ...filteredHistory];
            
            // 限制数量
            const limitedHistory = updatedHistory.slice(0, maxItems);
            
            // 保存到localStorage
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(limitedHistory));
            
            return true;
        } catch (error) {
            if (error.name === 'QuotaExceededError' || error.code === 22) {
                // 超出存储容量，尝试清理最早的记录
                console.warn('localStorage容量不足，自动清理最早的历史记录');
                const history = this.getHistory();
                if (history.length > 0) {
                    // 删除一半最旧的记录
                    const removeCount = Math.ceil(history.length / 2);
                    history.splice(-removeCount);
                    try {
                        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
                        // 再次尝试添加
                        return this.add(username, maxItems);
                    } catch (retryError) {
                        console.warn('清理后仍无法保存:', retryError);
                    }
                }
            }
            console.error('添加用户名历史记录失败:', error);
            return false;
        }
    },
    
    /**
     * 删除指定的历史记录
     * @param {string} username - 要删除的用户名
     * @returns {boolean} 是否删除成功
     */
    remove(username) {
        if (!this.isStorageAvailable()) return false;
        
        try {
            const history = this.getHistory();
            const filteredHistory = history.filter(item => item.username !== username);
            
            if (filteredHistory.length !== history.length) {
                localStorage.setItem(this.STORAGE_KEY, JSON.stringify(filteredHistory));
                return true;
            }
            return false;
        } catch (error) {
            console.error('删除用户名历史记录失败:', error);
            return false;
        }
    },
    
    /**
     * 清空所有历史记录
     * @returns {boolean} 是否清空成功
     */
    clear() {
        if (!this.isStorageAvailable()) return false;
        
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            return true;
        } catch (error) {
            console.error('清空用户名历史记录失败:', error);
            return false;
        }
    },
    
    /**
     * 检查用户名是否在历史记录中
     * @param {string} username - 要检查的用户名
     * @returns {boolean} 是否存在
     */
    has(username) {
        if (!username) return false;
        
        const history = this.getHistory();
        return history.some(item => item.username === username.trim());
    },
    
    /**
     * 将指定用户名置顶
     * @param {string} username - 要置顶的用户名
     * @returns {boolean} 是否置顶成功
     */
    bringToTop(username) {
        if (!username || !this.has(username)) return false;
        
        if (!this.isStorageAvailable()) return false;
        
        try {
            const history = this.getHistory();
            const filteredHistory = history.filter(item => item.username !== username.trim());
            const targetItem = history.find(item => item.username === username.trim());
            
            // 更新时间戳并添加到开头
            const updatedItem = {
                ...targetItem,
                timestamp: Date.now()
            };
            
            const updatedHistory = [updatedItem, ...filteredHistory];
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedHistory));
            
            return true;
        } catch (error) {
            console.error('置顶用户名历史记录失败:', error);
            return false;
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    const loginUsernameInput = document.getElementById('login-username');
    
    const registerForm = document.getElementById('register-form');
    const registerButton = document.getElementById('register-button');
    const registerUsernameInput = document.getElementById('register-username');
    const registerPasswordInput = document.getElementById('register-password');
    const registerConfirmPasswordInput = document.getElementById('register-confirm-password');
    const registerUsernameValidation = document.getElementById('register-username-validation');
    const registerPasswordValidation = document.getElementById('register-password-validation');
    const historyList = document.getElementById('username-history-list');

    // 清除所有错误信息
    function clearErrors() {
        const errorElements = document.querySelectorAll('.error');
        errorElements.forEach(element => {
            element.textContent = '';
        });
    }

    // 渲染用户名历史记录列表
    function renderHistoryList() {
        const history = UsernameHistoryManager.getHistory();
        historyList.innerHTML = '';

        if (history.length === 0) {
            historyList.classList.remove('show');
            return;
        }

        history.forEach((item, index) => {
            const listItem = document.createElement('div');
            listItem.className = 'username-history-item';
            listItem.dataset.username = item.username;

            const usernameSpan = document.createElement('span');
            usernameSpan.textContent = item.username;

            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.textContent = '×';
            removeBtn.title = '删除此记录';
            removeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                UsernameHistoryManager.remove(item.username);
                renderHistoryList();
            });

            listItem.appendChild(usernameSpan);
            listItem.appendChild(removeBtn);
            historyList.appendChild(listItem);
        });

        historyList.classList.add('show');
    }

    // 显示下拉列表
    function showHistoryList() {
        renderHistoryList();
    }

    // 隐藏下拉列表
    function hideHistoryList() {
        historyList.classList.remove('show');
        clearActiveItem();
    }

    // 清除活跃项
    function clearActiveItem() {
        const activeItem = document.querySelector('.username-history-item.active');
        if (activeItem) {
            activeItem.classList.remove('active');
        }
    }

    // 选择用户名
    function selectUsername(username) {
        loginUsernameInput.value = username;
        hideHistoryList();
        // 触发change事件
        loginUsernameInput.dispatchEvent(new Event('change'));
        // 聚焦到密码框
        document.getElementById('login-password').focus();
    }

    // 点击列表项选择用户名
    historyList.addEventListener('click', (e) => {
        const listItem = e.target.closest('.username-history-item');
        if (listItem) {
            const username = listItem.dataset.username;
            selectUsername(username);
        }
    });

    // 输入框聚焦/点击时显示下拉列表
    loginUsernameInput.addEventListener('focus', showHistoryList);
    loginUsernameInput.addEventListener('click', showHistoryList);

    // 点击外部区域隐藏下拉列表
    document.addEventListener('click', (e) => {
        if (!loginUsernameInput.contains(e.target) && !historyList.contains(e.target)) {
            hideHistoryList();
        }
    });

    // 键盘导航
    let activeIndex = -1;
    loginUsernameInput.addEventListener('keydown', (e) => {
        const history = UsernameHistoryManager.getHistory();
        const items = document.querySelectorAll('.username-history-item');
        
        if (items.length === 0) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                clearActiveItem();
                activeIndex = (activeIndex + 1) % items.length;
                items[activeIndex].classList.add('active');
                // 滚动到可见区域
                items[activeIndex].scrollIntoView({ block: 'nearest' });
                break;
            case 'ArrowUp':
                e.preventDefault();
                clearActiveItem();
                activeIndex = (activeIndex - 1 + items.length) % items.length;
                items[activeIndex].classList.add('active');
                // 滚动到可见区域
                items[activeIndex].scrollIntoView({ block: 'nearest' });
                break;
            case 'Enter':
                if (activeIndex >= 0 && activeIndex < items.length) {
                    e.preventDefault();
                    selectUsername(items[activeIndex].dataset.username);
                }
                break;
            case 'Escape':
                hideHistoryList();
                break;
        }
    });

    // 实现输入框与历史列表的状态同步
    loginUsernameInput.addEventListener('input', function() {
        const inputValue = this.value.trim();
        
        if (inputValue === '') {
            // 输入框清空时，重置下拉列表
            renderHistoryList();
            return;
        }
        
        // 如果输入的用户名已存在于历史列表中，自动将其置顶
        if (UsernameHistoryManager.has(inputValue)) {
            UsernameHistoryManager.bringToTop(inputValue);
            renderHistoryList();
        }
    });

    // 输入框change事件处理
    loginUsernameInput.addEventListener('change', function() {
        const inputValue = this.value.trim();
        // 如果输入的用户名已存在于历史列表中，确保其在顶部
        if (inputValue !== '' && UsernameHistoryManager.has(inputValue)) {
            UsernameHistoryManager.bringToTop(inputValue);
        }
    });
    
    // 登录/注册切换功能
    window.switchTab = function(tabName) {
        // 切换标签
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
        
        // 切换表单
        document.querySelectorAll('.auth-form').forEach(form => form.classList.remove('active'));
        document.getElementById(`${tabName}-form`).classList.add('active');
    };
    
    // 注册用户名验证
    registerUsernameInput.addEventListener('input', debounce(function() {
        const username = registerUsernameInput.value.trim();
        if (username.length < 1) {
            registerUsernameValidation.textContent = '';
            return;
        }
        
        // 检查用户名长度
        if (username.length < 3) {
            registerUsernameValidation.textContent = '用户名长度不能少于3个字符';
            registerUsernameValidation.style.color = '#dc3545';
            return;
        }
        
        if (username.length > 20) {
            registerUsernameValidation.textContent = '用户名长度不能超过20个字符';
            registerUsernameValidation.style.color = '#dc3545';
            return;
        }
        
        // 发送验证请求
        fetch('/validate_username', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => response.json())
        .then(data => {
            registerUsernameValidation.textContent = data.message;
            registerUsernameValidation.style.color = data.valid ? '#28a745' : '#dc3545';
        })
        .catch(error => {
            console.error('验证用户名时出错:', error);
        });
    }, 300));
    
    // 密码匹配验证
    registerConfirmPasswordInput.addEventListener('input', function() {
        const password = registerPasswordInput.value;
        const confirmPassword = registerConfirmPasswordInput.value;
        
        if (password && confirmPassword) {
            if (password === confirmPassword) {
                registerPasswordValidation.textContent = '密码匹配';
                registerPasswordValidation.style.color = '#28a745';
            } else {
                registerPasswordValidation.textContent = '密码不匹配';
                registerPasswordValidation.style.color = '#dc3545';
            }
        } else {
            registerPasswordValidation.textContent = '';
        }
    });
    
    // 登录表单提交
    loginForm.addEventListener('submit', function(event) {
        const username = loginUsernameInput.value.trim();
        const password = document.getElementById('login-password').value;
        
        // 基本验证
        if (!username) {
            alert('请输入用户名');
            event.preventDefault();
            return;
        }
        
        if (!password) {
            alert('请输入密码');
            event.preventDefault();
            return;
        }
        
        // 保存用户名到历史记录
        UsernameHistoryManager.add(username);
        
        // 禁用按钮防止重复提交
        loginButton.disabled = true;
        loginButton.textContent = '登录中...';
    });
    
    // 注册表单提交
    registerForm.addEventListener('submit', function(event) {
        const username = registerUsernameInput.value.trim();
        const password = registerPasswordInput.value;
        const confirmPassword = registerConfirmPasswordInput.value;
        
        // 基本验证
        if (!username) {
            registerUsernameValidation.textContent = '请输入用户名';
            registerUsernameValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        if (username.length < 3) {
            registerUsernameValidation.textContent = '用户名长度不能少于3个字符';
            registerUsernameValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        if (username.length > 20) {
            registerUsernameValidation.textContent = '用户名长度不能超过20个字符';
            registerUsernameValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        if (!password) {
            registerPasswordValidation.textContent = '请输入密码';
            registerPasswordValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        if (password.length < 6) {
            registerPasswordValidation.textContent = '密码长度不能少于6个字符';
            registerPasswordValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        if (password !== confirmPassword) {
            registerPasswordValidation.textContent = '密码不匹配';
            registerPasswordValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        // 禁用按钮防止重复提交
        registerButton.disabled = true;
        registerButton.textContent = '注册中...';
    });
    
    // 防抖函数
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
});