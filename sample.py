#!/usr/bin/env python3
# coding=utf-8


def onQQMessage(bot, contact, member, content):
    print(contact, member, content)
    if contact.ctype == 'group':
        return

    if content.startswith('[@ME]'):
        print('@me')
        content = content[len('[@ME]'):]
        content = content.strip()
        handleMyMessage(bot, contact, member, content)
    else:
        print('not @me')
        content = content.strip()
        handleCommonMessage(bot, contact, member, content)

def handleCommonMessage(bot, contact, member, content):
    if contact.name == '机器人测试':
        bot.SendTo(contact, content)

def handleMyMessage(bot, contact, member, content):
    print(content)
    if ' ' not in content:
        cmd = content
        msg = ''
    else:
        cmd, msg = content.split(' ', 1)

    if cmd == '-hello':
        bot.SendTo(contact, '你瞅啥')
    elif cmd.startswith('-echo'):
        bot.SendTo(contact, '你说 ' + msg)