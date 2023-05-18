from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from model.exts import db


# ORM模型映射成表的三步
# 1. flask db init：这步只需要执行一次
# 2. flask db migrate：识别ORM模型的改变，生成迁移脚本
# 3. flask db upgrade：运行迁移脚本，同步到数据库中

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, username, email ,phone, password , description):
        self.username = username
        self.email = email
        self.phone = phone
        self.description = description
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Port_Table(db.Model):
    __tablename__ = 'Port_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_user = db.Column(db.String(50), db.ForeignKey('user.username') ,nullable=False)
    target_ip = db.Column(db.String(15), nullable=False)
    target_port = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50), nullable=True)
    version = db.Column(db.String(50), nullable=True)

    def __init__(self, create_user, target_ip ,target_port, status , service , version):
        self.create_user = create_user
        self.target_ip = target_ip
        self.target_port = target_port
        self.status = status
        self.service = service
        self.version = version

    user = db.relationship('User', backref=db.backref('Port_Tables', lazy=True))

class Domain_Table(db.Model):
    __tablename__ = 'Domain_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_user = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    domain = db.Column(db.String(30), nullable=False)
    subdomain = db.Column(db.String(30), nullable=False)

    def __init__(self,create_user,domain,subdomain):
        self.create_user = create_user
        self.domain = domain
        self.subdomain = subdomain

    user = db.relationship('User', backref=db.backref('Domain_Tables', lazy=True))

class Spider_Table(db.Model):
    __tablename__ = 'Spider_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_user = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    urllist = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,create_user,url,urllist,code):
        self.create_user = create_user
        self.url = url
        self.urllist = urllist
        self.code = code

    user = db.relationship('User', backref=db.backref('Spider_Tables', lazy=True))

class Fingerprint_Table(db.Model):
    __tablename__ = 'Fingerprint_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=False)
    fingerprint = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    create_user = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)

    user = db.relationship('User', backref=db.backref('Fingerprint_Tables', lazy=True))

    def __init__(self,url,fingerprint,title,create_user):
        self.create_user = create_user
        self.url = url
        self.fingerprint = fingerprint
        self.title = title

class Vuln_Table(db.Model):
    __tablename__ = 'Vuln_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=True)
    vulntype = db.Column(db.String(100), nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)
    param = db.Column(db.Text, nullable=True)
    payload = db.Column(db.Text, nullable=True)
    snapshot = db.Column(db.Text, nullable=True)
    create_user = db.Column(db.String(50), nullable=False)

    def __init__(self,url,vulntype,param,payload,snapshot,create_user):
        self.url = url
        self.vulntype = vulntype
        self.param = param
        self.payload = payload
        self.snapshot = snapshot
        self.create_user = create_user

class Property_Table(db.Model):
    __tablename__ = 'Property_Tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=True)
    Number_of_vulnerabilities = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(30), default='进行中')
    create_user = db.Column(db.String(50), nullable=False)

    def __init__(self,url,Number_of_vulnerabilities,create_user):
        self.url = url
        self.Number_of_vulnerabilities = Number_of_vulnerabilities
        self.create_user = create_user

class TaskList(db.Model):
    __tablename__ = 'tasklist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.String(128), nullable=False)
    create_user = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    taskname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), default='进行中')
    create_time = db.Column(db.DateTime, default=datetime.now)

    def create_task(self, create_user, taskname, pid):
        new_task = TaskList(create_user=create_user, taskname=taskname, pid=pid)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def completed(self):
        self.status = '已完成'
        db.session.commit()
    def failed(self):
        self.status = '失败'
        db.session.commit()
