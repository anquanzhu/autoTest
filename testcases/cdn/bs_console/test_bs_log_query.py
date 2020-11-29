# -*- coding: utf-8 -*-

"""
BS 客户控制台，用量查询相关接口

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


@allure.feature('BS 客户控制台,统计分析-用量查询接口测试')
class Test_BS_Log_Query():

    def setup_class(self):
        # print('test start')
        self.session = Init.BS_SESSION
        self.base_info = Init.BASE_INFO
        self.log_info = Init.LOG_INFO
        self.console_host = self.base_info['bsHost']
        self.workspaceId = self.base_info['ctyunAcctId']
        self.log = CreateLogData()
        self.get_domain_list = self.log.get_bs_domain_list(self.workspaceId)

        # 接口
        self.flow_url = self.console_host + self.log_info['dataList']
        self.miss_dataList_url = self.console_host + self.log_info['missDataList']
        self.req_url = self.console_host + self.log_info['requestDataList']
        self.hit_url = self.console_host + self.log_info['hit']
        self.httpcode_url = self.console_host + self.log_info['httpcode']
        self.pvuv_url = self.console_host + self.log_info["pvuv"]

        # 日期类
        self.day_time = self.log.day_time
        self.yesterday_time = self.log.yesterday_time
        self.before_yesterday = self.log.before_yesterday
        self.sevenday_time = self.log.sevenday_time
        self.month_time = self.log.month_time
        self.now_time = self.log.now_time

        # 查询数据
        self.default_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                      "domain": self.get_domain_list, "startTime": self.day_time,
                                      "endTime": self.now_time}}

        self.cp_data_001 = {"data": {"workspaceId": self.workspaceId, "productType": ['001'], "isp": [], "province": [],
                                     "domain": self.log.get_bs_cp_domain(self.console_host, self.workspaceId,'001'),
                                     "startTime": self.day_time,"endTime": self.now_time}}

        self.cp_data_003 = {"data": {"workspaceId": self.workspaceId, "productType": ['003'], "isp": [], "province": [],
                                     "domain": self.log.get_bs_cp_domain(self.console_host, self.workspaceId,'003'),
                                     "startTime": self.day_time,"endTime": self.now_time}}

        self.cp_data_004 = {"data": {"workspaceId": self.workspaceId, "productType": ['004'], "isp": [], "province": [],
                                     "domain": self.log.get_bs_cp_domain(self.console_host, self.workspaceId,'004'),
                                     "startTime": self.day_time,"endTime": self.now_time}}

        self.cp_data_005 = {"data": {"workspaceId": self.workspaceId, "productType": ['005'], "isp": [], "province": [],
                                     "domain": self.log.get_bs_cp_domain(self.console_host, self.workspaceId,'005'),
                                     "startTime": self.day_time,"endTime": self.now_time}}

        self.isp_data_1 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [1], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_2 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [2], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_3 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [3], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_4 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [4], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_5 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [5], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_6 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [6], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.day_time,
                                    "endTime": self.now_time}}
        self.isp_data_100 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [100], "province": [],
                                      "domain": self.get_domain_list, "startTime": self.day_time,
                                      "endTime": self.now_time}}
        isp_list = [1, 2, 3, 4, 5, 6, 100]
        self.isp_data_random = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [random.choice(isp_list)],
                     "province": [],
                     "domain": self.get_domain_list, "startTime": self.day_time,
                     "endTime": self.now_time}}

        self.province_data_1 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [],
                                         "province": [random.choice(province)],
                                         "domain": self.get_domain_list, "startTime": self.day_time,
                                         "endTime": self.now_time}}

        self.province_data_2 = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [],
                                         "province": [random.choice(province)],
                                         "domain": self.get_domain_list, "startTime": self.yesterday_time,
                                         "endTime": self.now_time}}
        self.date_yesterday = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.yesterday_time,
                     "endTime": self.now_time}}

        self.date_compare = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.before_yesterday,
                     "endTime": self.yesterday_time}}

        self.date_sevenday = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.sevenday_time,
                     "endTime": self.now_time}}
        self.date_month = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                    "domain": self.get_domain_list, "startTime": self.month_time,
                                    "endTime": self.now_time}}
        self.default_pvuv = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": self.get_domain_list, "startTime": self.day_time, "endTime": self.now_time,
                     "ignore": "domain"}}

        self.random_domain_pvuv = {
            "data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                     "domain": [random.choice(self.get_domain_list)], "startTime": self.day_time,
                     "endTime": self.now_time, "ignore": "domain"}}

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story(' dataList 接口1')
    def test_CDN_243672(self):
        url = self.flow_url
        payload = self.default_data
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243673(self):
        url = self.miss_dataList_url
        payload = self.default_data
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243674(self):
        url = self.req_url
        payload = self.default_data
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243675(self):
        url = self.hit_url
        payload = self.default_data
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243676(self):
        url = self.httpcode_url
        payload = self.default_data
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243677(self):
        url = self.flow_url
        payload = self.date_yesterday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243678(self):
        url = self.miss_dataList_url
        payload = self.date_yesterday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243679(self):
        url = self.req_url
        payload = self.date_yesterday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243680(self):
        url = self.hit_url
        payload = self.date_yesterday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243681(self):
        url = self.httpcode_url
        payload = self.date_yesterday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243682(self):
        url = self.flow_url
        payload = self.date_sevenday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243683(self):
        url = self.miss_dataList_url
        payload = self.date_sevenday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243684(self):
        url = self.req_url
        payload = self.date_sevenday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243685(self):
        url = self.hit_url
        payload = self.date_sevenday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243686(self):
        url = self.httpcode_url
        payload = self.date_sevenday
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243687(self):
        url = self.flow_url
        payload = self.cp_data_001
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243688(self):
        url = self.miss_dataList_url
        payload = self.cp_data_001
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243689(self):
        url = self.req_url
        payload = self.cp_data_001
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243690(self):
        url = self.hit_url
        payload = self.cp_data_001
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243691(self):
        url = self.httpcode_url
        payload = self.cp_data_001
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243692(self):
        url = self.flow_url
        payload = self.cp_data_003
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243693(self):
        url = self.miss_dataList_url
        payload = self.cp_data_003
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243694(self):
        url = self.req_url
        payload = self.cp_data_003
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243695(self):
        url = self.hit_url
        payload = self.cp_data_003
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243696(self):
        url = self.httpcode_url
        payload = self.cp_data_003
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243697(self):
        url = self.flow_url
        payload = self.cp_data_004
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243698(self):
        url = self.miss_dataList_url
        payload = self.cp_data_004
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243699(self):
        url = self.req_url
        payload = self.cp_data_004
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243700(self):
        url = self.hit_url
        payload = self.cp_data_004
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243701(self):
        url = self.httpcode_url
        payload = self.cp_data_004
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243702(self):
        url = self.flow_url
        payload = self.cp_data_005
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243703(self):
        url = self.miss_dataList_url
        payload = self.cp_data_005
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243704(self):
        url = self.req_url
        payload = self.cp_data_005
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243705(self):
        url = self.hit_url
        payload = self.cp_data_005
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243706(self):
        url = self.httpcode_url
        payload = self.cp_data_005
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243707(self):
        url = self.flow_url
        payload = self.isp_data_random
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243708(self):
        url = self.miss_dataList_url
        payload = self.isp_data_random
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243709(self):
        url = self.req_url
        payload = self.isp_data_random
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243710(self):
        url = self.hit_url
        payload = self.isp_data_random
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243711(self):
        url = self.httpcode_url
        payload = self.isp_data_random
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_2437112(self):
        url = self.flow_url
        payload = self.province_data_1
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243713(self):
        url = self.miss_dataList_url
        payload = self.province_data_2
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243714(self):
        url = self.req_url
        payload = self.province_data_1
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243715(self):
        url = self.hit_url
        payload = self.province_data_2
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243716(self):
        url = self.httpcode_url
        payload = self.province_data_1
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1,默认数据对比')
    def test_CDN_243717(self):
        url = self.flow_url
        payload = self.date_compare
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 默认数据对比')
    def test_CDN_243718(self):
        url = self.miss_dataList_url
        payload = self.date_compare
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' dataList 接口1')
    def test_CDN_243719(self):
        url = self.flow_url
        payload = self.date_month
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 dataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' missDataList 接口1')
    def test_CDN_243720(self):
        url = self.miss_dataList_url
        payload = self.date_month
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 missDataList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' req_url 接口1')
    def test_CDN_243721(self):
        url = self.req_url
        payload = self.date_month
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 req_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' hit_url 接口1')
    def test_CDN_243722(self):
        url = self.hit_url
        payload = self.date_month
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 hit_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(' httpcode_url 接口1')
    def test_CDN_243723(self):
        url = self.httpcode_url
        payload = self.date_month
        # url = temp + data
        response = self.session.request("GET", url, data=json.dumps(payload), verify=False, timeout=10)
        print("-------------------查询 httpcode_url 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story(" GetPvUv 接口1 默认数据查询")
    def test_CDN_265365(self):
        url = self.pvuv_url
        payload = self.default_pvuv
        response = self.session.post(url, json=payload, verify=False, timeout=10)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text

    @allure.story(" GetPvUv 接口1 单域名查询")
    def test_CDN_265366(self):
        url = self.pvuv_url
        payload = self.random_domain_pvuv
        response = self.session.post(url, json=payload, verify=False, timeout=10)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text

    @allure.story(" GetPvUv 接口1 查询昨天的PV/UV")
    def test_CDN_265367(self):
        url = self.pvuv_url
        self.date_yesterday["data"]["ignore"] = "domain"
        payload = self.date_yesterday
        response = self.session.post(url, json=payload, verify=False, timeout=10)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text

    @allure.story(" GetPvUv 接口1 查询近7天的PV/UV")
    def test_CDN_265368(self):
        url = self.pvuv_url
        self.date_sevenday["data"]["ignore"] = "domain"
        payload = self.date_sevenday
        response = self.session.post(url, json=payload, verify=False, timeout=10)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text

    @allure.story(" GetPvUv 接口1 查询近30天的PV/UV")
    def test_CDN_265369(self):
        url = self.pvuv_url
        self.date_month["data"]["ignore"] = "domain"
        payload = self.date_month
        response = self.session.post(url, json=payload, verify=False, timeout=10)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text

    @pytest.mark.skipif(Init.ENV == "ITE", reason="测试环境可能无数据，暂不执行")
    @allure.story(" 小时粒度，PV峰值/总量正确 ")
    def test_CDN_270979(self):
        payload = self.default_pvuv
        response = self.session.post(self.pvuv_url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        hours = content["data"]["hours"]
        pvCount = [hour["pvCount"] for hour in hours]
        totalPv = 0
        for i in range(0, len(pvCount)):
            # pv总量
            totalPv += pvCount[i]
        # pv峰值
        maxPv = max(pvCount)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + self.pvuv_url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert totalPv == content["data"]["totalPv"]
        assert maxPv == content["data"]["maxPv"]

    @pytest.mark.skipif(Init.ENV == "ITE", reason="测试环境可能无数据，暂不执行")
    @allure.story(" 小时粒度，UV峰值/总量正确 ")
    def test_CDN_270980(self):
        payload = self.default_pvuv
        response = self.session.post(self.pvuv_url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        hours = content["data"]["hours"]
        uvCount = [hour["uvCount"] for hour in hours]
        totalUv = 0
        for i in range(0, len(uvCount)):
            # pv总量
            totalUv += uvCount[i]
        # pv峰值
        maxUv = max(uvCount)
        print(totalUv, maxUv)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + self.pvuv_url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert totalUv == content["data"]["totalUv"]
        assert maxUv == content["data"]["maxUv"]

    @pytest.mark.skipif(Init.ENV == "ITE", reason="测试环境可能无数据，暂不执行")
    @allure.story(" 天粒度，PV峰值/总量正确 ")
    def test_CDN_270981(self):
        self.date_sevenday["data"]["ignore"] = "domain"
        payload = self.date_sevenday
        response = self.session.post(self.pvuv_url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        hours = content["data"]["daily"]
        pvCount = [hour["pvCount"] for hour in hours]
        totalPv = 0
        for i in range(0, len(pvCount)):
            # Pv总量
            totalPv += pvCount[i]
        # Pv峰值
        maxPv = max(pvCount)
        print(totalPv, maxPv)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + self.pvuv_url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert totalPv == content["data"]["totalPv"]
        assert maxPv == content["data"]["maxPv"]

    @pytest.mark.skipif(Init.ENV == "ITE", reason="测试环境可能无数据，暂不执行")
    @allure.story(" 天粒度，UV峰值/总量正确 ")
    def test_CDN_270982(self):
        self.date_sevenday["data"]["ignore"] = "domain"
        payload = self.date_sevenday
        response = self.session.post(self.pvuv_url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        hours = content["data"]["daily"]
        uvCount = [hour["uvCount"] for hour in hours]
        totalUv = 0
        for i in range(0, len(uvCount)):
            # Uv总量
            totalUv += uvCount[i]
        # Uv峰值
        maxUv = max(uvCount)
        print(totalUv, maxUv)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + self.pvuv_url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert totalUv == content["data"]["totalUv"]
        assert maxUv == content["data"]["maxUv"]

    @pytest.mark.skipif(Init.ENV == "ITE", reason="测试环境可能无数据，暂不执行")
    @allure.story(" 天粒度，近30天的PV总量大于UV总量 ")
    def test_CDN_271054(self):
        # Pv：业务访问量， Uv：独立客户访问量
        self.date_month["data"]["ignore"] = "domain"
        payload = self.date_month
        response = self.session.post(self.pvuv_url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        totalPv = content["data"]["totalPv"]
        totalUv = content["data"]["totalUv"]
        print(totalPv, totalUv)
        print("-------------------查询 GetPvUv 接口-------------------")
        print('请求url: ' + self.pvuv_url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： Pv总量大于Uv总量")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert totalPv > totalUv

