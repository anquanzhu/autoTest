# -*- coding: utf-8 -*-

"""
CTYUN客户控制台，用户分析相关接口

"""
import json
import random

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData

productCode = ['001', '003', '004', '005']
isp = [1, 2, 3, 4, 5, 6, 100]
province = ["110000", "120000", "130000", "140000", "150000", "210000", "220000", "230000", "310000", "320000",
            "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "440000", "450000",
            "460000", "500000", "510000", "520000", "530000", "540000", "610000", "620000", "630000", "640000",
            "650000"]


@allure.feature('CTYUN 客户控制台 用户用量查询接口测试')
class Test_Ctyun_Log_dataList():

    def setup_class(self):
        # print('test start')
        self.session = Init.CTYUN_SESSION
        self.base_info = Init.BASE_INFO
        self.log_info = Init.LOG_INFO
        self.console_host = self.base_info['ctyunHost']
        self.workspaceId = self.base_info['ctyun_workspaceid']
        self.log = CreateLogData()
        self.get_domain_list = self.log.get_ctyun_domain_list(self.console_host, self.workspaceId)

        # 接口
        self.fbrData_url = self.console_host + self.log_info['fbrData']
        self.ispList_url = self.console_host + self.log_info['ispList']

        # 日期类
        self.day_time = self.log.day_time
        self.yesterday_time = self.log.yesterday_time
        self.sevenday_time = self.log.sevenday_time
        self.month_time = self.log.month_time
        self.now_time = self.log.now_time

        # 查询数据
        self.default_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                      "domain": self.get_domain_list, "startTime": self.day_time,
                                      "endTime": self.now_time}}
        self.cp_data_001 = {"data": {"workspaceId": self.workspaceId, "productType": ['001'], "isp": [], "province": [],
                                     "domain": self.log.get_ctyun_cp_domain(self.console_host, self.workspaceId, '001'),
                                     "startTime": self.day_time,
                                     "endTime": self.now_time}}

        self.cp_data_003 = {"data": {"workspaceId": self.workspaceId, "productType": ['003'], "isp": [], "province": [],
                                     "domain": self.log.get_ctyun_cp_domain(self.console_host, self.workspaceId, '003'), "startTime": self.day_time,
                                     "endTime": self.now_time}}
        self.cp_data_004 = {"data": {"workspaceId": self.workspaceId, "productType": ['004'], "isp": [], "province": [],
                                     "domain": self.log.get_ctyun_cp_domain(self.console_host, self.workspaceId, '004'), "startTime": self.day_time,
                                     "endTime": self.now_time}}
        self.cp_data_005 = {"data": {"workspaceId": self.workspaceId, "productType": ['005'], "isp": [], "province": [],
                                     "domain": self.log.get_ctyun_cp_domain(self.console_host, self.workspaceId, '005'), "startTime": self.day_time,
                                     "endTime": self.now_time}}
        self.single_domain = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                       "domain": [random.choice(self.get_domain_list)], "startTime": self.day_time,
                                       "endTime": self.now_time}}
        self.date_data_yesterday = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.yesterday_time,
                     "endTime": self.now_time}}

        self.date_data_sevenday = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.sevenday_time,
                     "endTime": self.now_time}}
        self.date_data_month = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                         "domain": self.get_domain_list, "startTime": self.month_time,
                                         "endTime": self.now_time}}

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story(' 单个域名查询用户省份分析数据')
    def test_CDN_246235(self):
        url = self.fbrData_url
        payload = self.single_domain
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 单个域名查询用户运营商分析数据')
    def test_CDN_246236(self):
        url = self.ispList_url
        payload = self.single_domain
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 视频直播产品查询 用户省份分析数据')
    def test_CDN_246233(self):
        url = self.fbrData_url
        payload = self.cp_data_004
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 视频直播产品查询 用户运营商分析数据')
    def test_CDN_246234(self):
        url = self.ispList_url
        payload = self.cp_data_004
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 视频点播产品查询 用户省份分析数据')
    def test_CDN_246231(self):
        url = self.fbrData_url
        payload = self.cp_data_005
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 视频点播产品查询 用户运营商分析数据')
    def test_CDN_246232(self):
        url = self.ispList_url
        payload = self.cp_data_005
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 下载加速产品查询 用户省份分析数据')
    def test_CDN_246229(self):
        url = self.fbrData_url
        payload = self.cp_data_003
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 下载加速产品查询 用户运营商分析数据')
    def test_CDN_246230(self):
        url = self.ispList_url
        payload = self.cp_data_003
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 静态加速产品查询 用户省份分析数据')
    def test_CDN_246227(self):
        url = self.fbrData_url
        payload = self.cp_data_001
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 静态加速产品查询 用户运营商分析数据')
    def test_CDN_246228(self):
        url = self.ispList_url
        payload = self.cp_data_001
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 默认查询 用户省份分析数据')
    def test_CDN_246225(self):
        url = self.fbrData_url
        payload = self.default_data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' 默认查询 用户运营商分析数据')
    def test_CDN_246226(self):
        url = self.ispList_url
        payload = self.default_data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3
