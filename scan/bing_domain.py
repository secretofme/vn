import requests
from urllib.parse import urlparse
from utils.randomAgent import getRandomUserAgent
import re
import threading
import sys

def search_subdomains_domain(domain, result_list, thread_num):
    """
    使用Bing搜索引擎查找给定域名的子域名，并将结果存储在列表中。
    """
    # 构造搜索URL
    headers = getRandomUserAgent()
    url = f'https://cn.bing.com/search?q=site%3A{domain}'
    # 发送HTTP请求
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except:
        return

    # 提取子域名
    results = response.text.split('<cite>')[1:]
    subdomains = []
    for result in results:
        subdomain = re.sub('<.*?>', '', result.split('</cite>')[0]).strip()
        if subdomain.endswith(domain):
            continue
        parsed_uri = urlparse(subdomain)
        domain_name = '{uri.netloc}'.format(uri=parsed_uri)
        if domain_name not in subdomains:
            subdomains.append(domain_name)

    # 将子域名列表加入到结果列表中
    with thread_num:
        result_list.extend(subdomains)

def search_subdomains(domain, max_threads):
    """
    使用多线程方式搜索给定域名的子域名，并返回结果列表。
    """
    # 创建结果列表
    result_list = []
    # 创建锁对象
    lock = threading.Lock()
    # 创建线程列表
    thread_list = []
    # 启动多个线程
    for i in range(max_threads):
        t = threading.Thread(target=search_subdomains_domain, args=(domain, result_list, lock))
        t.start()
        thread_list.append(t)

    # 等待所有线程执行完毕
    for t in thread_list:
        t.join()

    # 对子域名列表进行去重操作
    result = list(set(result_list))
    result = [x for x in result if x != '']
    return result

if __name__ == '__main__':
    domain = sys.argv[1]
    max_threads = sys.argv[2]
    result = search_subdomains(domain, int(max_threads))
    print(result)
