#!/usr/bin/env python3
# coding=utf-8

def onQQMessage(bot, contact, member, content):
    print(contact, member, content)
    if contact.ctype == 'group' and contact.name != '机器人测试':
        return

    if content.startswith('[@ME]'):
        content = content[len('[@ME]'):]
        content = content.strip()
        handle_my_message(bot, contact, member, content)
    else:
        content = content.strip()
        handle_common_message(bot, contact, member, content)


def get_contact(bot, qq_id):
    l = bot.List('buddy', 'qq=' + qq_id)
    if not l:
        return None
    else:
        return l[0]


def handle_common_message(bot, contact, member, content):
    pass


def handle_my_message(bot, contact, member, content):
    if ' ' not in content:
        cmd = content
        msg = ''
    else:
        cmd, msg = content.split(' ', 1)

    if cmd == '-hello':
        bot.SendTo(contact, '你瞅啥')
    elif cmd.startswith('-echo'):
        bot.SendTo(contact, '你说 ' + msg)
    elif cmd.startswith('-personal'):
        person = get_contact(bot, member.qq)
        if not person:
            return
        bot.SendTo(person, msg)
