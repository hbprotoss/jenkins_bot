#!/usr/bin/env python3
# coding=utf-8

import sys
from qqbot import _bot as bot


bot.Login(['-u', 'bot'])
l = bot.List('buddy', '416493840')
bot.Run()
