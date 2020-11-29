# -*- coding: utf-8 -*-

# VIP客户控制台，热门分析相关接口

import json
import random

import allure
import pytest
from bin.Init import Init
from bin.createLogData import CreateLogData

productCode = ['001', '003', '004', '005']
httpCode = ["2XX","3XX","4XX","5XX"]
sort_list = ["flow","request"]
province = ["110000", "120000", "130000", "140000", "150000", "210000", "220000", "230000", "310000", "320000",
            "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "440000", "450000",
            "460000", "500000", "510000", "520000", "530000", "540000", "610000", "620000", "630000", "640000",
            "650000"]


@allure.feature("VIP客户控制台,统计分析-热门分析接口测试")
class Test_Vip_Top(object):

    def setup_class(self):
        # print('test start')
        self.session = Init.CONSOLE_SESSION
        self.base_info = Init.BASE_INFO
        self.log_info = Init.LOG_INFO
        self.console_host = self.base_info['host']
        self.workspaceId = self.base_info['workspaceid']
        self.log = CreateLogData()
        self.get_domain_list = self.log.get_available_domain_list()

        # 接口
        self.uri_url = self.console_host + self.log_info['ListTopUri']
        self.referer_url = self.console_host + self.log_info['ListTopReferer']
        self.domain_url = self.console_host + self.log_info['ListTopDomain']
        self.ip_url = self.console_host + self.log_info['ListTopIp']

        # 日期类
        self.day_time = self.log.day_time
        self.yesterday_time = self.log.yesterday_time
        self.before_yesterday = self.log.before_yesterday
        self.sevenday_time = self.log.sevenday_time
        self.month_time = self.log.month_time
        self.now_time = self.log.now_time

        # 查询数据
        self.default_uri_hit_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"HIT","sortedBy":"flow"}}

        self.default_uri_miss_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"MISS","sortedBy":"flow"}}

        self.default_referer_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "productCode":[],"sortedBy":"flow"}}

        self.default_domain_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,
                    "productCode":[],"sortedBy":"flow"}}

        self.default_ip_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[],"sortedBy":"flow"}}

        self.uri_hit_data_001 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('001'),"top":100,
                    "httpCode":[],"productCode":["001"],"status":"HIT","sortedBy":"flow"}}

        self.uri_miss_data_001 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('001'),"top":100,
                    "httpCode":[],"productCode":["001"],"status":"MISS","sortedBy":"flow"}}

        self.referer_data_001 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('001'),"top":100,
                    "productCode":["001"],"sortedBy":"flow"}}

        self.domain_data_001 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('001'),
                    "productCode":["001"],"sortedBy":"flow"}}

        self.ip_data_001 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('001'),"top":100,
                    "provinceCode":["001"],"sortedBy":"flow"}}

        self.uri_hit_data_003 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('003'),"top":100,
                    "httpCode":[],"productCode":["003"],"status":"HIT","sortedBy":"flow"}}

        self.uri_miss_data_003 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('003'),"top":100,
                    "httpCode":[],"productCode":["003"],"status":"MISS","sortedBy":"flow"}}

        self.referer_data_003 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('003'),"top":100,
                    "productCode":["003"],"sortedBy":"flow"}}

        self.domain_data_003 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('003'),
                    "productCode":["003"],"sortedBy":"flow"}}

        self.ip_data_003 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('003'),"top":100,
                    "provinceCode":["003"],"sortedBy":"flow"}}

        self.uri_hit_data_004 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('004'),"top":100,
                    "httpCode":[],"productCode":["004"],"status":"HIT","sortedBy":"flow"}}

        self.uri_miss_data_004 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('004'),"top":100,
                    "httpCode":[],"productCode":["004"],"status":"MISS","sortedBy":"flow"}}

        self.referer_data_004 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('004'),"top":100,
                    "productCode":["004"],"sortedBy":"flow"}}

        self.domain_data_004 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('004'),
                    "productCode":["004"],"sortedBy":"flow"}}

        self.ip_data_004 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('004'),"top":100,
                    "provinceCode":["004"],"sortedBy":"flow"}}

        self.uri_hit_data_005 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('005'),"top":100,
                    "httpCode":[],"productCode":["005"],"status":"HIT","sortedBy":"flow"}}

        self.uri_miss_data_005 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('005'),"top":100,
                    "httpCode":[],"productCode":["005"],"status":"MISS","sortedBy":"flow"}}

        self.referer_data_005 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('005'),"top":100,
                    "productCode":["005"],"sortedBy":"flow"}}

        self.domain_data_005 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('005'),
                    "productCode":["005"],"sortedBy":"flow"}}

        self.ip_data_005 = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.log.get_cp_domain('005'),"top":100,
                    "provinceCode":["005"],"sortedBy":"flow"}}

        self.uri_hit_httpcode_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[random.choice(httpCode)],"productCode":[],"status":"HIT","sortedBy":"flow"}}

        self.uri_miss_httpcode_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[random.choice(httpCode)],"productCode":[],"status":"MISS","sortedBy":"flow"}}

        self.uri_hit_request_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"HIT","sortedBy":"request"}}

        self.uri_miss_request_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"MISS","sortedBy":"request"}}

        self.referer_request_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "productCode":[],"sortedBy":"request"}}

        self.domain_request_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,
                    "productCode":[],"sortedBy":"request"}}

        self.ip_request_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[],"sortedBy":"request"}}

        self.ip_province_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.yesterday_time,
                    "endTime":self.day_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[random.choice(province)],"sortedBy":"request"}}

        self.today_uri_hit_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.day_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"HIT","sortedBy":"flow"}}

        self.today_uri_miss_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.day_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "httpCode":[],"productCode":[],"status":"MISS","sortedBy":"flow"}}

        self.today_referer_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.day_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "productCode":[],"sortedBy":"flow"}}

        self.today_domain_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.day_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,
                    "productCode":[],"sortedBy":"flow"}}

        self.today_ip_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.day_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[],"sortedBy":"flow"}}

        self.seven_domain_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.sevenday_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,
                    "productCode":[],"sortedBy":"flow"}}

        self.senven_ip_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.sevenday_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[],"sortedBy":"flow"}}

        self.month_domain_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.month_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,
                    "productCode":[],"sortedBy":"flow"}}

        self.month_ip_data = {
            "data":{"workspaceId":self.workspaceId,"startTime":self.month_time,
                    "endTime":self.now_time,"domain":self.get_domain_list,"top":100,
                    "provinceCode":[],"sortedBy":"flow"}}

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('-------------------test end-------------------')

    @allure.story("默认查询热门URL")
    def test_CDN_248713(self):
        url = self.uri_url
        payload = self.default_uri_hit_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("默认查询热门URL(回源)")
    def test_CDN_248714(self):
        url = self.uri_url
        payload = self.default_uri_miss_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("默认查询热门Referer")
    def test_CDN_248715(self):
        url = self.referer_url
        payload = self.default_referer_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("默认查询域名排行")
    def test_CDN_248716(self):
        url = self.domain_url
        payload = self.default_domain_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("默认查询TOP客户端IP")
    def test_CDN_248717(self):
        url = self.ip_url
        payload = self.default_ip_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("静态加速产品下查询热门URL")
    def test_CDN_248718(self):
        url = self.uri_url
        payload = self.uri_hit_data_001
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("静态加速产品下查询热门URL(回源)")
    def test_CDN_249250(self):
        url = self.uri_url
        payload = self.uri_miss_data_001
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("静态加速产品下查询热门Referer")
    def test_CDN_249251(self):
        url = self.referer_url
        payload = self.referer_data_001
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("静态加速产品下查询域名排行")
    def test_CDN_249252(self):
        url = self.domain_url
        payload = self.domain_data_001
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("静态加速产品下查询TOP客户端IP")
    def test_CDN_249253(self):
        url = self.ip_url
        payload = self.ip_data_001
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("下载加速产品下查询热门URL")
    def test_CDN_249254(self):
        url = self.uri_url
        payload = self.uri_hit_data_003
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("下载加速产品下查询热门URL(回源)")
    def test_CDN_249255(self):
        url = self.uri_url
        payload = self.uri_miss_data_003
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("下载加速产品下查询热门Referer")
    def test_CDN_249256(self):
        url = self.referer_url
        payload = self.referer_data_003
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("下载加速产品下查询域名排行")
    def test_CDN_249257(self):
        url = self.domain_url
        payload = self.domain_data_003
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("下载加速产品下查询TOP客户端IP")
    def test_CDN_249258(self):
        url = self.ip_url
        payload = self.ip_data_003
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频点播加速产品下查询热门URL")
    def test_CDN_249259(self):
        url = self.uri_url
        payload = self.uri_hit_data_004
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频点播加速产品下查询热门URL(回源)")
    def test_CDN_249260(self):
        url = self.uri_url
        payload = self.uri_miss_data_004
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频点播加速产品下查询Referer")
    def test_CDN_249261(self):
        url = self.referer_url
        payload = self.referer_data_004
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频点播加速产品下查询域名排行")
    def test_CDN_249262(self):
        url = self.domain_url
        payload = self.domain_data_004
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频点播加速产品下查询TOP客户端IP")
    def test_CDN_249263(self):
        url = self.ip_url
        payload = self.ip_data_004
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询热门URL")
    def test_CDN_249264(self):
        url = self.uri_url
        payload = self.uri_hit_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询热门URL")
    def test_CDN_249264(self):
        url = self.uri_url
        payload = self.uri_hit_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询热门URL(回源)")
    def test_CDN_249265(self):
        url = self.uri_url
        payload = self.uri_miss_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询Referer")
    def test_CDN_249266(self):
        url = self.referer_url
        payload = self.referer_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询域名排行")
    def test_CDN_249267(self):
        url = self.domain_url
        payload = self.domain_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("视频直播加速产品下查询TOP客户端IP")
    def test_CDN_249268(self):
        url = self.ip_url
        payload = self.ip_data_005
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("状态码查询热门URL")
    def test_CDN_249269(self):
        url = self.uri_url
        payload = self.uri_hit_httpcode_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("状态码查询热门URL(回源)")
    def test_CDN_249270(self):
        url = self.uri_url
        payload = self.uri_miss_httpcode_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("访问次数维度查询热门URL")
    def test_CDN_249272(self):
        url = self.uri_url
        payload = self.uri_hit_request_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("访问次数维度查询热门URL(回源)")
    def test_CDN_249274(self):
        url = self.uri_url
        payload = self.uri_miss_request_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("访问次数维度查询热门Referer")
    def test_CDN_249276(self):
        url = self.referer_url
        payload = self.referer_request_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("访问次数维度查询域名排行")
    def test_CDN_249278(self):
        url = self.domain_url
        payload = self.domain_request_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("访问次数维度查询TOP客户端IP")
    def test_CDN_249280(self):
        url = self.ip_url
        payload = self.ip_request_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("通过地区查询TOP客户端IP")
    def test_CDN_249281(self):
        url = self.ip_url
        payload = self.ip_province_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询今天的热门URL")
    def test_CDN_249282(self):
        url = self.uri_url
        payload = self.today_uri_hit_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询今天的热门URL(回源)")
    def test_CDN_249283(self):
        url = self.uri_url
        payload = self.today_uri_miss_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topuri 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询今天的热门Referer")
    def test_CDN_249284(self):
        url = self.referer_url
        payload = self.today_referer_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topreferer 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询今天的域名排行")
    def test_CDN_249285(self):
        url = self.domain_url
        payload = self.today_domain_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询今天的TOP客户端IP")
    def test_CDN_249286(self):
        url = self.ip_url
        payload = self.today_ip_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询7天的域名排行")
    def test_CDN_249287(self):
        url = self.domain_url
        payload = self.seven_domain_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查询7天的TOP客户端IP")
    def test_CDN_249288(self):
        url = self.ip_url
        payload = self.senven_ip_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    # @pytest.mark.skip("响应超时") # 跳过该测试
    @allure.story("查询30天的域名排行")
    def test_CDN_249289(self):
        url = self.domain_url
        payload = self.month_domain_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topdomain 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 10

    # @pytest.mark.skip("响应超时") # 跳过该测试
    @allure.story("查询30天的TOP客户端IP")
    def test_CDN_249290(self):
        url = self.ip_url
        payload = self.month_ip_data
        response = self.session.post(url, json=payload, timeout=10)
        print("-------------------查询 topip 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  expect： 返回码与响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 10

