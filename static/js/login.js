document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById('username');
    const usernameValidation = document.getElementById('username-validation');
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    
    // 昵称验证
    usernameInput.addEventListener('input', debounce(function() {
        const username = usernameInput.value.trim();
        if (username.length < 1) {
            usernameValidation.textContent = '';
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
            usernameValidation.textContent = data.message;
            usernameValidation.style.color = data.valid ? '#28a745' : '#dc3545';
        })
        .catch(error => {
            console.error('验证昵称时出错:', error);
        });
    }, 300));
    
    // 表单提交
    loginForm.addEventListener('submit', function(event) {
        const username = usernameInput.value.trim();
        
        // 基本验证
        if (!username) {
            usernameValidation.textContent = '请输入昵称';
            usernameValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        // 检查昵称长度
        if (username.length > 20) {
            usernameValidation.textContent = '昵称长度不能超过20个字符';
            usernameValidation.style.color = '#dc3545';
            event.preventDefault();
            return;
        }
        
        // 禁用按钮防止重复提交
        loginButton.disabled = true;
        loginButton.textContent = '登录中...';
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