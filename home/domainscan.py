#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : domainscan.py

from flask import Blueprint,request,render_template,g,redirect,url_for,session
from utils.decorators import  login_required
from model.models import Domain_Table
from model.exts import db

domainscan = Blueprint("domainscan", __name__)

from .task import addtask
@domainscan.route("/doaminscan", methods=['POST'])
@login_required
def domain_scan():
    domain = request.form.get('domain')
    max_threads = 2
    addtask(taskname = '域名探测',domain = domain, max_threads=max_threads)
    return redirect(url_for('domainscan.select_domain'))

@domainscan.route("/doaminscan", methods=['GET'])
@login_required
def select_domain():
    """
        展示端口扫描结果
    """
    select = request.args.get('filter')
    q = request.args.get('q')
    session['filter'] = select
    session['q'] = q
    if q and select == "target_domain":
        data = Domain_Table.query.filter(Domain_Table.create_user == g.user.username, Domain_Table.domain == q).all()
    else:
        data = Domain_Table.query.filter(Domain_Table.create_user == g.user.username).all()
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
    return render_template("DomainScanPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           filter = session.get('filter', ''),
                           q = session.get('q', ''))