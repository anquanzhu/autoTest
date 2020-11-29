# -*- coding: utf-8 -*-

"""
BS 客户控制台，计费详情相关接口

"""
import json
import random

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData


@allure.feature('BS 客户控制台 计费详情页接口测试')
class Test_BS_Billing():

    def setup_class(self):
        # print('test start')
        self.session = Init.BS_SESSION
        self.base_info = Init.BASE_INFO
        self.console_host = self.base_info['bsHost']
        self.workspace_id = self.base_info['ctyunAcctId']
        self.head_json = self.base_info['headers_json']
        self.today = CreateLogData().day_time
        self.now = CreateLogData().now_time
        self.head_form = self.base_info['headers_form']

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story('flowpacket/ListV3 查all')
    def test_CDN_243724(self):
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
    def test_CDN_243725(self):
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
    def test_CDN_243726(self):
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
    def test_CDN_243727(self):
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
    def test_CDN_243728(self):
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
    def test_CDN_243729(self):
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
        assert 'accountId' in response.text
        assert 'resourceId' in response.text
        assert 'salesEntryId' in response.text
        assert 'effDate' in response.text
        assert 'workorderId' in response.text
        assert 'billingTypeId' in response.text
        assert 'operatorTime' in response.text
        assert 'createTime' in response.text
        assert 'state' in response.text
        assert 'expDate' in response.text
        assert 'operator' in response.text
        assert 'resourceType' in response.text
        assert response.elapsed.total_seconds() < 3
