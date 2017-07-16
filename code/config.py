#coding:utf8
import os, logging, time

BASE_PATH = os.popen('echo $HOME').read().replace('\n','') + u'/Documents/'
DATA_FOLD = BASE_PATH + u'order_manage_data/'
CODE_FOLD = BASE_PATH + u'order_manage/'

# GIT
GIT_UPLOAD_INTERVAL = 60*60*2  # 2小时，GIT同步的频率
MONGO_DB_DUMP_FOLD = DATA_FOLD + u'mongodb/'

# wechat
WECHAT_ROOM_LIST = [u'测试群']
WECHAT_QR_PATH = DATA_FOLD + u'/QR.png'

# mongodb
GOODS_XLS_FILE = DATA_FOLD + u'17-18年财务年销售政策及任务.xls'
GOODS_XLS_SHEET_NAME = u'价格体系'
GOODS_XLS_PRICE_TITLE = (u'终端最低指导价/集团价',u'出厂价')
MONGO_URL = 'localhost'
MONGO_DB_ORDER_MANAGE = 'order_manage'
MONGO_TABLE_TEST = 'test'
MONGO_TABLE_GOODS = 'goods'

# ERROR
ERROR_NO_USER_RECORD = -1
ERROR_NO_GOOD_RECORD = -2
ERROR_GOOD_ID_NOT_EXIST = -3
ERROR_OLD_NAME_WRONG = -4
ERROR_NEW_NAME_EXIST = -5

# LOG
LOG_FOLD = DATA_FOLD + u'log/'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='%s%s.log' % (LOG_FOLD, time.strftime('%Y-%m-%d-%H%M%S', time.localtime())),
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
