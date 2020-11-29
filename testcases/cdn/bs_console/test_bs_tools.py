# -*- coding: utf-8 -*-

"""
BS 客户控制台，诊断工具相关接口

"""
import json
import random

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData


@allure.feature('BS 客户控制台诊断工具页接口测试')
class Test_Bs_Tools():

    def setup_class(self):
        # print('test start')
        self.session = Init.BS_SESSION
        self.base_info = Init.BASE_INFO
        self.console_host = self.base_info['bsHost']
        self.workspace_id = self.base_info['ctyunAcctId']

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story('diagnose/IpCheck 接口1')
    def test_CDN_243730(self):
        temp = self.console_host + '/cdn/gw/diagnose/IpCheck?ipv4=192.168.1.1'
        data = '&workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询domain/GetList接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert '"isCDNip":"false"' in response.text
        assert '"ipAddress":"未知"' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('diagnose/IpCheck 接口2')
    def test_CDN_243731(self):
        temp = self.console_host + '/cdn/gw/diagnose/IpCheck?ipv4=222.222.169.89'
        data = '&workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询domain/GetList接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert '"isCDNip":"true"' in response.text
        assert '"ipAddress":"保定市"' in response.text
        assert response.elapsed.total_seconds() < 3
