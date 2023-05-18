import wtforms
from wtforms.validators import  Length, EqualTo, email


# 表单验证

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

class EditForm(wtforms.Form):
    email = wtforms.StringField(validators=[Length(min=5, max=20, message="邮箱格式错误！"),email()])
    phone = wtforms.StringField(validators=[Length(min=11, max=11, message="电话号码格式错误")])