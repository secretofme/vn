from flask import Flask,session,g,jsonify,redirect,url_for,render_template
import config
from model.exts import db
from model.models import *
from flask_migrate import Migrate
from home.admin import admin
from home.portscan import portscan
from home.domainscan import domainscan
from home.crawler import crawler
from home.task import task
from home.vulnscan import vulnscan
from home.fingerprintscan import fingerprintscan

app = Flask(__name__)
# 加载配置文件
app.config.from_object(config)
# 初始化app
db.init_app(app)

# 注册蓝图
app.register_blueprint(admin)
app.register_blueprint(portscan)
app.register_blueprint(domainscan)
app.register_blueprint(crawler)
app.register_blueprint(vulnscan)
app.register_blueprint(fingerprintscan)
app.register_blueprint(task)

migrate = Migrate(app, db)

# 钩子函数，特殊的装饰器
# 在渲染前执行，拿到session
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

# 上下文处理器
@app.context_processor
def my_context_processor():
    return {"user": g.user}

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'status':'404','error': 'Not found'}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'status':'500','error': 'Internal server error'}), 500

# 自定义过滤器
@app.template_filter('my_eval')
def my_eval(value):
    v = eval(value)
    return v

@app.route("/", methods=['GET'])
def i():
    return redirect(url_for('admin.login'))

@app.route("/test", methods=['GET'])
def test():

    return render_template("ipdw.html")

if __name__ == '__main__':
    app.run(threaded=True)
