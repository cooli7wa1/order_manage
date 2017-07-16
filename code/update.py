#coding:utf8
import threading
from config import *

class Git:

    def _updateToGit(self):
        logging.debug('==== GIT开始上传数据')
        cnt = 0
        os.chdir(MONGO_DB_DUMP_FOLD)
        os.system('mongodump -d order_manage')
        os.chdir(DATA_FOLD)
        os.system('git add --all')
        os.system('git commit -m "robot update"')
        while True:
            ret = os.system('git push origin master')
            if ret == 0:
                logging.debug('==== GIT上传成功')
                return 0
            else:
                cnt += 1
                logging.debug('==== GIT本次上传失败， cnt: %d' % cnt)
                if cnt >= 3:
                    logging.error('==== GIT上传失败， cnt: %d' % cnt)
                    return -1

    def _updateThread(self):
        while True:
            self._updateToGit()
            time.sleep(GIT_UPLOAD_INTERVAL)

    def createGitThread(self):
        git_thread = threading.Thread(target=self._updateThread)
        git_thread.setDaemon(True)
        git_thread.start()
        git_thread.name = u'GIT thread ' + time.strftime('%d_%H%M%S', time.localtime(time.time()))
        logging.debug('==== thread name is ' + git_thread.name.encode('utf-8'))

