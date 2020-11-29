# -*- coding: utf-8 -*-

"""
CTYUN客户控制台，刷新预取相关接口

"""
import datetime
import json
import random
import time
from datetime import date, timedelta, datetime

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData
from bin.unit.Params import get_unix_time


@allure.feature('CTYUN 客户控制台刷新预取页接口测试')
class Test_Ctyun_Refresh():

    def setup_class(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        day_time = int(time.mktime(datetime.now().date().timetuple()))
        now_time = get_unix_time(now)

        # print('test start')
        self.session = Init.CTYUN_SESSION
        self.base_info = Init.BASE_INFO
        self.console_host = self.base_info['ctyunHost']
        self.workspace_id = self.base_info['ctyun_workspaceid']
        self.head_json = self.base_info['headers_json']
        self.today = day_time
        self.now = now_time
        self.head_form = self.base_info['headers_form']
        # 提取工作区对应的域名列表
        self.log = CreateLogData()
        self.get_domain_list = self.log.get_ctyun_used_domain_list(self.console_host, self.workspace_id)
        self.get_fan_domain = self.log.get_ctyun_all_domain(self.console_host, self.workspace_id)

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story('refresh/ListRefreshTask 接口1')
    def test_CDN_246208(self):
        temp = self.console_host + '/cdn/gw/refresh/ListRefreshTask'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&task_type=1&start_time=' + str(
            self.today) + '&end_time=' + str(self.now) + ''
        payload = {}
        url = temp + data
        response = self.session.request("POST", url, data=payload, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'create_time' in response.text
        # assert 'total' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('refresh/ListRefreshTask 接口2')
    def test_CDN_246209(self):
        temp = self.console_host + '/cdn/gw/refresh/ListRefreshTask'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&task_type=2&start_time=' + str(
            self.today) + '&end_time=' + str(self.now) + ''
        payload = {}
        url = temp + data
        response = self.session.request("POST", url, data=payload, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'create_time' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('preload/ListPreloadTaskk 接口')
    def test_CDN_246210(self):
        temp = self.console_host + '/cdn/gw/preload/ListPreloadTask'
        data = '?workspaceId=' + self.workspace_id + '&page=1&page_size=10&pageSize=10&start_time=' + str(
            self.today) + '&end_time=' + str(self.now) + ''
        payload = {}
        url = temp + data
        response = self.session.request("POST", url, data=payload, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'total' in response.text
        assert response.elapsed.total_seconds() < 3

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    # @pytest.mark.repeat(50)
    @allure.story('CreateRefreshTask 接口')
    def test_CDN_246204(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_domain_list)
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": [domain],
                     "domain": "", "task_type": "1"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        # assert 'core.ok' in response.text
        # assert 'secrets' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 接口2')
    def test_CDN_246205(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_domain_list)
        domain_https = random.choice(
            self.get_domain_list)
        value=[]
        value.append(domain_https)
        value.append(domain)
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": value,
                     "domain": "", "task_type": "1"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        # assert 'secrets' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 接口2')
    def test_CDN_246206(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        # 只能刷新已启用的域名
        used_domain_list = self.get_domain_list
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": used_domain_list,
                     "domain": "", "task_type": "1"}}
        # print(type(payload), payload)
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        # assert 'core.ok' in response.text
        # assert 'secrets' in response.text
        # assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 刷泛域名')
    def test_CDN_246219(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_fan_domain)
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": [domain],
                     "domain": "", "task_type": "1"}}
        print(type(payload), payload)
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        # assert 'core.ok' in response.text
        assert '请求参数错误' in response.text
        # assert 'value_error.url.scheme' in response.text

    @allure.story('CreateRefreshTask 刷泛域名目录')
    def test_CDN_246220(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_fan_domain) + "/images/"
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": [domain],
                     "domain": "", "task_type": "2"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert '请求参数错误' in response.text
        assert 'value_error' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 刷没有操作权限的URL')
    def test_CDN_246214(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": ["http://www.hehehe.com"],
                     "domain": "", "task_type": "1"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' not in response.text
        assert '填写内容有误，请核对添加的域名' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 刷目录')
    def test_CDN_246215(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_domain_list)
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": [domain + "/images/"],
                     "domain": "", "task_type": "2"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 刷多个目录')
    def test_CDN_246216(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        domain = random.choice(self.get_domain_list) + "/images/"
        domain_https = random.choice(self.get_domain_list) + "/gal.text/"
        value = []
        value.append(domain_https)
        value.append(domain)
        payload = {
            "data": {"workspaceId": self.workspace_id,
                     "values": value,
                     "domain": "", "task_type": "2"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask,刷新大量目录 ')
    def test_CDN_246217(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        # 只能刷新已启用的域名
        used_domain_list = self.get_domain_list
        directory_list = ['/images/', '/text/', '/pdf/']
        valuse_list = []
        for temp in used_domain_list:
            valuse_list.append(temp + directory_list[0])
            valuse_list.append(temp + directory_list[1])
            # valuse_list.append(temp + directory_list[2])
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": valuse_list,
                     "domain": "", "task_type": "2"}}
        print(type(payload), payload)
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        # assert '请求参数错误' in response.text
        # assert '100006' in response.text
        # 由于刷新的目录太多，所有肯定超过3秒，这条不验证
        # assert response.elapsed.total_seconds() < 3

    @allure.story('CreateRefreshTask 刷没有操作权限的目录')
    def test_CDN_246218(self):
        url = self.console_host + '/cdn/gw/refresh/CreateRefreshTask'
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": ["http://www.hehehe.com/text/"],
                     "domain": "", "task_type": "2"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' not in response.text
        assert '填写内容有误，请核对添加的域名' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story('domain/CheckPrivilege 刷不存在的URL')
    def test_CDN_246221(self):
        url = self.console_host + '/cdn/gw/domain/CheckPrivilege'
        payload = {
            "data": {"workspaceId": self.workspace_id, "values": ["http://www.baidu55555.com"], "do": "c_refresh"}}
        # url = temp + data
        response = self.session.request("POST", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 CreateRefreshTask 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert '"list":[{"enable":"false","on":"www.baidu55555.com"}]' in str(response.text)
        assert response.elapsed.total_seconds() < 3
