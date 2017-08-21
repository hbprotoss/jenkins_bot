#!/usr/bin/env python3
# coding=utf-8

import time
import jenkins
from qqbot import _bot as bot

jenkins_server = jenkins.Jenkins(url='http://jenkins.great-tao.com:8080/', username='hubin', password='QtVShbCMoIyN0pAV')

def main():
    qq_id = '136314998'
    group_name = '机器人测试'
    running_job_dict = {}

    bot.Login(['-q', qq_id])
    group = find_group(group_name)
    if not group:
        print('找不到群' + group_name)
        quit()

    while True:
        builds = jenkins_server.get_running_builds()
        builds_dict = {b.name : b for b in builds}
        finished_builds = running_job_dict - builds_dict
        time.sleep(5)

def find_group(name):
    for group in bot.List('group'):
        if group.name == name:
            return group
    return None

if __name__ == '__main__':
    main()