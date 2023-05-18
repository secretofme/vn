from functools import wraps
from flask import session, redirect, url_for

# 储存所有的装饰器
# 在不改变函数的基础上增加一个功能

# 登录验证
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return wrapper
