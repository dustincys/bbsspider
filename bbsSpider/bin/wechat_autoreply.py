#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from datetime import datetime

import itchat
import sqlite3

conn = sqlite3.connect('/home/dustin/temp/houstonbbskey')

# conn.execute(
#     "INSERT INTO pt values('{0}');".format("哈哈test"))
# conn.execute(
#     "DELETE FROM pt WHERE('{0}');".format("哈哈test"))
# cursor = conn.execute("select * from pt")
# print u"-{0}".format("-".join([row[0] for row in cursor]))
# conn.close()

reload(sys)
sys.setdefaultencoding('utf8')

newInstance = itchat.new_instance()

newInstance.auto_login(
    hotReload=True,
    statusStorageDir='/home/dustin/temp/newInstance.pkl')


@newInstance.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_reply_text(msg):
    if msg['IsAt']:
        msgContent = msg['Content'].strip("@石见 石页")
        msgContent = msgContent.strip()
        if msgContent.startswith("+") or msgContent.startswith("-"):
            if msgContent.startswith("+"):
                hbbskey = msgContent.strip("+")
                conn.execute(
                    "DELETE FROM nt WHERE('{0}');".format(hbbskey))
                conn.execute(
                    "INSERT INTO pt values('{0}');".format(hbbskey))

            elif msgContent.startswith("-"):
                hbbskey = msgContent.strip("-")
                conn.execute(
                    "DELETE FROM pt WHERE('{0}');".format(hbbskey))
                conn.execute(
                    "INSERT INTO nt values('{0}');".format(hbbskey))
                pass

            newInstance.send('@%s I received: %s, key database updated' %
                             (msg['ActualNickName'], msgContent), msg['FromUserName'])
            pcursor = conn.execute("SELECT * from pt")
            ncursor = conn.execute("SELECT * from nt")
            plist = [row[0] for row in pcursor]
            nlist = [row[0] for row in ncursor]
            newInstance.send(
                u"{0}\n{1}".format(
                    u'positive key: +{0}'.format("+".join(plist)),
                    u'negative key: -{0}'.format("-".join(nlist))),
                msg['FromUserName'])
            pass
        pass
    return


newInstance.run()
