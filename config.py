import os

SECRET_KEY = os.urandom(24)
# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'vn'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 配置awvs服务器
AWVS_API_KEY = ''  # 替换成你的 AWVS API 密钥
AWVS_URL = 'https://ip:3443'  # 替换成你的 AWVS 服务器地址和端口号
# 配置xray代理服务器
XRAY_IP = ''
XRAY_PORT = ''

# 配置redis
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379
# REDIS_DB = 0
# REDIS_PASSWORD = ''