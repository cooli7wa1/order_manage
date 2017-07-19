#coding:utf8

import wechat, update
import log

if __name__ == '__main__':
    update.Git().createGitThread()
    wechat.wechatMain()

