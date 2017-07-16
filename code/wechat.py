#coding:utf8
import itchat, threading, re, json, random
from config import *
from db import Good, Record
import helpers
__metaclass__ = type

monitor_rooms = []

class Room:

    def getRoomUserNameByNickName(self, nick_name):
        try:
            logging.debug(u'==== 开始 ====')
            rooms = itchat.get_chatrooms()
            for i in range(len(rooms)):
                if rooms[i][u'NickName'] == nick_name:
                    return rooms[i][u'UserName']
        finally:
            logging.debug(u'==== 结束 ====')

    def initRoom(self):
        for r in WECHAT_ROOM_LIST:
            monitor_rooms.append(self.getRoomUserNameByNickName(r))

class SendMsg:

    send_lock = threading.Lock()
    def formatMsg(self, type, title, msg_ori):
        logging.debug(u'==== 开始 ====')
        msg = u''
        msg += title
        if type == 'cjl_a':
            for good_id in msg_ori:
                msg += u'=== 产品编号【%s】===\n' % good_id
                for record in msg_ori[good_id]:
                    msg += u'%s【%s】\n' % (record, msg_ori[good_id][record])
        elif type == 'cjl_s':
            for record in msg_ori:
                msg += u'%s【%s】\n' % (record, msg_ori[record])
        elif type == 'cpxx_a':
            for info in msg_ori:
                msg += u'%s\n' % info
        elif type == 'cpxx_s':
            for item in msg_ori:
                detail_js = json.dumps(msg_ori[item], ensure_ascii=False, encoding='utf8')
                if item == u'终端最低指导价/集团价':
                    item = u'最低指导价'
                item_js = json.dumps(item, ensure_ascii=False, encoding='utf8')
                msg += u'【%s】%s\n' % (item_js, detail_js)
        elif type == 'no_user':
            msg += u'\u2728您是新用户：\n' \
                  u'输入【新用户】，为您开通账号' \
                  u'\u2728您是老用户但更改了昵称：\n' \
                  u'输入【更新昵称#旧昵称】'
        logging.debug(u'==== 开始 ====')
        return msg

    def sendMsg(self, msg, to):
        delay = [1.5,1.6,1.7,1.8,1.9,2.0]
        SendMsg.send_lock.acquire()
        time.sleep(random.choice(delay))
        itchat.send('@msg@%s' % msg, to)
        SendMsg.send_lock.release()

class DealMsg:

    def dealGroupMsg(self, msg):
        ''' current cmd_list:
            录入#编号#数量：录入
            查记录：查看所有编号产品的记录 ==》 编号：日期：数量
            查记录#编号：查看指定编号产品的记录 ==》 日期：数量
            产品信息：查看所有编号产品的简要信息 ==》 代码，名称，规格
            产品信息#编号：查看制定编号产品的相关信息 ==》 详细信息
            帮助

            新用户：开通新用户
            更新昵称#旧昵称：更新数据库中用户的昵称
        '''
        logging.debug(u'==== 开始 ====')
        try:
            nick_name = msg[u'ActualNickName']
            to = msg[u'FromUserName']
            cmd = msg['Text'].strip()
            if re.match(u'录入#.+#.+', cmd):
                logging.debug(u'收到录入命令')
                if not Record().checkNickName(nick_name):
                    logging.debug(u'没有此人')
                    m = SendMsg().formatMsg('no_user', u'@%s 数据库中没有您的记录\n' % nick_name, '')
                    SendMsg().sendMsg(m, to)
                    return
                good_id, num = cmd.split('#')[1:]
                ret = Record().insertRecord(nick_name, good_id, num)
                if ret < 0:
                    if ret == ERROR_GOOD_ID_NOT_EXIST:
                        logging.debug(u'没有此产品')
                        SendMsg().sendMsg(u'@%s 没有此产品，编号正确？' % (nick_name), to)
                SendMsg().sendMsg(u'@%s 录入成功\n【%s】%s' % (nick_name, good_id, num), to)
                return
            elif cmd == u'查记录':
                logging.debug(u'收到查所有记录命令')
                if not Record().checkNickName(nick_name):
                    logging.debug(u'没有此人')
                    m = SendMsg().formatMsg('no_user', u'@%s 数据库中没有您的记录\n' % nick_name, '')
                    SendMsg().sendMsg(m, to)
                    return
                record = Record().getAllRecords(nick_name)
                if record < 0:
                    if record == ERROR_NO_USER_RECORD:
                        logging.debug(u'当前用户没有任何数据记录')
                        SendMsg().sendMsg(u'@%s 没有您的记录' % nick_name, to)
                        return
                else:
                    logging.debug(record)
                    m = SendMsg().formatMsg('cjl_a', u'@%s 所有记录：\n' % nick_name, record)
                    SendMsg().sendMsg(m, to)
            elif re.match(u'查记录#.+', cmd):
                logging.debug(u'收到查记录命令')
                if not Record().checkNickName(nick_name):
                    logging.debug(u'没有此人')
                    m = SendMsg().formatMsg('no_user', u'@%s 数据库中没有您的记录\n' % nick_name, '')
                    SendMsg().sendMsg(m, to)
                    return
                good_id = cmd.split('#')[1]
                record = Record().getGoodRecord(nick_name, good_id)
                if record < 0:
                    if record == ERROR_NO_USER_RECORD:
                        logging.debug(u'当前用户没有任何数据记录')
                        SendMsg().sendMsg(u'@%s 没有您的记录' % nick_name, to)
                    elif record == ERROR_NO_GOOD_RECORD:
                        logging.debug(u'当前用户没有此产品记录')
                        SendMsg().sendMsg(u'@%s 没有此产品的记录' % nick_name, to)
                    elif record == ERROR_GOOD_ID_NOT_EXIST:
                        logging.debug(u'没有此产品')
                        SendMsg().sendMsg(u'@%s 没有此产品' % nick_name, to)
                    return
                else:
                    logging.debug(record)
                    m = SendMsg().formatMsg('cjl_s', u'@%s 【%s】记录：\n' % (nick_name, good_id), record)
                    SendMsg().sendMsg(m, to)
            elif cmd == u'产品信息':
                logging.debug(u'收到查看所有产品信息的命令')
                good_info = Good().getAllGoodsInfo()
                if not good_info:
                    logging.debug(u'没有产品')
                    SendMsg().sendMsg(u'@%s 产品数据库为空，没有任何产品' % nick_name, to)
                    return
                else:
                    all_goods_info = []
                    for good_info in Good().getAllGoodsInfo():
                        s = u'【%s】%s,%s' % (good_info[u'产品代码'], good_info[u'名称'], good_info[u'产品规格'])
                        simple_info_js = json.dumps(s, ensure_ascii=False, encoding='utf8')
                        logging.debug(simple_info_js)
                        all_goods_info.append(simple_info_js)
                    m = SendMsg().formatMsg('cpxx_a', u'@%s 所有产品列表：\n' % nick_name, all_goods_info)
                    SendMsg().sendMsg(m, to)
            elif re.match(u'产品信息#.+', cmd):
                logging.debug(u'收到查看产品信息命令')
                good_id = cmd.split('#')[1]
                good_info = Good().getGoodInfo(good_id)
                if not good_info:
                    logging.debug(u'没有此产品')
                    SendMsg().sendMsg(u'@%s 没有此产品' % nick_name, to)
                    return
                else:
                    simple_info_js = json.dumps(good_info, ensure_ascii=False, encoding='utf8')
                    logging.debug(simple_info_js)
                    m = SendMsg().formatMsg('cpxx_s', u'@%s 【%s】详细信息：\n' % (nick_name, good_id), good_info)
                    SendMsg().sendMsg(m, to)
            elif cmd == u'新用户':
                logging.debug(u'收到新用户命令')
                ret = Record().addNewUser(nick_name)
                if ret < 0:
                    if ret == ERROR_NEW_NAME_EXIST:
                        logging.debug(u'用户名已经存在')
                        SendMsg().sendMsg(u'@%s 用户名已经存在\n请更改您的群内昵称后再试' % nick_name, to)
                        return
                else:
                    SendMsg().sendMsg(u'@%s 开通账号成功\n重新输入命令吧' % nick_name, to)
                    return
            elif re.match(u'更新昵称#.+', cmd):
                logging.debug(u'收到更新昵称命令')
                old_name = cmd.split('#')[1]
                ret = Record().changeNickName(old_name, nick_name)
                if ret < 0:
                    if ret == ERROR_OLD_NAME_WRONG:
                        logging.debug(u'没找到旧昵称')
                        SendMsg().sendMsg(u'@%s 没有此旧昵称' % nick_name, to)
                    elif ret == ERROR_NEW_NAME_EXIST:
                        logging.debug(u'新昵称已经存在')
                        SendMsg().sendMsg(u'@%s 用户名已经存在\n请更改您的群内昵称后再试' % nick_name, to)
                    return
                else:
                    SendMsg().sendMsg(u'@%s 更新昵称成功\n重新输入命令吧' % nick_name, to)
                    return
            elif cmd == u'帮助':
                logging.debug(u'收到帮助命令')
                m = helpers.getCmdList()
                SendMsg().sendMsg(m, to)
            else:
                return
        finally:
            logging.debug(u'==== 结束 ====')

    def dealSingleMsg(self, msg):
        # elif cmd == u'更新产品':
        # logging.debug(u'收到更新产品命令')
        # Good().updateGoods()
        # logging.debug(u'更新产品结束')
        pass

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def recGroupMsg(msg):
    if msg['FromUserName'] not in monitor_rooms:
        return
    p = threading.Thread(target=DealMsg().dealGroupMsg, args=(msg,))
    p.setDaemon(True)
    p.start()
    return

@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def recSingleMsg(msg):
    if msg['FromUserName'] not in monitor_rooms:
        return
    p = threading.Thread(target=DealMsg().dealSingleMsg, args=(msg,))
    p.setDaemon(True)
    p.start()
    return

def wechatMain():
    itchat.auto_login(picDir=WECHAT_QR_PATH, hotReload=True)
    time.sleep(1)
    Room().initRoom()
    itchat.run()