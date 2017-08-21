#!/usr/bin/env python3
# coding=utf-8

import time
import sys
import jenkins
from qqbot import _bot as bot

jenkins_server = jenkins.Jenkins(url='http://jenkins.great-tao.com:8080/', username=sys.argv[1], password=sys.argv[2])

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
        # builds = eval("[{'executor': 0, 'name': 'ci-gt-common-timer-dev', 'node': '(master)', 'number': 36, 'url': 'http://jenkins.great-tao.com:8080/job/ci-gt-common-timer-dev/36/'}]")
        builds_dict = {b['name'] : b for b in builds}

        created_builds_dict = {k:v for k,v in builds_dict.items() if k not in running_job_dict}
        notify_created(group, created_builds_dict.values())

        running_job_dict.update(created_builds_dict)

        finished_builds_dict = {k:v for k,v in running_job_dict.items() if k not in builds_dict}
        notify_finished(group, finished_builds_dict.values())

        for k,v in finished_builds_dict.items():
            del running_job_dict[k]

        time.sleep(5)

def find_group(name):
    for group in bot.List('group'):
        if group.name == name:
            return group
    return None

def get_build_user(build):
    for action in build['actions']:
        if action['_class'] == 'hudson.model.CauseAction':
            return action['causes'][0]['userName']

def notify_finished(contact, finished_builds):
    if not finished_builds:
        return
    for build in finished_builds:
        notify(contact, build, False)

def notify_created(contact, created_builds):
    if not created_builds:
        return
    for build in created_builds:
        notify(contact, build, True)

def notify(contact, build, isCreate):
    if not build:
        return
    url = build['url']
    name = build['name']
    number = build['number']
    build_user = get_build_user(jenkins_server.get_build_info(name, number))
    bot.SendTo(contact, '%s %s发布 %s\n%s' % (build_user, '正在' if isCreate else '完成', name, url))

if __name__ == '__main__':
    main()