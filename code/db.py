#coding:utf8
import pymongo, xlrd, json, time
from xls import xls
from config import *
__metaclass__ = type

class MongoDB:

    def __init__(self, table):
        self.client = pymongo.MongoClient(MONGO_URL, connect=False)
        self.db = self.client[MONGO_DB_ORDER_MANAGE]
        self.table = self.db[table]

class Record(MongoDB):

    def __init__(self):
        super(Record, self).__init__(MONGO_TABLE_TEST)

    def checkNickName(self, nick_name):
        cursor = self.table.find({u'nick_name': nick_name})
        if cursor.count() == 0:
            return False
        else:
            return True

    def changeNickName(self, old_name, new_name):
        if not self.checkNickName(old_name):
            return ERROR_OLD_NAME_WRONG
        if self.checkNickName(new_name):
            return ERROR_NEW_NAME_EXIST
        self.table.update_one({u'nick_name': old_name}, {"$set": {u'nick_name':new_name}})
        return 0

    def addNewUser(self, nick_name):
        if self.checkNickName(nick_name):
            return ERROR_NEW_NAME_EXIST
        self.table.insert({u'nick_name': nick_name})
        return 0

    def insertRecord(self, nick_name, good_id, num):
        if not Good().getGoodInfo(good_id):
            return ERROR_GOOD_ID_NOT_EXIST
        cur_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        str = good_id + u'.' + cur_time
        self.table.update_one({u'nick_name': nick_name}, {"$set": {str:num}}, upsert=True)
        return 0

    def getGoodRecord(self, nick_name, good_id):
        if not Good().getGoodInfo(good_id):
            return ERROR_GOOD_ID_NOT_EXIST
        cursor = self.table.find({u'nick_name':nick_name}, {"_id":0})
        if cursor.count() == 0:
            return ERROR_NO_USER_RECORD
        else:
            record = cursor.next()
            return record[good_id] if good_id in record else ERROR_NO_GOOD_RECORD

    def getAllRecords(self, nick_name):
        cursor = self.table.find({u'nick_name':nick_name}, {"_id":0})
        if cursor.count() == 0:
            return ERROR_NO_USER_RECORD
        else:
            record = cursor.next()
            del record[u'nick_name']
            return record

class Good(MongoDB):

    def __init__(self):
        super(Good, self).__init__(MONGO_TABLE_GOODS)

    def updateGoods(self):
        self.db.drop_collection(MONGO_TABLE_GOODS)
        for row_dict in xls(GOODS_XLS_FILE, GOODS_XLS_SHEET_NAME, f_title=GOODS_XLS_PRICE_TITLE).getRowDict():
            # print(json.dumps(row_dict, ensure_ascii=False, encoding='utf8'))
            self.table.insert_one(row_dict)

    def getGoodInfo(self, good_id):
        '''search good_id in db, return good_info if find else None
        '''
        cursor = self.table.find({u'产品代码':good_id}, {"_id":0})
        if cursor.count() != 0:
            return cursor.next()
        else:
            return None

    def getAllGoodsInfo(self):
        cursor = self.table.find({}, {"_id":0})
        if cursor.count() != 0:
            return cursor
        else:
            return None