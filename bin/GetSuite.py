# -*- coding: utf-8 -*-

"""
读取yaml测试数据 ,TODO 考虑数据传递各种文件，函数的情况

"""
import json

import yaml
import os
import os.path

from bin.unit import Log
from bin.unit.Rondom import random_string, random_int, random_float

file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


# def replace_random(parm):
#     # dict = ['$random_string$', '$random_int$', '$random_float$']
#     new_parm = None
#     file_list = walkfile('/testcase/params/')
#     if parm.find('$random_string$'):
#         new_parm = parm.replace('$random_string$', random_string(8))
#     elif parm.find('$random_int$'):
#         if (new_parm != None):
#             new_parm = new_parm.replace('$random_int$', random_int('1000,10000'))
#         else:
#             new_parm = parm.replace('$random_int$', random_int('1000,10000'))
#     elif parm.find('$random_float$'):
#         if (new_parm != None):
#             new_parm = new_parm.replace('$random_float$', random_float('1000,10000,2'))
#         else:
#             new_parm = parm.replace('$random_float$', random_float('1000,10000,2'))
#     # print(new_parm)
#
#     else:
#         new_parm = parm
#     # print('new:', new_parm)
#     for item in file_list:
#         if parm.find(item):
#             if (new_parm != None):
#                 new_parm = new_parm.replace(item, read(item))
#             else:
#                 new_parm = parm.replace(item, read(item))
#         else:
#             new_parm = parm
#     return new_parm


def parse():
    path_ya = file_path + '/testcase/yaml'
    # print(path_ya)
    cases_list = []
    for root, dirs, files in os.walk(path_ya):
        for name in files:
            watch_file_path = os.path.join(root, name)
            with open(watch_file_path, 'r', encoding='utf-8') as f:
                case = yaml.safe_load(f)
                cases_list.append(case)
    return cases_list


def read(filename):
    path = file_path
    if filename is None:
        Log.info()
    f = open(path + filename, 'r', encoding='utf-8')
    # print(f.read())
    return f.read()


def walkfile(path):
    # path = file_path + path  # '/testcase/params'
    # print(path)
    file_list = []
    for root, dirs, files in os.walk(path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            # print(os.path.join(root, f))
            file_list.append(f)
        # 遍历所有的文件夹
        # for d in dirs:
        #     print(3,os.path.join(root, d))
    # print(file_list)
    return file_list


"""
读取某一个具体的yaml文件测试数据

"""


def get_suite(name):
    data = get_all_cases()
    param = None
    log = Log.Log()
    for i in range(len(data)):
        # for items in data[i]:
        if name in data[i].keys():
            param = data[i][name]

    if param == None:
        param = name
        log.info('please check your suite name ')

    return param


def get_all_cases():
    cases = parse()
    cases_list = []
    for i in range(len(cases)):
        case = json.dumps(cases[i], ensure_ascii=False)
        temp = replace_random(case)
        json_list = json.loads(temp, strict=False)
        cases_list.append(json_list)
    return cases_list


if __name__ == '__main__':
    # lists = GetCases.get_case_list()
    # walkfile()
    # print(lists)
    ss = 'dfasdgds' + '$random_string$' + '222' + '$random_int$' + '$random_float$'
    # replace_random('/cdn/gw/cert/CreateCert')
    # get_case_list()
    # get_cases()
    get_suite('creatCert')
    get_suite('abc')
