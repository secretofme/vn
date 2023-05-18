from flask import session,redirect,render_template,request,url_for,flash,Blueprint,g
from model.models import User
from utils.forms import RegisterForm
from model.exts import db
from utils.decorators import  login_required

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route('/login', methods=['GET', 'POST'])
@admin.route('/', methods=['GET', 'POST'])
def login():
    """
        登录功能
    :return: 登录页面
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('admin.index'))
        else:
            flash("用户名或密码输入错误")
            return render_template('login.html')

@admin.route("/logout")
@login_required
def logout():
    """
        清空session，用户退出
    """
    session.clear()
    return redirect(url_for('admin.login'))

@admin.route("/register", methods=['POST'])
def register():
    """
        注册功能
    """
    # 表单验证：flask-wtf: wtforms
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username).first()
        if user:
            flash("注册的用户已存在")
            return render_template("login.html")
        else:
            user = User(username=username, password=password,email=None,phone=None,description=None)
            db.session.add(user)
            db.session.commit()
            flash("注册成功")
            return redirect(url_for("admin.login"))
    else:
        print(form.errors)
        flash("两次输入的密码不一致！")
        return redirect(url_for("admin.login"))

@admin.route("/changePasswd", methods=['GET' , 'POST'])
@login_required
def changePasswd():
    """
        修改密码

    """
    if request.method == 'GET':
        return render_template("changepwd.html")
    else:
        oldpasswd = request.form.get('oldpassword')
        newpasswd = request.form.get('newpassword')
        password_confirm = request.form.get('password_confirm')
        if g.user.check_password(oldpasswd) and newpasswd == password_confirm:
            g.user.set_password(newpasswd)
            db.session.commit()
            return redirect(url_for('admin.login'))
        else:
            flash("旧密码输入错误！")
            return redirect(url_for('admin.changePasswd'))

@admin.route("/edit", methods=[ 'GET','POST'])
@login_required
def edit():
    """
        编辑个人信息
    """
    print(g.user.username)
    if request.method == 'GET':
        return render_template("edit.html")
    else:
        email = request.form.get('email')
        phone = request.form.get('phone')
        description = request.form.get('description')
        if email is not None:
            g.user.email = email
        if phone is not None:
            g.user.phone = phone
        if description is not None:
            g.user.description = description
        db.session.commit()
        return redirect(url_for('admin.edit'))

from .vulnscan import get_vuln_amount
from .vulnscan import get_vuln_rank
@admin.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    amount = get_vuln_amount()
    rank = get_vuln_rank()
    return render_template("index.html",amount=amount,rank=rank)