# -*-coding: utf-8 -*-
import json

import pytest
import allure
import time

from bin.Init import Init
from bin.createOrder import createOrderData
from bin.createDomain import CreateDomain
import random

"""
CTYUN客户控制台，工单列表相关接口

"""


@allure.feature("CTYUN客户控制台,工单列表接口测试")
class Test_Ctyun_Order(object):

    def setup_class(self):
        print("----------test start--------")
        self.session = Init.CTYUN_SESSION
        self.base_info = Init.BASE_INFO
        self.domain_info = Init.DOMAIN_INFO
        self.console_host = self.base_info['ctyunHost']
        self.workspaceId = self.base_info['ctyun_workspaceid']
        self.domainData = CreateDomain(self.workspaceId)
        self.orderData = createOrderData(self.session, self.console_host, self.workspaceId)
        self.domain_list = self.orderData.order_domainlist()
        self.order_list = self.orderData.list_orderid(self.domain_list)
        self.fail_doamin_list = self.orderData.domain_status_4(self.domain_list)

    def teardown_class(self):
        self.session.close()
        print("---------test end-----------")

    @allure.story("权限域名列表接口 GetList")
    def test_CDN_260757(self):
        url = self.domain_info["listDomainV2"]
        payload = self.orderData.order_domainlist_data()
        response = self.session.get(self.console_host + url, params=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        print(response.text)
        print("-------------------查询 GetList 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  "  域名列表数量大于或等于0")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert len(content["data"]["list"]) >= 0
        assert response.elapsed.total_seconds() < 3

    @allure.story("工单列表接口 ListOrder")
    def test_CDN_260759(self):
        url = self.domain_info["listOrder"]
        payload = self.orderData.order_default_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 返回码与响应时间")
        if len(content["data"]["list"]) > 0:
            first_order = content["data"]["list"][0]
            assert first_order["createTime"]
            assert first_order["domain"]
            assert first_order["orderId"]
            assert first_order["orderNo"]
            assert first_order["orderType"]
            assert first_order["recordStatus"]
            assert first_order["status"]
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("通过域名查询工单")
    def test_CDN_260761(self):
        url = self.domain_info["listOrder"]
        payload = self.orderData.order_domain_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 返回值中有域名")
        # 由于有部分旧域名数据在工单列表中无工单，故针对这种情况校验
        content = json.loads(response.text)
        if content["data"]["list"]:
            assert payload["data"]["domainList"][0] in response.text
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("工单状态查询工单")
    def test_CDN_260762(self):
        url = self.domain_info["listOrder"]
        payload = self.orderData.order_status_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 返回值中有工单状态")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert payload["data"]["status"][0] in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("工单类型查询工单")
    def test_CDN_260763(self):
        url = self.domain_info["listOrder"]
        payload = self.orderData.order_type_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 返回值中有工单类型")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert payload["data"]["orderType"][0] in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("工单时间查询工单")
    def test_CDN_260764(self):
        url = self.domain_info["listOrder"]
        payload = self.orderData.order_time_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 状态码和响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("查看工单详情")
    def test_CDN_260760(self):
        url = self.domain_info["orderDetail"]
        payload = {
            "workspaceId": self.workspaceId,
            "orderId": random.choice(self.order_list)
        }
        response = self.session.get(self.console_host + url, params=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------查看 OrderDetail 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 返回值中有工单id")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert payload["orderId"] in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("域名校验接口 Check")
    def test_CDN_260758(self):
        url = self.domain_info["checkDomain"]
        payload = {
            "workspaceId": self.workspaceId,
            "domain": random.choice(self.fail_doamin_list)
        }
        response = self.session.get(self.console_host + url, params=payload, verify=False, timeout=10)
        print(response.text)
        print("-------------------检测 Check 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 状态码和响应时间")
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("域名关联工单，在途域名在工单列表内")
    def test_CDN_261183(self):
        url = self.domain_info["listOrder"]
        order_list = self.orderData.domain_orderlist()
        # 域名列表有在途工单的情况，随机拿一个工单
        if order_list:
            order_list_num = len(order_list)
            random_order = order_list[random.randint(0, order_list_num-1)]
            domain = random_order.get("domain")
            orderId = random_order.get("orderId")
            # 1:停用，2:启用，3:删除，4:新增，5:更新
            order_type = random_order.get("action")
            print("domain为：{}, orderId为：{}，order_type为：{}".format(domain, orderId,order_type))
        else:
            domain = ""
            orderId = ""
            order_type = ""
        # 工单列表
        payload = self.orderData.order_default_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        orderList = content["data"]["list"]
        order = [order for order in orderList if order["domain"] == domain and order["orderId"] == orderId and
                 order["orderType"] == order_type]
        print(order)
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 域名工单在工单列表中")
        if order_list:
                assert order
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("域名与工单关联，已启用状态域名-查找新增工单")
    def test_CDN_261181(self):
        url = self.domain_info["listOrder"]
        domain_list = self.orderData.domain_manage_list(4)
        # 域名列表有其用域名的情况，随机拿一个域名
        if domain_list:
            domain_list_num = len(domain_list)
            domain = domain_list[random.randint(0, domain_list_num-1)]
            domain_name = domain["domain"]
            domain_date = domain["insertDate"]
            print("domain为：{}".format(domain_name))
        else:
            domain_name = ""
            domain_date = ""

        # 工单列表
        payload = self.orderData.order_default_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        # 工单列表中该域名的新增工单
        try:
            order = [order for order in content["data"]["list"] if order["domain"] == domain_name and
                     order["orderType"] == "4" and int(order["createTime"]) < int(domain_date)]
            print(order)
        except Exception as e:
            order = []
            print("域名列表下无已启用域名，报错信息：{}".format(e))
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 启用域名在工单列表中有新增工单")
        if domain_list:
                assert order
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("域名与工单关联，已停用状态域名-查找停用工单")
    def test_CDN_261182(self):
        url = self.domain_info["listOrder"]
        domain_list = self.orderData.domain_manage_list(6)
        # 域名列表有启用域名的情况，随机拿一个域名
        if domain_list:
            domain_list_num = len(domain_list)
            domain = domain_list[random.randint(0, domain_list_num-1)]
            domain_name = domain["domain"]
            print("domain为：{}".format(domain_name))
        else:
            domain_name = ""

        # 工单列表
        payload = self.orderData.order_default_data(self.domain_list)
        response = self.session.post(self.console_host + url, json=payload, verify=False, timeout=10)
        content = json.loads(response.text)
        # 工单列表中该域名的新增工单
        try:
            order = [order for order in content["data"]["list"] if order["domain"] == domain_name and
                     order["orderType"] == "1"]
            print(order)
        except Exception as e:
            order = []
            print("域名列表下无已停用域名，报错信息：{}".format(e))
        print(response.text)
        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + url)
        print("请求data: " + str(payload))
        print("返回： " + response.text)
        print("重点验证："  " expect： 已停用域名在工单列表中有停用工单")
        if domain_list:
                assert order
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3

    @allure.story("域名与工单关联，新增域名，查找新增工单")
    def test_CDN_261184(self):
        domain_url = self.domain_info["createDomain"]
        payload = self.domainData.generate_randomDomain()
        response = self.session.post(self.console_host + domain_url, json=payload, verify=False, timeout=10)
        print(response.text)
        # 工单等待时间
        time.sleep(1)

        # 工单列表
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.console_host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        all_orders = content["data"]["list"]
        # 工单列表中找新增域名，类型为新增，状态为进行中的该工单

        order = [order for order in all_orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        print(order)

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert response.status_code == 200
        assert 'core.ok' in response.text
        assert response.elapsed.total_seconds() < 3


