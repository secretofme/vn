#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : wappalyzer.py

from flask import Blueprint, request, jsonify, render_template, g, session, redirect, url_for, logging
from utils.decorators import  login_required
from model.models import Vuln_Table,Property_Table
import requests
from model.exts import db
from sqlalchemy import or_, not_

vulnscan = Blueprint("vulnscan", __name__)

def get_http_status_code(url):
    '''
    判断url是否存活
    :return: 存活状态
    '''
    try:
        res = requests.get(url)
        code = res.status_code
        data = {
            'http_code': code,
            'status': "success"
        }
        if code == 200 or code == 403:
            return jsonify(data)
    except Exception as e:
        data = {
            'http_code': 404,
            'status': str(e)
        }
    return

@vulnscan.route("/webhook", methods=['POST'])
def xray_webhook():
    '''
    接收xray的漏洞数据
    :return:
    '''

    data = request.json
    if data['type']=='web_vuln':
        url = data['data']['detail']['addr']
        vulntype = data['data']['plugin']
        param = data['data']['detail']['extra']['param']
        payload = data['data']['detail']['payload']
        snapshot = data['data']['detail']['snapshot']
        vuln = Vuln_Table(url=url, vulntype=vulntype, param=str(param),
                      payload=payload, snapshot=str(snapshot),create_user=g.user.suername)
        db.session.add(vuln)
        db.session.commit()
    return 'success'

from scan.awvs_xray import main
@vulnscan.route("/addtask", methods=['POST'])
@login_required
def addtask():
    '''
    添加扫描任务
    :return:
    '''
    urls = request.form.get('urls').split(',')
    print(urls)
    urls = [url for url in urls if get_http_status_code(url)]
    for url in urls:
        pt = Property_Table(url=url, Number_of_vulnerabilities=0, create_user=g.user.username)
        db.session.add(pt)
        db.session.commit()
    # main(urls)
    return redirect(url_for('vulnscan.showProperty'))

from scan.awvs_xray import get_target_status
@vulnscan.route("/showProperty", methods=['GET'])
@login_required
def showProperty():
    '''
    展示添加的资产
    :return:
    '''

    select = request.args.get('filter')
    q = request.args.get('q')
    session['filter'] = select
    session['q'] = q
    if q and select == "property":
        data = Property_Table.query.filter(Property_Table.create_user == g.user.username, Property_Table.url.like("%"+q+"%")).all()
    else:
        data = Property_Table.query.filter(Property_Table.create_user == g.user.username).all()
        for d in data:
            get_amount(d.url) #更新漏洞数
            # 获取d.url的爬虫状态，更新状态
            # status = get_target_status(d.url)
            # if status == 'completed':
            #     d.status = '已完成'
            # elif status == 'failed':
            #     d.status = '失败'
            db.session.commit()
        session.pop('filter', None)
        session.pop('q', None)
    page = int(request.args.get("page", 1))
    # 每页显示 10 条记录
    per_page = 10
    # 计算总页数
    total_pages = (len(data) + per_page - 1) // per_page
    # 对数据集进行分页
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    return render_template("VulnScanPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           filter = session.get('filter', ''),
                           q = session.get('q', ''))


@vulnscan.route("/showInformation/<path:url>", methods=['GET'])
@login_required
def showInformation(url):
    '''
    展示相关的漏洞详情
    :return:
    '''
    session['url'] = url
    data = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.url.like("%"+url+"%")).all()
    page = int(request.args.get("page", 1))
    # 每页显示 10 条记录
    per_page = 10
    # 计算总页数
    total_pages = (len(data) + per_page - 1) // per_page
    # 对数据集进行分页
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    return render_template("VulnInformationPage.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data,
                           url = session.get('url', ''))

@vulnscan.route("/deletetask", methods=['POST'])
@login_required
def deletetask():
    '''
    删除资产以及相应的漏洞
    :return:
    '''
    url = request.args.get('url')
    pt = Property_Table.query.filter(Property_Table.create_user == g.user.username, Property_Table.url == url).all()
    vt = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.url.like("%" + url + "%")).all()
    for p in pt:
        db.session.delete(p)
        db.session.commit()
    for v in vt:
        db.session.delete(v)
        db.session.commit()
    return redirect(url_for('vulnscan.showProperty'))

def get_amount(url):
    '''
    更新漏洞数
    :param url: 目标url
    :return:
    '''
    count = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.url.like("%"+url+"%")).count()
    pt = Property_Table.query.filter(Property_Table.create_user == g.user.username, Property_Table.url == url).first()
    pt.Number_of_vulnerabilities = count
    db.session.commit()
    return count

def get_vuln_amount():
    '''
    获取漏洞类型数量
    :return: 结果data
    '''
    sql_amount = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%sql%")).count()
    xss_amount = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%xss%")).count()
    rce_amount = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%rce%")).count()
    other_amount = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username,
        not_(or_(Vuln_Table.vulntype.like('%sql%'),
        Vuln_Table.vulntype.like('%xss%'),
        Vuln_Table.vulntype.like('%rce%')))).count()
    data = [
        {'sql_amount': sql_amount},
        {'xss_amount': xss_amount},
        {'rce_amount': rce_amount},
        {'other_amount': other_amount}
    ]
    return data

def get_vuln_rank():
    '''
    获取漏洞等级漏洞数
    :return: 结果data
    '''
    sql_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%sql%")).count()
    xss_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%xss%")).count()
    xxe_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%xxe%")).count()
    rce_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%rce%")).count()
    password_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%rce%")).count()
    ssrf_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%ssrf%")).count()
    leak_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%leak%")).count()
    unauth_rank = Vuln_Table.query.filter(Vuln_Table.create_user == g.user.username, Vuln_Table.vulntype.like("%unauth%")).count()
    low_rank = password_rank + leak_rank
    mid_rank = xss_rank + ssrf_rank + xxe_rank
    high_rank = unauth_rank + rce_rank + sql_rank
    data = [
        {'low_rank': low_rank},
        {'mid_rank': mid_rank},
        {'high_rank': high_rank}
    ]
    return data