#!.usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : B1u
# @File   : Nmap_port_scan.py

'''
端口扫描
'''
import nmap
import threading
import queue
import sys

lock = threading.Lock()  # 线程锁对象
scan_results = []

def scan(target_host, target_port):
    try:
        scanner = nmap.PortScanner()
        results = scanner.scan(hosts=target_host, ports=str(target_port), arguments='-T4 -A -v -Pn ')  # 禁ping的快速扫描
        state = results['scan'][target_host]['tcp'][target_port]['state']
        service = results['scan'][target_host]['tcp'][target_port]['product']
        version = results['scan'][target_host]['tcp'][target_port]['version']
        # 将扫描结果添加到全局变量中
        if state == "open":
            scan_results.append([target_host, target_port, state, service, version])
    except Exception as e:
        print(f"[ERROR] Scan {target_host}:{target_port} failed: {str(e)}")

def worker(q):
    while True:
        item = q.get()
        if item is None:
            break
        ip, port = item
        scan(ip, port)
        q.task_done()


def run_scan(ip_list, port_list, max_threads=10):
    q = queue.Queue()
    threads = []
    for ip in ip_list:
        for port in port_list:
            q.put((ip, int(port)))

    # 启动线程
    for i in range(max_threads):
        t = threading.Thread(target=worker, args=(q,))
        threads.append(t)
        t.start()

    # 等待所有任务完成
    q.join()

    # 停止所有线程
    for i in range(max_threads):
        q.put(None)
    for t in threads:
        t.join()
    with lock:
        result = scan_results.copy()
        scan_results.clear()  # 清空全局变量
    return result

if __name__ == '__main__':
    ips = sys.argv[1].strip("[]' ").split("', '")
    port = sys.argv[2].strip("[]' ").split("', '")
    max_threads = sys.argv[3]
    result = run_scan(ips, port, int(max_threads))
    print(result)