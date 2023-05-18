#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : fingerprintscan.py

from flask import Blueprint,request,render_template,flash,g,redirect,url_for,session
from utils.decorators import  login_required
from model.models import Spider_Table,TaskList,Fingerprint_Table
from model.exts import db
import requests
import multiprocessing

fingerprintscan = Blueprint("fingerprintscan", __name__)

from .task import addtask
@fingerprintscan.route("/fingerprint", methods=['POST'])
@login_required
def fingerprint_scan():
    url = request.form.get('url')
    # 获取另一个蓝图中定义的函数
    addtask(taskname = '指纹识别',url = url)
    return redirect(url_for('fingerprintscan.select_fingerprint'))

@fingerprintscan.route("/fingerprint", methods=['GET'])
@login_required
def select_fingerprint():
    """
    """
    select = request.args.get('filter')
    q = request.args.get('q')
    session['filter'] = select
    session['q'] = q
    if q and select == "url":
        data = Fingerprint_Table.query.filter(Fingerprint_Table.create_user == g.user.username, Fingerprint_Table.url.like ("%"+q+"%")).all()
    else:
        data = Fingerprint_Table.query.filter(Fingerprint_Table.create_user == g.user.username).all()
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
    return render_template("FingerprintPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           filter = session.get('filter', ''),
                           q = session.get('q', ''))