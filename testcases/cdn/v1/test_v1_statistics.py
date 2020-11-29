# -*- coding: utf-8 -*-

import allure
import pytest
from bin.createLogData import CreateLogData
from bin.Sha256Ext import post_json_head
from bin.Init import Init
import random
import time
import datetime


# 配置
productCode = ['001', '003', '004', '005']
isp = [1, 2, 3, 4, 5, 6, 100]
province = ["110000", "120000", "130000", "140000", "150000", "210000", "220000", "230000", "310000", "320000",
            "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "440000", "450000",
            "460000", "500000", "510000", "520000", "530000", "540000", "610000", "620000", "630000", "640000",
            "650000"]

now = int(time.time())
today = datetime.date.today()
morning = int(time.mktime(time.strptime(today.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')))
sevenmorning = int(time.mktime(time.strptime((today + datetime.timedelta(days=-6)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')))
monthmorning = int(time.mktime(time.strptime((today - datetime.timedelta(days=today.day-1)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')))

starttime = [monthmorning]


@allure.feature("客户控制台v1接口统计分析接口测试")
class TestStatistics(object):

    def setup_class(self):
        print('test start')
        self.v1_info = Init.V1_INFO
        self.base_info = Init.V1_BASE_INFO
        self.host = self.base_info["host"]
        self.ctyunacctid = self.base_info["ctyunAcctId"]
        self.domain = self.base_info["domain"]
        self.log = CreateLogData()
        self.seven = self.log.sevenday_time
        self.month = self.log.month_time
        self.today = self.log.month_time
        self.now = self.log.now_time

    def teardown_class(self):
        # 做清数据，退出登录等
        print('test end')

    @pytest.mark.skip("服务未通")  # 跳过该测试
    @allure.testcase(" query/querybandwidthandTraffic ")
    def test_CDN_241493(self):
        # 统计流量带宽
        url = self.v1_info["querybandwidthandTraffic"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,4),
                "province": random.sample(province,10),
                "productType": random.sample(productCode,3),
                "startTime":random.choice(starttime),
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3

    @pytest.mark.skip("服务未通")  # 跳过该测试
    @allure.testcase(" statistics/RequestDataList ")
    def test_CDN_241489(self):
        # 统计请求数
        url = self.v1_info["requestdataList"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,4),
                "province": random.sample(province,10),
                "productType": random.sample(productCode,3),
                "startTime":random.choice(starttime),
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3

    @pytest.mark.skip("服务未通")  # 跳过该测试
    @allure.testcase(" statistics/HitDate ")
    def test_CDN_241491(self):
        # 统计命中数
        url = self.v1_info["hitDate"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,4),
                "province": random.sample(province,10),
                "productType": random.sample(productCode,3),
                "startTime":random.choice(starttime),
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3

    @pytest.mark.skip("服务未通")
    @allure.testcase(" statistics/HttpCodeSummary ")
    def test_CDN_241492(self):
        # Http状态码汇总
        url = self.v1_info["httpCodeSummary"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,4),
                "province": random.sample(province,10),
                "productType": random.sample(productCode,3),
                "startTime":random.choice(starttime),
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3

    @allure.testcase(" statistics/MissData ")
    def test_CDN_241490(self):
        # 回源数据
        url = self.v1_info["missData"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,4),
                "province": random.sample(province,10),
                "productType": random.sample(productCode,3),
                "startTime":morning,
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3

    @pytest.mark.skip("服务未通")  # 跳过该测试
    @allure.testcase(" statistics/HttpCode ")
    def test_CDN_241494(self):
        # 状态码
        url = self.v1_info["httpCode"]
        data = {
            "data":{
                "ctyunAcctId": self.ctyunacctid,
                "domain": self.domain,
                "isp": random.sample(isp,2),
                "province": random.sample(province,2),
                "productType": random.sample(productCode,2),
                "startTime":random.choice(starttime),
                "endTime":now
            }
        }
        response = post_json_head(self.host,url,data)
        print("请求url：" + url + ";")
        print("请求data：" + str(data) + ";")
        print("返回：" + str(response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in response.text
        assert self.domain[0] in response. text
        # assert response.elapsed.total_seconds() < 3
