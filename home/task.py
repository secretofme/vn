#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : task.py

from flask import Blueprint,request,render_template,flash,g,url_for,redirect
from utils.decorators import  login_required
from model.models import TaskList,Domain_Table,Port_Table,Spider_Table,Fingerprint_Table
from model.exts import db
import requests
import subprocess
import time

processes = {}

task = Blueprint("task", __name__)

@task.route("/tasklist", methods=['GET'])
@login_required
def tasklist():
    print(processes)
    data = TaskList.query.filter(TaskList.create_user == g.user.username).order_by(TaskList.id.desc()).all()
    page = int(request.args.get("page", 1))
    # 每页显示 10 条记录
    per_page = 10
    # 计算总页数
    total_pages = (len(data) + per_page - 1) // per_page
    # 对数据集进行分页
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    return render_template("TaskList.html",
                           page=page,
                           per_page=per_page,
                           total_pages=total_pages,
                           data=page_data)

def addscan(scan_process,taskname):
    global processes
    task = TaskList()
    task = task.create_task(create_user=g.user.username, taskname=taskname, pid=scan_process.pid)
    # 将进程对象存储到字典中
    processes[scan_process.pid] = scan_process
    print(processes)
    # 等待进程结束并获取输出结果
    output, error = scan_process.communicate()
    result = eval(output.decode().strip().split('\n')[0])
    # result = output.decode().strip().split('\n')[0]
    print(result)
    task.completed()
    # 从字典中移除进程对象
    processes.pop(scan_process.pid)
    return result

def addtask(taskname,**kwargs):
    if taskname=='端口扫描':
        print(kwargs['ips'], kwargs['port'], kwargs['max_threads'])
        # 启动端口扫描进程
        port_process = subprocess.Popen(["python", "scan/Nmap_port_scan.py", str(kwargs['ips']), str(kwargs['port']),str(kwargs['max_threads'])], stdout=subprocess.PIPE)
        result = addscan(port_process,taskname)
        for i in result:
            check = Port_Table.query.filter(Port_Table.create_user == g.user.username,Port_Table.target_ip == i[0],Port_Table.target_port == i[1]).first()
            if check:
                continue
            else:
                add_result = Port_Table(create_user=g.user.username, target_ip=i[0], target_port=i[1], status=i[2],service=i[3], version=i[4])
                db.session.add(add_result)
                db.session.commit()
        flash('扫描结束')

    elif taskname=='域名探测':
        print(kwargs['domain'], kwargs['max_threads'])
        domain_process = subprocess.Popen(["python", "scan/aizhan_domain.py", kwargs['domain']], stdout=subprocess.PIPE)
        result = addscan(domain_process,taskname)
        for i in result:
            check = Domain_Table.query.filter(Domain_Table.create_user == g.user.username,Domain_Table.subdomain == i).first()
            if check:
                continue
            else:
                add_result = Domain_Table(create_user=g.user.username, domain=kwargs['domain'], subdomain=i)
                db.session.add(add_result)
                db.session.commit()
        flash('扫描结束')

    elif taskname=='爬虫':
        print(kwargs['url'], kwargs['deepth'])
        spider_process = subprocess.Popen(["python", "scan/spider.py", kwargs['url'], str(kwargs['deepth'])], stdout=subprocess.PIPE)
        result = addscan(spider_process,taskname)
        for i in result:
            check = Spider_Table.query.filter(Spider_Table.create_user == g.user.username,Spider_Table.urllist == i).first()
            if check:
                continue
            else:
                code = requests.get(kwargs['url']).status_code
                add_result = Spider_Table(create_user=g.user.username, url=kwargs['url'], urllist=i, code=code)
                db.session.add(add_result)
                db.session.commit()
        flash('爬取完成')

    elif taskname=='指纹识别':
        print(kwargs['url'])
        fingerprirnt_process = subprocess.Popen(["python", "scan/wappalyzer.py", kwargs['url']],stdout=subprocess.PIPE)
        result = addscan(fingerprirnt_process, taskname)
        check = Fingerprint_Table.query.filter(Fingerprint_Table.create_user == g.user.username,Fingerprint_Table.url == kwargs['url']).first()
        if check:
            check.fingerprint = result['apps']
            check.title = result['title']
            db.session.commit()
        else:
            add_result = Fingerprint_Table(create_user=g.user.username, url=kwargs['url'], fingerprint=result['apps'], title=result['title'])
            db.session.add(add_result)
            db.session.commit()
        flash('识别完成')

@task.route("/tasklist/<id>", methods=['GET'])
@login_required
def stoptask(id):
    global processes
    # 获取需要终止的进程 ID
    task = TaskList.query.filter(TaskList.create_user == g.user.username, TaskList.id == id).first()
    if task.status=="completed" or not len(processes):
        db.session.delete(task)
        db.session.commit()
        flash('任务删除成功')
        return redirect(url_for('task.tasklist'))

    pid = int(task.pid)
    # 检查是否有对应的进程正在运行
    if pid in processes:
        # 终止进程并从字典中移除
        process = processes.pop(pid)
        process.kill()
        db.session.delete(task)
        db.session.commit()
        flash('任务删除成功')
        print(processes)
    return redirect(url_for('task.tasklist'))
