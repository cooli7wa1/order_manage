#coding:utf8
import logging, time
from config import DATA_FOLD

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