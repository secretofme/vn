#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : crawler.py

from flask import Blueprint,request,render_template,flash,g,redirect,url_for,session
from utils.decorators import  login_required
from model.models import Spider_Table,TaskList
from model.exts import db
import requests
import multiprocessing

crawler = Blueprint("crawler", __name__)

from .task import addtask
@crawler.route("/crawler", methods=['POST'])
@login_required
def spiderscan():
    url = request.form.get('url')
    deepth = request.form.get('deepth')
    if deepth == '':
        deepth = '2'
    addtask(taskname = '爬虫', url = url, deepth=deepth)
    return redirect(url_for('crawler.select_spider'))

@crawler.route("/crawler", methods=['GET'])
@login_required
def select_spider():
    select = request.args.get('filter')
    q = request.args.get('q')
    session['filter'] = select
    session['q'] = q
    if q and select == "url":
        data = Spider_Table.query.filter(Spider_Table.create_user == g.user.username, Spider_Table.url.like("%"+ q +"%")).all()
    elif q and select == "key":
        data = Spider_Table.query.filter(Spider_Table.create_user == g.user.username, Spider_Table.urllist.like("%"+ q +"%")).all()
    else:
        data = Spider_Table.query.filter(Spider_Table.create_user == g.user.username).all()
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
    return render_template("SpiderPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           filter = session.get('filter', ''),
                           q = session.get('q', ''))