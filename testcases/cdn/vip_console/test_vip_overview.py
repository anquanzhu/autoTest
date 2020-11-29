# -*- coding: utf-8 -*-

"""
VIP客户控制台，概览页相关接口

"""
import json

import allure
import pytest
from bin.Init import Init
from bin.Yaml import readYaml


@allure.feature('VIP客户控制台概览页接口测试')
class Test_Vip_Overview():

    def setup_class(self):
        print('test start')
        self.session = Init.CONSOLE_SESSION
        self.base_info = Init.BASE_INFO
        self.console_host = self.base_info['host']
        self.workspace_id = self.base_info['workspaceid']
        self.head_json = self.base_info['headers_json']
        self.head_form = self.base_info['headers_form']
        self.ENV = Init.ENV
        self.domain_info = Init.DOMAIN_INFO

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('test end')

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    # @pytest.mark.repeat(50)
    @allure.story('productV3接口,注意，这里依赖业务平台，切表之后会没数据')
    def test_CDN_240848(self):
        temp = self.console_host + '/cdn/gw/flowpacket/ProductV3'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + '?' + data
        response = self.session.request("GET", url, data=payload, timeout=10)
        print("-------------------查询ProductV3接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3
        # 线上的返回没有 product_cname
        # if self.ENV == 'ITE':
        assert '静态加速' in response.text
        assert '下载加速' in response.text
        assert '视频点播加速' in response.text
        assert '视频直播加速' in response.text
        # elif self.ENV == 'PE':
        assert 'product_type' in response.text
        assert 'account_id' in response.text
        assert 'billing_type' in response.text
        assert 'resource_id' in response.text
        assert 'product_code' in response.text
        assert 'product_cname' in response.text
        assert 'status' in response.text

    @allure.story('domain/GetList接口1')
    def test_CDN_240849(self):
        temp = self.console_host + '/cdn/gw/domain/GetList?do=c_domain&'
        data = 'workspaceId=' + self.workspace_id
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
        assert 'productCode' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('domain/GetList接口2,返回与1一样')
    def test_CDN_240850(self):
        temp = self.console_host + '/cdn/gw/domain/GetList?do=c_data&'
        data = 'workspaceId=' + self.workspace_id
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
        assert 'productCode' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu接口，CDN控制台域名相关按钮')
    def test_CDN_240851(self):
        temp = self.console_host + '/cdn/ctyun/menu?domain=cdn.domain&'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询menu接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'cdn.domain' in response.text
        assert 'CDN控制台域名相关按钮' in response.text
        assert '添加域名' in response.text
        assert '域名管理' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('message/ListMessage接口1')
    def test_CDN_240852(self):
        temp = self.console_host + '/cdn/gw/message/ListMessage?type=1&'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 message/ListMessage 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'cdn.domain' in response.text
        # assert 'CDN控制台域名相关按钮' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('cert/CertList接口')
    def test_CDN_240853(self):
        temp = self.console_host + '/cdn/gw/cert/CertList'
        data = ''
        payload = {"data": {"workspaceId": self.workspace_id, "limit": 9999}}
        url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), timeout=10)
        print("-------------------查询 cert/CertList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'secrets' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('message/ListMessage接口2')
    def test_CDN_240854(self):
        temp = self.console_host + '/cdn/gw/message/ListMessage?type=4&'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 message/ListMessage 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    """
    CDN控制台依赖IAM的一些接口
    /iam/gw/workspace/menu/GetTree?domain=workspace.header&locale=zh-cn&workspaceId=10003885
    /iam/gw/workspace/menu/GetTree?domain=workspace.header.dropdown&locale=zh-cn&workspaceId=10003885
    /iam/gw/workspace/menu/GetTree?workspaceId=10003885&domain=cdn.main
    /iam/gw/workspace/menu/GetTree?workspaceId=10003885&domain=cdn.domain
    /iam/gw/workspace/menu/GetTree?domain=cdn.header.dropdown&locale=zh-cn&workspaceId=10003885
    /iam/gw/workspace/menu/GetTree?domain=cdn.header&locale=zh-cn&workspaceId=10003885
    """

    @allure.story('menu/GetTree接口1: 工作区主页头像下拉菜单')
    def test_CDN_244506(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=workspace.header&locale=zh-cn'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert '工作区主页头部菜单' in response.text
        # assert '基本信息' in response.text
        # assert '修改密码' in response.text
        # assert '修改资料' in response.text
        # assert '其他工作区' in response.text
        # assert '注销' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu/GetTree接口1： 工作区主页头部下拉菜单2')
    def test_CDN_244507(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=workspace.header.dropdown&locale=zh-cn'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert '工作区主页头部下拉菜单' in response.text
        assert '基本信息' in response.text
        assert '修改密码' in response.text
        assert '修改资料' in response.text
        assert '其他工作区' in response.text
        assert '注销' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu/GetTree接口1： CDN控制台主菜单')
    def test_CDN_244508(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=cdn.main'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'CDN控制台主菜单' in response.text
        assert '概览' in response.text
        assert 'CDN控制台概览' in response.text
        assert '域名管理' in response.text
        assert '证书管理' in response.text
        assert '统计分析' in response.text
        assert '刷新预取' in response.text
        assert '日志下载' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu/GetTree接口1： CDN控制台域名相关按钮')
    def test_CDN_244509(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=cdn.domain'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'CDN控制台域名相关按钮' in response.text
        assert '添加域名' in response.text
        assert '域名管理' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu/GetTree接口1： CDN控制台头部下拉菜单3')
    def test_CDN_244510(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=cdn.header.dropdown&locale=zh-cn'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'CDN控制台头部下拉菜单' in response.text
        assert '基本信息' in response.text
        assert '修改密码' in response.text
        assert '修改资料' in response.text
        assert '其他工作区' in response.text
        assert '注销' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('menu/GetTree接口1： CDN控制台头部菜单4')
    def test_CDN_244511(self):
        temp = self.console_host + '/iam/gw/workspace/menu/GetTree?'
        data = 'workspaceId=' + self.workspace_id + '&domain=cdn.header&locale=zh-cn'
        payload = {}
        url = temp + data
        response = self.session.request("GET", url, data=payload, verify=False, timeout=10)
        print("-------------------查询 menu/GetTree 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + data)
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert 'CDN控制台头部菜单' in response.text
        assert '概览' in response.text
        assert '个人中心' in response.text
        assert '工作区' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('域名列表接口的关联与核对')
    def test_CDN_259935(self):
        """
        1. 校对c_data ,c_domain下的域名数量 （domain代表用户可访问的域名数量，data代表用户进行统计分析操作的域名数量）
        2. 校对域名管理页面的域名数量等同于1里面统计的域名数量
        :return:
        """
        temp_data = self.console_host + '/cdn/gw/domain/GetList?do=c_data&'
        temp_domain = self.console_host + '/cdn/gw/domain/GetList?do=c_domain&'
        temp_domianManage = self.console_host + self.domain_info['listDomain']
        list_data = '?workspaceId=' + self.workspace_id + '&page=1&pageSize=1000'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url_data = temp_data + data
        url_domain = temp_domain + data
        url_domianManage = temp_domianManage + list_data
        response_data = self.session.request("GET", url_data, data=payload, verify=False, timeout=10)
        response_domain = self.session.request("GET", url_data, data=payload, verify=False, timeout=10)
        list_response = self.session.request("GET", url_domianManage, data=payload, verify=False, timeout=10)
        sum1 = len(json.loads(response_data.text)['data']['list'])
        sum2 = len(json.loads(response_domain.text)['data']['list'])
        sum3 = len(json.loads(list_response.text)['data']['list'])
        print("-------------------查询 域名列表1 接口-------------------")
        print('请求url1: ' + url_data)
        print('请求url2: ' + url_domain)
        print("请求data: " + data)
        print("返回： " + response_data.text)
        print("返回： " + response_domain.text)
        print("域名数量： ", sum1, sum2, sum3)
        print("重点验证："  "  expect： 返回码与响应时间")
        print("-------------------查询 域名列表2  接口-------------------")
        print('请求url: ' + temp_domianManage)
        print("请求data: " + list_data)
        print("返回： " + list_response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response_data.status_code == 200
        assert 'core.ok' in response_data.text
        assert response_data.elapsed.total_seconds() < 3
        assert response_domain.status_code == 200
        assert 'core.ok' in response_domain.text
        assert response_domain.elapsed.total_seconds() < 3
        assert sum1 == sum2
        assert sum1 == sum3


    product_url='/cdn/gw/flowpacket/ProductV3?workspaceId=10003885&_t=1604642614567'