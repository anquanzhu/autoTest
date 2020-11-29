# -*- coding: utf-8 -*-

'''
    删除 “配置中” 的域名，这种情况下域名不会落库
    数据库中没有该类数据，所以需要通过脚本解决
    1. 找出自动化生产的配置中的域名
    2. 循环去工单系统提交，让它落库
    3. 去数据库删除这些域名
    json.loads str--->json    json.dumps json--->str
'''

import json

from bin.Init import Init
from bin.Mysql import DbConnect
from bin.Workorder import deal_new_domain

"""
    获取域名列表，来源是SCC
"""


def get_config_domain(user_session, host, workspaceid):
    """
        获取进行中的域名（即域名来自SCC，而不是工单系统）
        :param user_session:
        :param host:
        :param workspaceid:
        :return:
    """
    if 'vip' in user_session:
        session = Init.CONSOLE_SESSION
    elif 'ctyun' in user_session:
        session = Init.CTYUN_SESSION
    else:
        session = Init.BS_SESSION
    base_info = Init.BASE_INFO
    domain_info = Init.DOMAIN_INFO
    # session = Init.CONSOLE_SESSION
    # workspaceId = base_info['workspaceid']
    list_domain = host + domain_info['listDomain']
    list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
    list_response = session.get(url=list_domain, params=list_data, headers=base_info['headers_form'], verify=False,
                                timeout=10)
    # print(list_response.text)
    body = json.loads(list_response.text)
    print(type(body))
    print(body)
    domain_list = []
    temp = body['data']['list']
    # print(temp)
    for i in range(len(temp)):
        domain = temp[i]['domain']
        status = temp[i]['status']
        if (status == 3):
            # if ('Auto' in domain) & (status == '3'):
            domain_list.append(domain)
    print(domain_list)
    return domain_list


"""
    获取工单域名列表，来源是工单
"""


def get_order_domain(user_session, host, workspaceid):
    """
    获取进行中的域名（即域名来自工单系统，而不是SCC）
    :param user_session:
    :param host:
    :param workspaceid:
    :return:
    """
    if 'vip' in user_session:
        session = Init.CONSOLE_SESSION
    elif 'ctyun' in user_session:
        session = Init.CTYUN_SESSION
    else:
        session = Init.BS_SESSION
    base_info = Init.BASE_INFO
    domain_info = Init.DOMAIN_INFO
    list_domain = host + domain_info['listDomainV2']
    list_data = 'workspaceId=' + workspaceid + '&do=c_order&from=order'
    list_response = session.get(url=list_domain, params=list_data, headers=base_info['headers_form'], verify=False,
                                timeout=10)
    # print(list_response.text)
    body = json.loads(list_response.text)
    # print(type(body))
    # print(body)
    domain_list = []
    temp = body['data']['list']
    # print(temp)
    count = 0
    for i in range(len(temp)):
        domain = temp[i]['id']
        status = temp[i]['status']
        if (status == '2'):
            # if ('Auto' in domain) & (status == '3'):
            domain_list.append(domain)
            count = count + 1
    print(count, domain_list)
    return domain_list




def get_wo_id(user_session, host, workspaceid):
    """
    获取工单ID,没什么用
    :param user_session:
    :param host:
    :param workspaceid:
    :return:
    """
    if 'vip' in user_session:
        session = Init.CONSOLE_SESSION
    elif 'ctyun' in user_session:
        session = Init.CTYUN_SESSION
    else:
        session = Init.BS_SESSION
    base_info = Init.BASE_INFO
    domain_info = Init.DOMAIN_INFO
    list_domain = host + domain_info['listOrder']
    domain_list = get_order_domain(user_session, host, workspaceid)
    list_data = {"data": {"workspaceId": workspaceid, "page": 1, "page_size": 100, "pageSize": 100,
                          "domainList": domain_list, "orderType": "", "status": "",
                          "startTime": "", "endTime": ""}}

    list_response = session.get(url=list_domain, params=list_data, headers=base_info['headers_json'], verify=False,
                                timeout=10)
    # print(list_response.text)
    body = json.loads(list_response.text)
    # print(type(body))
    print(body)
    wo_list = []
    temp = body['data']['list']
    # print(temp)
    for i in range(len(temp)):
        domain = temp[i]['id']
        status = temp[i]['status']
        if (status == '2'):
            # if ('Auto' in domain) & (status == '3'):
            wo_list.append(domain)
    print(wo_list)
    return wo_list


def deal_config_domain(user_session, host, workspaceid, express):
    """
    删除新增工单里面的进行中的工单---域名
    :param user_session:  使用哪个控制台的session
    :param host:
    :param workspaceid:
    :param express:  数据库表达式
    :return:
    """

    domain_list = get_order_domain(user_session, host, workspaceid)
    for domain in domain_list:
        # 处理新增的域名
        # deal_new_domain(domain, 'createDomainConfigOrder', cnname)
        deal_new_domain(domain)
    DbConnect().delete_doamin(express)


'''
    删除 "删除中" 状态的域名

'''

if __name__ == '__main__':
    # deal_config_domain('vip', 'https://iam-test.ctcdn.cn', '10001510', '周琪')
    # deal_config_domain('vip', 'https://iam-test.ctcdn.cn', '10003885', '陈孟琪')
    # get_order_domain('vip', 'https://iam-test.ctcdn.cn', '10003885')

    deal_config_domain('vip', 'https://iam-test.ctcdn.cn', '10003885',
                       'client_id=\'14444\' and (domain like \'Auto%\' or domain like \'V1%\')')
