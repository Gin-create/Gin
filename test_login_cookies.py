import requests

# 创建一个会话对象
session = requests.Session()

# 登录URL
login_url = 'http://localhost:5001/login'

# 登录数据
login_data = {
    'username': 'gin',
    'password': 'gin',
    'server_url': 'http://localhost:5001'
}

# 打印登录前的Cookies
print(f'登录前Cookies: {dict(session.cookies)}')

# 发送登录请求，允许重定向
response = session.post(login_url, data=login_data, allow_redirects=True)

# 打印登录后的状态码
print(f'登录状态码: {response.status_code}')

# 打印登录后的URL
print(f'登录后URL: {response.url}')

# 打印登录后的Cookies
print(f'登录后Cookies: {dict(session.cookies)}')

# 打印响应头
print(f'响应头: {dict(response.headers)}')

# 打印响应内容的前500个字符
print(f'响应内容前500字符: {response.text[:500]}...')
