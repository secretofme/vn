#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : portscan.py

from flask import Blueprint,request,render_template,flash,g,redirect,url_for,session
from utils.decorators import  login_required
from model.models import Port_Table,TaskList
from model.exts import db
import multiprocessing

portscan = Blueprint("portscan", __name__)

from .task import addtask
@portscan.route("/portscan", methods=['POST'])
@login_required
def port_scan():
    """
        端口扫描功能
    :return: 端口扫描结果
    """
    ips = request.form.get('target_ips').split(",")
    port = request.form.get('target_ports').split(",")
    if port[0] == '':
        port = ['21','22','23','25','53','80','111','389','443','465','873','993','995','1000','1433','1521','1723','3306','3389','5000','5001','5432','5900','5989','6379','6666','7001','8000','8001','8009','8010','8080','8081','8088','8443','8888','9900','9999','10621','27017']
    max_threads = 100
    addtask(taskname = '端口扫描',ips = ips, port = port,max_threads=max_threads)
    return redirect(url_for('portscan.select_port'))

@portscan.route("/portscan", methods=['GET'])
@login_required
def select_port():
    """
        展示端口扫描结果
    """
    select = request.args.get('filter')
    q = request.args.get('q')
    session['filter'] = select
    session['q'] = q
    if q and select == "target_port":
        data = Port_Table.query.filter(Port_Table.create_user == g.user.username, Port_Table.target_port == q).all()
    elif q and select == "target_ip":
        data = Port_Table.query.filter(Port_Table.create_user == g.user.username, Port_Table.target_ip == q).all()
    else:
        data = Port_Table.query.filter(Port_Table.create_user == g.user.username).all()
        session.pop('filter', None)
        session.pop('q', None)
    page = int(request.args.get("page", 1))
    # data = Port_Table.query.filter(Port_Table.status == "open").all()
    # 每页显示 10 条记录
    per_page = 10
    # 计算总页数
    total_pages = (len(data) + per_page - 1) // per_page
    # 对数据集进行分页
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    return render_template("PortScanPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           filter = session.get('filter', ''),
                           q = session.get('q', ''))