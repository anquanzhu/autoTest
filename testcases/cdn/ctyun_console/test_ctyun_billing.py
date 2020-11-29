# -*- coding: utf-8 -*-

"""
CTYUN客户控制台，计费详情模块相关接口

"""
import json
import random

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData


@allure.feature('CTYUN客户控制台计费详情模块')
class Test_Ctyun_Billing():

    def setup_class(self):
        # print('test start')
        self.session = Init.CTYUN_SESSION
        self.base_info = Init.BASE_INFO
        self.console_host = self.base_info['ctyunHost']
        self.workspace_id = self.base_info['ctyun_workspaceid']
        self.head_json = self.base_info['headers_json']
        self.today = CreateLogData().day_time
        self.now = CreateLogData().now_time
        self.head_form = self.base_info['headers_form']

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story('flowpacket/ListV3 查all')
    def test_CDN_246289(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ListV3'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ListV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'account_id' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('flowpacket/ListV3 接口1')
    def test_CDN_246290(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ListV3'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&productCode=001'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ListV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'account_id' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('flowpacket/ListV3 接口2')
    def test_CDN_246291(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ListV3'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&productCode=003'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ListV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'account_id' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('flowpacket/ListV3 接口3')
    def test_CDN_246293(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ListV3'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&productCode=004'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ListV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'account_id' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('flowpacket/ListV3 接口4')
    def test_CDN_246292(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ListV3'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&productCode=005'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ListV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'account_id' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('flowpacket/HistoryV3 接口')
    def test_CDN_246294(self):
        temp = self.console_host + '/cdn/gw/flowpacket/HistoryV3'
        data = '?workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/HistoryV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'list' in response.text
        assert response.elapsed.total_seconds() < 3

    """
    CTYUN 控制台，用户可以反复修改计费方式，VIP和BS则不能修改
    /cdn/gw/flowpacket/ChangeV3?workspaceId=10039265&resourceId=592c46e4cd0c4edc8adfce23f040efa4&resourceType=001&billingType=2&_t=1601430123751
    /cdn/gw/flowpacket/ChangeV3?workspaceId=10039265&resourceId=cf7bac8745e14594ba70171f8c92664e&resourceType=004&billingType=2&_t=1601430129134
    /cdn/gw/flowpacket/ChangeV3?workspaceId=10039265&resourceId=cf7bac8745e14594ba70171f8c92664e&resourceType=004&billingType=1&_t=1601430134833
    /cdn/gw/flowpacket/ChangeV3?workspaceId=10039265&resourceId=cf7bac8745e14594ba70171f8c92664e&resourceType=004&billingType=1&_t=1601430134833
    需要获取resourceId（在系统里面唯一） 和resourceType
    
    """

    @allure.story('/cdn/gw/flowpacket/ChangeV3 接口,修改一次')
    def test_CDN_246451(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ProductV3'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + '?' + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        resource_temp = json.loads(response.text)['data']['list']
        resource_list = []
        # print('resource_remp: ', resource_temp)
        for i in range(len(resource_temp)):
            resource = resource_temp[i]
            # print(type(resource), resource)
            if resource['billing_type'] == 1:
                bill = '2'
            else:
                bill = '1'
            re = '&resourceId=' + resource['resource_id'] + '&resourceType=' + resource[
                'product_code'] + '&billingType=' + bill
            resource_list.append(re)
        # print(resource_list)
        temp_ChangeV3 = self.console_host + '/cdn/gw/flowpacket/ChangeV3'
        data_ChangeV3 = '?workspaceId=' + self.workspace_id + random.choice(resource_list)
        payload = {}
        url_ChangeV3 = temp_ChangeV3 + data_ChangeV3
        response_ChangeV3 = self.session.request("GET", url_ChangeV3, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ChangeV3 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(data_ChangeV3))
        print("返回： " + response_ChangeV3.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response_ChangeV3.status_code == 200
        assert 'core.e' in response_ChangeV3.text
        assert '变更计费方式异常:无资源信息' in response_ChangeV3.text
        assert response_ChangeV3.elapsed.total_seconds() < 3

    @allure.story('/cdn/gw/flowpacket/ChangeV3 接口，修改多次')
    def test_CDN_246452(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ProductV3'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + '?' + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        resource_temp = json.loads(response.text)['data']['list']
        resource_list = []
        # print('resource_remp: ', resource_temp)
        for i in range(len(resource_temp)):
            resource = resource_temp[i]
            # print(type(resource), resource)
            if resource['billing_type'] == 1:
                bill = '2'
            else:
                bill = '1'
            re = '&resourceId=' + resource['resource_id'] + '&resourceType=' + resource[
                'product_code'] + '&billingType=' + bill
            resource_list.append(re)
        # print(resource_list)
        change1 = random.choice(resource_list)
        bill_type = str(random.choice(resource_list))[-1]
        if bill_type == '1':
            change2 = str(change1)[:-1] + '2'
        else:
            change2 = str(change1)[:-1] + '1'
        temp_ChangeV3 = self.console_host + '/cdn/gw/flowpacket/ChangeV3'
        data_ChangeV3 = '?workspaceId=' + self.workspace_id + change1
        payload = {}
        url_ChangeV3 = temp_ChangeV3 + data_ChangeV3
        response_ChangeV3 = self.session.request("GET", url_ChangeV3, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ChangeV3 接口-------------------")
        print('请求url: ' + url_ChangeV3)
        print("请求data: " + str(data_ChangeV3))
        print("返回： " + response_ChangeV3.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.e' in response_ChangeV3.text
        assert '变更计费方式异常' in response_ChangeV3.text
        assert response.elapsed.total_seconds() < 3

        data_ChangeV4 = '?workspaceId=' + self.workspace_id + change2
        payload = {}
        url_ChangeV4 = temp_ChangeV3 + data_ChangeV4
        response_ChangeV4 = self.session.request("GET", url_ChangeV4, data=payload, verify=False, timeout=10)
        print("-------------------查询 flowpacket/ChangeV3 接口-------------------")
        print('请求url: ' + url_ChangeV4)
        print("请求data: " + str(data_ChangeV4))
        print("返回： " + response_ChangeV4.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response_ChangeV4.status_code == 200
        assert 'core.e' in response_ChangeV4.text
        assert '变更计费方式异常' in response_ChangeV4.text
        assert response_ChangeV4.elapsed.total_seconds() < 3
