# -*- coding: utf-8 -*-

import os
import sys

import yaml

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def readYaml(yamlname):
    """
    读取yaml文件，root_dir为项目的根目录
    :param yamlname: 从根目录出发，达到的yaml具体路径
    :return: yaml文件的所有内容，dict 类型
    """
    yamlPath = os.path.join(root_dir, yamlname)
    f = open(yamlPath, 'r', encoding='utf-8')
    content = yaml.load(f.read(), Loader=yaml.FullLoader)
    return content


def writeYaml(yamlname, data):
    """
    写入数据到yaml文件
    :param yamlname: 从根目录出发，达到的yaml具体路径
    :param data: 想要写入yaml的数据
    :return:
    """
    yamlPath = os.path.join(root_dir, yamlname)
    # a 追加写入，w,覆盖写入
    fw = open(yamlPath, 'a', encoding='utf-8')
    # 构建数据,注意必须是dict格式，key-value
    # 装载数据
    yaml.dump(data, fw, encoding='utf-8')


def get_env():
    argv_len = len(sys.argv)
    temp = ''
    if argv_len > 1:
        temp = sys.argv[1]
    if temp == 'ite':
        env = 'ITE'
    elif temp == 'pe' or temp == 'PE':
        env = 'PE'
    else:
        env = 'ITE'
    return env


# env = readYaml('application.yaml').get('ENV')


def choose_Yaml():
    '''
    集成测试环境 Integrated Test Environment ； ITE
    自动化测试环境 Automated test environment ；ATE
    生产环境 production environment ； PE
    :return:
    '''
    env = get_env()
    print("当前测试环境：", env)
    if env == 'ITE':
        content = readYaml('params/cdn/base_ite.yaml')
        # log.info('当前环境：' + env)
    elif env == 'ATE' or env == 'ate':
        content = readYaml('params/cdn/base_ate.yaml')
        # log.info('当前环境：' + env)
    elif env == 'PE' or env == 'pe':
        content = readYaml('params/cdn/base_pe.yaml')
        # log.info('当前环境：' + env)
    else:
        content = ''
        print("环境变量错误，请检查!")
        # log.error('环境变量错误，请检查applicationg.yaml!')
    return content


def choose_v1yaml():
    '''
    集成测试环境 Integrated Test Environment ； ITE
    生产环境 production environment ； PE
    :return:
    '''
    env = get_env()
    if env == 'ITE':
        content = readYaml('params/cdn/v1_test.yaml')
        print("当前环境：" + env)
        # log.info('当前环境：' + env)
    elif env == 'PE' or env == 'pe':
        content = readYaml('params/cdn/v1_pe.yaml')
        print("当前环境：" + env)
        # log.info('当前环境：' + env)
    else:
        content = ''
        print("环境变量错误，请检查!")
        # log.error('环境变量错误，请检查applicationg.yaml!')
    return content


if __name__ == '__main__':
    print(get_env())
    # aa=readYaml('params/cdn/base.yaml')
    # print(aa)
    # data = {
    #     "cookie1": {'domain': '.yiyao.cc', 'expiry': 1521558688.480118, 'httpOnly': False, 'name': '_ui_', 'path': '/',
    #                 'secure': False, 'value': 'HSX9fJjjCIImOJoPUkv/QA=='}}
    # writeYaml('application.yaml', data)
    # print(readYaml("params/cdn/v1.yaml"))
    # print(readYaml('application.yaml').get('ENV'))
