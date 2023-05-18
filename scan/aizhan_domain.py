import requests
from bs4 import BeautifulSoup
import sys

def search_subdomains(domain):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://www.baidu.com/'
    }
    url = f"https://baidurank.aizhan.com/baidu/{domain}/"
    html = requests.get(url, stream=True, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    job_bt = soup.find('ul', class_="clearfix")
    a_tags = job_bt.find_all('a')
    subdomain = [a.text.strip() for a in a_tags]
    return list(set(subdomain))

if __name__ == '__main__':
    domain = sys.argv[1]
    # domain = 'hnnd.com.cn'
    result = search_subdomains(domain)
    print(result)
