#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from datetime import datetime

import itchat

reload(sys)
sys.setdefaultencoding('utf8')


class itchatSender(object):
    '''
    Automatically send message to chatroom on time according to user's predefinition.
    params:
            `roomName`: The name of chatroom you want to send message to;
            `context`: The message you want to send to chatroom;
            `time`: Time to send out message, in form of a dict.
    Usage:
            Please refer to the __main__ function part.
    '''

    def __init__(self, roomName='', context='', isRoom="True"):
        self.roomName = roomName
        self.context = context
        itchat.auto_login(
            hotReload=True,
            loginCallback=self.loginCallback,
            exitCallback=self.exitCallback,
            statusStorageDir='newInstance2.pkl')
        print "isRoom"
        print isRoom == "True"
        if isRoom == "True":
            self.sendChatroomMsg(roomName, context)
        else:
            print "isRoom"
            print isRoom
            self.sendMPSMsg(roomName, context)

    def sendChatroomMsg(self, roomName, context):
        itchat.get_chatrooms(update=True)
        roomNickName = roomName
        candidates = itchat.search_chatrooms(name=roomNickName)
        print candidates
        username = ''
        for candidate in candidates:
            print candidate['NickName']
            if candidate['NickName'] == roomNickName:
                username = candidate['UserName']
                break
        if username:
            msg = "{}\n\n消息由爬虫自动发送".format(context)
            itchat.send_msg(msg=msg, toUserName=username)

    def sendMPSMsg(self, roomName, context):
        friends_list = itchat.get_friends(update=True)
        name = itchat.search_friends(name=roomName)
        userName = name[0]["UserName"]
        itchat.send(context, userName)

    def loginCallback(self):
        print "Successfully logged in."

    def exitCallback(self):
        print "Successfully logged out."


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='itchat sender')

    parser.add_argument('--msg', dest='msg', help='message')
    parser.add_argument('--chatroom', dest='chatroom', help='chatroom')
    parser.add_argument('--ischatroom', dest='ischatroom',
                        default="True", help='chatroom')

    args = parser.parse_args()

    itchatSender(roomName=args.chatroom, context=args.msg,
                 isRoom=args.ischatroom)
