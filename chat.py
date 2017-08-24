#!/usr/bin/env python3
# coding=utf-8

import requests
from qqbot import utf8logger as logger


def onQQMessage(bot, contact, member, content):
    # print(contact, member, content)
    # if contact.ctype == 'group' and contact.name != '机器人测试':
    #     return

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
    if not content.startswith('-'):
        cmd = ''
        msg = content
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
    else:
        handle_default_message(bot, contact, member, msg)


def handle_default_message(bot, contact, member, content):
    r = requests.post('http://www.tuling123.com/openapi/api',
                      json={'key': 'a9ea09dc380c4e128d30f97386acc32f', 'info': content, 'userid': member.qq})
    if r.status_code != 200:
        logger.ERROR('data %s', r.json())
        bot.SendTo(contact, '啊！人类无法理解的火星语')
        return
    response = r.json()
    code = response['code']
    msg = ''
    if code == 100000:
        msg = response['text']
    elif code == 200000:
        msg = response['text'] + " " + response['url']
    elif code == 302000:
        msg = response['text']
        msg = msg + '\n\n'.join(('%s %s\n%s' % (n['article'], n['source'], n['detailurl']) for n in response['list']))
    bot.SendTo(contact, msg)
