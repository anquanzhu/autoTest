# -*- coding: utf-8 -*-
import json
import random

import allure
import pytest
import time

from bin.GetSuite import read
from bin.Yaml import readYaml, choose_v1yaml
from bin.createDomain import CreateDomain
from bin.unit.Rondom import random_string
from bin.Sha256Ext import post_json_head, post_form_head
from bin.createV1Domain import Create_v1_Domain
from bin.Init import Init
from bin.createOrder import createOrderData
from bin.Workorder import deal_new_domain, workorder_fail_domain, workOrder_Flow_Domain

productcode = ["001", "003", "004", "005"]

# 静态加速、动态加速、下载加速、视频点播加速、视频直播加速
# 全站加速、"006" 暂不执行
params_data = [["001", "服务调用成功"], ["002", "尚未开通此产品，不能创建对应类型的域名"], ["003", "服务调用成功"],
               ["004", "服务调用成功"], ["005", "服务调用成功"]]


@allure.feature("客户控制台v1接口域名接口测试")
class TestDomain(object):

    def setup_class(self):
        print('test start')
        self.v1_info = Init.V1_INFO
        self.base_v1_info = Init.V1_BASE_INFO
        self.host = self.base_v1_info["host"]
        self.ctyunacctid = self.base_v1_info["ctyunAcctId"]
        # self.autoctyunid = self.base_v1_info["autoCtyun"]
        self.createV1Domain = Create_v1_Domain()
        self.session = Init.CONSOLE_SESSION
        self.base_info = Init.BASE_INFO
        # self.auto_session = Init.Auto_SESSION
        # self.autoworkspaceId = self.base_info["AutoWorkspaceId"]
        self.domain_info = Init.DOMAIN_INFO
        self.workspaceId = self.base_info['workspaceid']
        self.orderData = createOrderData(self.session, self.host, self.workspaceId)
        self.domain_list = self.orderData.order_domainlist()
        self.order_list = self.orderData.list_orderid(self.domain_list)
        self.fail_doamin_list = self.orderData.domain_status_4(self.domain_list)
        # 自助配置账号-工单数据
        # self.Auto_orderData = createOrderData(self.auto_session, self.host, self.autoworkspaceId)
        # self.auto_domain_list = self.Auto_orderData.order_domainlist()
        # self.auto_order_list = self.Auto_orderData.list_orderid(self.domain_list)

    def teardown_class(self):
        # 做清数据，退出登录等
        print('test end')

    @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("域名新增-配置失败-重新发起-配置成功-域名启用")
    def test_CDN_262372(self):
        # 新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3
        # 工单等待时间
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        orders = content["data"]["list"]

        order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        if order:
            print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
        else:
            print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert order_list_response.status_code == 200
        assert 'core.ok' in order_list_response.text
        assert order_list_response.elapsed.total_seconds() < 3

        # 工单系统配置失败
        workorder_fail_domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为失败，类型为新增
        order_list_response_2 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_2.text)
        content_2 = json.loads(order_list_response_2.text)
        orders_2 = content_2["data"]["list"]
        order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "4"]
        if order_2:
            print("已找到域名为{}的失败工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
        else:
            print("未找到域名为{}的失败工单".format(payload["data"]["domain"]))
        assert order_2

        # 页面重新发起，校验域名
        url = self.domain_info["checkDomain"]
        check_domain_payload = {
            "workspaceId": self.workspaceId,
            "domain": payload["data"]["domain"]
        }
        check_domain_response = self.session.get(self.host + url, params=check_domain_payload, verify=False, timeout=10)
        print(check_domain_response.text)
        assert "服务调用成功" in check_domain_response.text
        assert "\"data\":{}" in check_domain_response.text

        # 重新发起新增域名
        domain_payload_2 = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response_2 = post_json_head(self.host, create_domain_url, domain_payload_2)
        print(create_domain_response_2.text)
        time.sleep(1)
        assert domain_payload_2["data"]["domain"] in create_domain_response_2.text

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        self.domain_list.append(domain_payload_2["data"]["domain"])
        order_payload_2 = self.orderData.order_default_data(self.domain_list)
        order_list_response_3 = self.session.post(self.host + orderlist_url, json=order_payload_2, verify=False,
                                                  timeout=10)
        print(order_list_response_3.text)
        content_3 = json.loads(order_list_response_3.text)
        orders_3 = content_3["data"]["list"]
        order_3 = [order for order in orders_3 if order["domain"] == domain_payload_2["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "2"]
        if order_3:
            print("已找到第二次发起的域名为{}的新增工单，工单为：{}".format(domain_payload_2["data"]["domain"], str(order_3)))
        else:
            print("未找到第二次发起的域名为{}的新增工单".format(domain_payload_2["data"]["domain"]))
        assert order_3

        # 工单系统配置成功
        deal_new_domain(domain_payload_2["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
        order_list_response_4 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_4.text)
        content_4 = json.loads(order_list_response_4.text)
        orders_4 = content_4["data"]["list"]
        order_4 = [order for order in orders_4 if order["domain"] == domain_payload_2["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "3"]
        if order_4:
            print("已找到第二次发起的域名为{}的新增成功工单，工单为：{}".format(domain_payload_2["data"]["domain"],
                                                        str(order_4)))
        else:
            print("未找到第二次发起的域名为{}的新增成功工单".format(domain_payload_2["data"]["domain"]))
        assert order_4

        # 调用域名列表接口，查找新增成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert domain_payload_2["data"]["domain"] in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

    @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("域名新增-配置成功-域名启用-编辑-配置成功-域名启用")
    def test_CDN_262373(self):
        # 新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3
        # 工单等待时间
        time.sleep(2)

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        print(self.domain_list)
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        orders = content["data"]["list"]

        order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        if order:
            print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
        else:
            print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert order_list_response.status_code == 200
        assert 'core.ok' in order_list_response.text
        assert order_list_response.elapsed.total_seconds() < 3

        # 工单系统配置成功
        deal_new_domain(payload["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
        order_list_response_2 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_2.text)
        content_2 = json.loads(order_list_response_2.text)
        orders_2 = content_2["data"]["list"]
        order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "3"]
        if order_2:
            print("已找到域名为{}的新增成功工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
        else:
            print("未找到域名为{}的新增成功工单".format(payload["data"]["domain"]))
        assert order_2

        # 调用域名列表接口，查找新增成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert payload["data"]["domain"] in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

        # 编辑域名
        edit_domain_payload = self.createV1Domain.edit_domain(self.ctyunacctid, payload["data"]["domain"],
                                                              payload["data"]["productCode"])
        edit_domain_response = post_json_head(self.host, create_domain_url, edit_domain_payload)
        print(edit_domain_response.text)
        print("-------------------验证编辑域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(edit_domain_payload) + ";")
        print("返回： " + str(edit_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in edit_domain_response.text
        assert payload["data"]["domain"] in edit_domain_response.text
        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找更新的域名工单，状态为进行中，类型为更新
        order_list_response_3 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_3.text)
        content_3 = json.loads(order_list_response_3.text)
        orders_3 = content_3["data"]["list"]
        order_3 = [order for order in orders_3 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "5" and order["status"] == "2"]
        if order_3:
            print("已找到域名为{}的更新工单，工单为：{}".format(payload["data"]["domain"], str(order_3)))
        else:
            print("未找到域名为{}的更新工单".format(payload["data"]["domain"]))
        assert order_3

        # 工单系统配置成功
        deal_new_domain(payload["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找更新的域名工单，状态为成功，类型为更新
        order_list_response_4 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_4.text)
        content_4 = json.loads(order_list_response_4.text)
        orders_4 = content_4["data"]["list"]
        order_4 = [order for order in orders_4 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "5" and order["status"] == "3"]
        if order_4:
            print("已找到域名为{}的更新成功工单，工单为：{}".format(payload["data"]["domain"], str(order_4)))
        else:
            print("未找到域名为{}的更新成功工单".format(payload["data"]["domain"]))
        assert order_4
        time.sleep(1)

        # 域名列表该域名无在途工单
        order_list = self.orderData.domain_orderlist()
        assert payload["data"]["domain"] not in str(order_list)

    @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("域名新增-配置成功-域名启用-编辑-配置失败-域名启用")
    def test_CDN_262374(self):
        # 新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3
        # 工单等待时间
        time.sleep(2)

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        print(self.domain_list)
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        orders = content["data"]["list"]

        order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        if order:
            print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
        else:
            print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert order_list_response.status_code == 200
        assert 'core.ok' in order_list_response.text
        assert order_list_response.elapsed.total_seconds() < 3

        # 工单系统配置成功
        deal_new_domain(payload["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
        order_list_response_2 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_2.text)
        content_2 = json.loads(order_list_response_2.text)
        orders_2 = content_2["data"]["list"]
        order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "3"]
        if order_2:
            print("已找到域名为{}的新增成功工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
        else:
            print("未找到域名为{}的新增成功工单".format(payload["data"]["domain"]))
        assert order_2

        # 调用域名列表接口，查找新增成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert payload["data"]["domain"] in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

        # 编辑域名
        edit_domain_payload = self.createV1Domain.edit_domain(self.ctyunacctid, payload["data"]["domain"],
                                                              payload["data"]["productCode"])
        edit_domain_response = post_json_head(self.host, create_domain_url, edit_domain_payload)
        print(edit_domain_response.text)
        print("-------------------验证编辑域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(edit_domain_payload) + ";")
        print("返回： " + str(edit_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in edit_domain_response.text
        assert payload["data"]["domain"] in edit_domain_response.text
        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找更新的域名工单，状态为进行中，类型为更新
        order_list_response_3 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_3.text)
        content_3 = json.loads(order_list_response_3.text)
        orders_3 = content_3["data"]["list"]
        order_3 = [order for order in orders_3 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "5" and order["status"] == "2"]
        if order_3:
            print("已找到域名为{}的更新工单，工单为：{}".format(payload["data"]["domain"], str(order_3)))
        else:
            print("未找到域名为{}的更新工单".format(payload["data"]["domain"]))
        assert order_3

        # 工单系统配置失败
        workorder_fail_domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用工单列表接口，查找更新的域名工单，状态为失败，类型为更新
        order_list_response_4 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_4.text)
        content_4 = json.loads(order_list_response_4.text)
        orders_4 = content_4["data"]["list"]
        order_4 = [order for order in orders_4 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "5" and order["status"] == "4"]
        if order_4:
            print("已找到域名为{}的更新失败工单，工单为：{}".format(payload["data"]["domain"], str(order_4)))
        else:
            print("未找到域名为{}的更新失败工单".format(payload["data"]["domain"]))
        assert order_4
        time.sleep(1)

        # 域名列表该域名无在途工单
        order_list = self.orderData.domain_orderlist()
        assert payload["data"]["domain"] not in str(order_list)

    @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("域名新增-配置成功-域名启用-停用-删除")
    def test_CDN_262375(self):
        # 新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3
        # 工单等待时间
        time.sleep(2)

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        print(self.domain_list)
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        orders = content["data"]["list"]

        order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        if order:
            print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
        else:
            print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert order_list_response.status_code == 200
        assert 'core.ok' in order_list_response.text
        assert order_list_response.elapsed.total_seconds() < 3

        # 工单系统配置成功
        deal_new_domain(payload["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
        order_list_response_2 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_2.text)
        content_2 = json.loads(order_list_response_2.text)
        orders_2 = content_2["data"]["list"]
        order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "3"]
        if order_2:
            print("已找到域名为{}的新增成功工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
        else:
            print("未找到域名为{}的新增成功工单".format(payload["data"]["domain"]))
        assert order_2

        # 调用域名列表接口，查找新增成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert payload["data"]["domain"] in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

        # 停用域名
        stop_domain_url = self.v1_info["changeDomain"]
        stop_domain_payload = self.createV1Domain.stop_domain(self.ctyunacctid, payload["data"]["domain"],
                                                              payload["data"]["productCode"])
        stop_domain_response = post_form_head(self.host, stop_domain_url, stop_domain_payload)
        print(stop_domain_response.text)
        print("-------------------验证停用域名是否成功-------------------")
        print('请求url: ' + str(stop_domain_url) + ";")
        print("请求data: " + str(stop_domain_payload) + ";")
        print("返回： " + str(stop_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" in stop_domain_response.text
        assert "处理成功" in stop_domain_response.text

        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找停用的域名工单，状态为进行中，类型为停用
        order_list_response_3 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_3.text)
        content_3 = json.loads(order_list_response_3.text)
        orders_3 = content_3["data"]["list"]
        order_3 = [order for order in orders_3 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "1" and order["status"] == "2"]
        if order_3:
            print("已找到域名为{}的停用工单，工单为：{}".format(payload["data"]["domain"], str(order_3)))
        else:
            print("未找到域名为{}的停用工单".format(payload["data"]["domain"]))
        assert order_3

        # 工单系统停用域名成功
        workOrder_Flow_Domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用工单列表接口，查找停用的域名工单，状态为成功，类型为停用
        order_list_response_4 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_4.text)
        content_4 = json.loads(order_list_response_4.text)
        orders_4 = content_4["data"]["list"]
        order_4 = [order for order in orders_4 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "1" and order["status"] == "3"]
        if order_4:
            print("已找到域名为{}的停用成功工单，工单为：{}".format(payload["data"]["domain"], str(order_4)))
        else:
            print("未找到域名为{}的停用成功工单".format(payload["data"]["domain"]))
        assert order_4
        time.sleep(1)

        # 域名列表该域名无在途工单
        order_list = self.orderData.domain_orderlist()
        assert payload["data"]["domain"] not in str(order_list)

        # 删除域名
        delete_domain_url = self.v1_info["changeDomain"]
        delete_domain_payload = self.createV1Domain.delete_domain(self.ctyunacctid, payload["data"]["domain"],
                                                                  payload["data"]["productCode"])
        delete_domain_response = post_form_head(self.host, delete_domain_url, delete_domain_payload)
        print(delete_domain_response.text)
        print("-------------------验证删除域名是否成功-------------------")
        print('请求url: ' + str(delete_domain_url) + ";")
        print("请求data: " + str(delete_domain_payload) + ";")
        print("返回： " + str(delete_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" in delete_domain_response.text
        assert "处理成功" in delete_domain_response.text

        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找删除的域名工单，状态为进行中，类型为删除
        order_list_response_5 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_5.text)
        content_5 = json.loads(order_list_response_5.text)
        orders_5 = content_5["data"]["list"]
        order_5 = [order for order in orders_5 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "3" and order["status"] == "2"]
        if order_5:
            print("已找到域名为{}的删除工单，工单为：{}".format(payload["data"]["domain"], str(order_5)))
        else:
            print("未找到域名为{}的删除工单".format(payload["data"]["domain"]))
        assert order_5

        # 工单系统删除域名成功
        workOrder_Flow_Domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用域名列表接口，查找删除成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert payload["data"]["domain"] not in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

    @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("域名新增-配置成功-域名启用-停用-启用")
    def test_CDN_262376(self):
        # 新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, random.choice(productcode))
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3
        # 工单等待时间
        time.sleep(2)

        # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
        orderlist_url = self.domain_info["listOrder"]
        self.domain_list.append(payload["data"]["domain"])
        print(self.domain_list)
        order_payload = self.orderData.order_default_data(self.domain_list)
        order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                timeout=10)
        print(order_list_response.text)
        content = json.loads(order_list_response.text)
        orders = content["data"]["list"]

        order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                 order["orderType"] == "4" and order["status"] == "2"]
        if order:
            print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
        else:
            print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))

        print("-------------------查询 ListOrder 接口-------------------")
        print('请求url: ' + orderlist_url)
        print("请求data: " + str(order_payload))
        print("返回： " + order_list_response.text)
        print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
        assert order
        assert order_list_response.status_code == 200
        assert 'core.ok' in order_list_response.text
        assert order_list_response.elapsed.total_seconds() < 3

        # 工单系统配置成功
        deal_new_domain(payload["data"]["domain"], "3")
        time.sleep(1)

        # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
        order_list_response_2 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_2.text)
        content_2 = json.loads(order_list_response_2.text)
        orders_2 = content_2["data"]["list"]
        order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "4" and order["status"] == "3"]
        if order_2:
            print("已找到域名为{}的新增成功工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
        else:
            print("未找到域名为{}的新增成功工单".format(payload["data"]["domain"]))
        assert order_2

        # 调用域名列表接口，查找新增成功的域名
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        domain_list_response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        assert payload["data"]["domain"] in domain_list_response.text
        assert "服务调用成功" in domain_list_response.text

        # 停用域名
        stop_domain_url = self.v1_info["changeDomain"]
        stop_domain_payload = self.createV1Domain.stop_domain(self.ctyunacctid, payload["data"]["domain"],
                                                              payload["data"]["productCode"])
        stop_domain_response = post_form_head(self.host, stop_domain_url, stop_domain_payload)
        print(stop_domain_response.text)
        print("-------------------验证停用域名是否成功-------------------")
        print('请求url: ' + str(stop_domain_url) + ";")
        print("请求data: " + str(stop_domain_payload) + ";")
        print("返回： " + str(stop_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" in stop_domain_response.text
        assert "处理成功" in stop_domain_response.text

        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找停用的域名工单，状态为进行中，类型为停用
        order_list_response_3 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_3.text)
        content_3 = json.loads(order_list_response_3.text)
        orders_3 = content_3["data"]["list"]
        order_3 = [order for order in orders_3 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "1" and order["status"] == "2"]
        if order_3:
            print("已找到域名为{}的停用工单，工单为：{}".format(payload["data"]["domain"], str(order_3)))
        else:
            print("未找到域名为{}的停用工单".format(payload["data"]["domain"]))
        assert order_3

        # 工单系统停用域名成功
        workOrder_Flow_Domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用工单列表接口，查找停用的域名工单，状态为成功，类型为停用
        order_list_response_4 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_4.text)
        content_4 = json.loads(order_list_response_4.text)
        orders_4 = content_4["data"]["list"]
        order_4 = [order for order in orders_4 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "1" and order["status"] == "3"]
        if order_4:
            print("已找到域名为{}的停用成功工单，工单为：{}".format(payload["data"]["domain"], str(order_4)))
        else:
            print("未找到域名为{}的停用成功工单".format(payload["data"]["domain"]))
        assert order_4
        time.sleep(1)

        # 域名列表该域名无在途工单
        order_list = self.orderData.domain_orderlist()
        assert payload["data"]["domain"] not in str(order_list)

        # 启用域名
        start_domain_url = self.v1_info["changeDomain"]
        start_domain_payload = self.createV1Domain.start_domain(self.ctyunacctid, payload["data"]["domain"],
                                                                payload["data"]["productCode"])
        start_domain_response = post_form_head(self.host, start_domain_url, start_domain_payload)
        print(start_domain_response.text)
        print("-------------------验证启用域名是否成功-------------------")
        print('请求url: ' + str(start_domain_url) + ";")
        print("请求data: " + str(start_domain_payload) + ";")
        print("返回： " + str(start_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" in start_domain_response.text
        assert "处理成功" in start_domain_response.text

        time.sleep(1)

        # 域名列表该域名有在途工单
        order_list = self.orderData.domain_orderlist()
        # assert payload["data"]["domain"] in str(order_list)
        print(order_list)

        # 调用工单列表接口，查找启用的域名工单，状态为进行中，类型为启用
        order_list_response_5 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_5.text)
        content_5 = json.loads(order_list_response_5.text)
        orders_5 = content_5["data"]["list"]
        order_5 = [order for order in orders_5 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "2" and order["status"] == "2"]
        if order_5:
            print("已找到域名为{}的启用工单，工单为：{}".format(payload["data"]["domain"], str(order_5)))
        else:
            print("未找到域名为{}的启用工单".format(payload["data"]["domain"]))
        assert order_5

        # 工单系统启用域名成功
        workOrder_Flow_Domain(payload["data"]["domain"])
        time.sleep(1)

        # 调用工单列表接口，查找启用的域名工单，状态为成功，类型为启用
        order_list_response_6 = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                  timeout=10)
        print(order_list_response_6.text)
        content_6 = json.loads(order_list_response_6.text)
        orders_6 = content_6["data"]["list"]
        order_6 = [order for order in orders_6 if order["domain"] == payload["data"]["domain"] and
                   order["orderType"] == "2" and order["status"] == "3"]
        if order_6:
            print("已找到域名为{}的启用成功工单，工单为：{}".format(payload["data"]["domain"], str(order_6)))
        else:
            print("未找到域名为{}的启用成功工单".format(payload["data"]["domain"]))
        assert order_6

    # @pytest.mark.skip("2020/11/12，停用状态域名调用接口进行编辑，返回失败")
    # @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    @allure.story("已停用状态域名，不能编辑域名")
    def test_CDN_264311(self):
        # 根据域名状态，做域名操作限制
        # 域名列表
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)
        print("-------------------验证域名列表是否成功-------------------")
        print('请求url: ' + str(list_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(list_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in list_domain_response.text
        assert list_domain_response.elapsed.total_seconds() < 3

        content = json.loads(list_domain_response.text)
        domains = content["data"]["list"]
        stop_domains = [domain for domain in domains if domain["status"] == 6]

        # 随机拿一个已停止状态的域名
        domain = random.choice(stop_domains)
        print("已停止状态的域名：{}，产品类型为：{}".format(domain["domain"], domain["productCode"]))

        # 编辑域名
        create_domain_url = self.v1_info["createDomain"]
        edit_domain_payload = self.createV1Domain.edit_domain(self.ctyunacctid, domain["domain"],
                                                              domain["productCode"])
        edit_domain_response = post_json_head(self.host, create_domain_url, edit_domain_payload)
        print(edit_domain_response.text)
        print("-------------------验证编辑域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(edit_domain_payload) + ";")
        print("返回： " + str(edit_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用失败")
        assert "服务调用成功" not in edit_domain_response.text
        assert domain["domain"] in edit_domain_response.text

    # @pytest.mark.skip("2020/11/12，启用状态域名调用接口进行删除，返回失败")
    @allure.story("已启用状态域名，不能删除域名")
    def test_CDN_264310(self):
        # 根据域名状态，做域名操作限制
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)
        print("-------------------验证域名列表是否成功-------------------")
        print('请求url: ' + str(list_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(list_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in list_domain_response.text
        assert list_domain_response.elapsed.total_seconds() < 3

        content = json.loads(list_domain_response.text)
        domains = content["data"]["list"]
        start_domains = [domain for domain in domains if domain["status"] == 4]

        # 随机拿一个已启用状态的域名
        domain = random.choice(start_domains)
        print("已启用状态的域名：{}，产品类型为：{}".format(domain["domain"], domain["productCode"]))

        # 删除域名
        delete_domain_url = self.v1_info["changeDomain"]
        delete_domain_payload = self.createV1Domain.delete_domain(self.ctyunacctid, domain["domain"],
                                                                  domain["productCode"])
        delete_domain_response = post_form_head(self.host, delete_domain_url, delete_domain_payload)
        print(delete_domain_response.text)
        print("-------------------验证删除域名是否成功-------------------")
        print('请求url: ' + str(delete_domain_url) + ";")
        print("请求data: " + str(delete_domain_payload) + ";")
        print("返回： " + str(delete_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用失败")
        assert "服务调用成功" not in delete_domain_response.text

    # @pytest.mark.skip("2020/11/12，启用状态域名调用接口再次进行启用，返回失败")
    @allure.story("已启用状态域名，不能再次启用域名")
    def test_CDN_264343(self):
        # 根据域名状态，做域名操作限制
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)
        print("-------------------验证域名列表是否成功-------------------")
        print('请求url: ' + str(list_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(list_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in list_domain_response.text
        assert list_domain_response.elapsed.total_seconds() < 3

        content = json.loads(list_domain_response.text)
        domains = content["data"]["list"]
        start_domains = [domain for domain in domains if domain["status"] == 4]

        # 随机拿一个已启用状态的域名
        domain = random.choice(start_domains)
        print("已启用状态的域名：{}，产品类型为：{}".format(domain["domain"], domain["productCode"]))

        # 启用域名
        start_domain_url = self.v1_info["changeDomain"]
        start_domain_payload = self.createV1Domain.start_domain(self.ctyunacctid, domain["domain"],
                                                                domain["productCode"])
        start_domain_response = post_form_head(self.host, start_domain_url, start_domain_payload)
        print(start_domain_response.text)
        print("-------------------验证启用域名是否成功-------------------")
        print('请求url: ' + str(start_domain_url) + ";")
        print("请求data: " + str(start_domain_payload) + ";")
        print("返回： " + str(start_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" not in start_domain_response.text

    # @pytest.mark.skip("2020/11/12，停用状态域名调用接口再次进行停用，返回失败")
    @allure.story("已停用状态域名，不能再次停用域名")
    def test_CDN_264344(self):
        # 根据域名状态，做域名操作限制
        # 域名列表
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)
        print("-------------------验证域名列表是否成功-------------------")
        print('请求url: ' + str(list_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(list_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in list_domain_response.text
        assert list_domain_response.elapsed.total_seconds() < 3

        content = json.loads(list_domain_response.text)
        domains = content["data"]["list"]
        stop_domains = [domain for domain in domains if domain["status"] == 6]

        # 随机拿一个已停止状态的域名
        domain = random.choice(stop_domains)
        print("已停止状态的域名：{}，产品类型为：{}".format(domain["domain"], domain["productCode"]))

        # 停用域名
        stop_domain_url = self.v1_info["changeDomain"]
        stop_domain_payload = self.createV1Domain.stop_domain(self.ctyunacctid, domain["domain"],
                                                              domain["productCode"])
        stop_domain_response = post_form_head(self.host, stop_domain_url, stop_domain_payload)
        print(stop_domain_response.text)
        print("-------------------验证停用域名是否成功-------------------")
        print('请求url: ' + str(stop_domain_url) + ";")
        print("请求data: " + str(stop_domain_payload) + ";")
        print("返回： " + str(stop_domain_response.text) + ";")
        print("重点验证："  "  expect： 处理成功")
        assert "服务调用成功" not in stop_domain_response.text

    @allure.story("批量新增各个产品域名，包括账号下未开通的产品类型")
    @pytest.mark.parametrize("product, exception", params_data)
    def test_CDN_262424(self, product, exception):
        # 批量新增域名
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.create_domain(self.ctyunacctid, product)
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert exception in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3

        if exception != "尚未开通此产品，不能创建对应类型的域名":
            time.sleep(2)
            # 调用工单列表接口，查找新增的域名工单，状态为进行中，类型为新增
            orderlist_url = self.domain_info["listOrder"]
            self.domain_list.append(payload["data"]["domain"])
            print(self.domain_list)
            order_payload = self.orderData.order_default_data(self.domain_list)
            order_list_response = self.session.post(self.host + orderlist_url, json=order_payload, verify=False,
                                                    timeout=10)
            print(order_list_response.text)
            content = json.loads(order_list_response.text)
            orders = content["data"]["list"]
            order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
                     order["orderType"] == "4" and order["status"] == "2"]
            if order:
                print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
            else:
                print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))
            assert order

    @allure.story("新增全量字段域名")
    def test_CDN_261747(self):
        create_domain_url = self.v1_info["createDomain"]
        payload = self.createV1Domain.full_field_domain(self.ctyunacctid)
        create_domain_response = post_json_head(self.host, create_domain_url, payload)
        print(create_domain_response.text)
        print("-------------------验证新增域名是否成功-------------------")
        print('请求url: ' + str(create_domain_url) + ";")
        print("请求data: " + str(payload) + ";")
        print("返回： " + str(create_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回域名名称")
        assert "服务调用成功" in create_domain_response.text
        assert payload["data"]["domain"] in create_domain_response.text
        assert create_domain_response.elapsed.total_seconds() < 3

    @pytest.mark.skip(" 调试ok ")  # 跳过该测试
    @allure.story(" domain/copy ")
    def test_CDN_240684(self):
        # 域名列表
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)

        content = json.loads(list_domain_response.text)
        all_domain = [domain for domain in content["data"]["list"] if domain["status"] == 4 or
                      domain["status"] == 6]

        domain = random.choice(all_domain)

        # 通过V1--copy 接口创建域名
        v1_domain = 'V1-Test_' + random_string(4) + '.ctyun.cn'
        copydomain_url = self.v1_info['copyDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid,
            "newDomain": v1_domain,
            "originDomain": domain.get("domain"),
            "recordNum": "京ICP备13052560号",
            "recordStatus": 1,
        }
        copy_domain_response = post_form_head(self.host, copydomain_url, data)
        print(copy_domain_response.text)
        print("-------------------验证复制域名是否成功-------------------")
        print('请求url: ' + str(copydomain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(copy_domain_response.text) + ";")
        print("重点验证："  "  expect： 添加成功")
        assert "服务调用成功" in copy_domain_response.text
        assert "添加成功" in copy_domain_response.text
        assert copy_domain_response.elapsed.total_seconds() < 3

    @allure.story(" domain/get ")
    def test_CDN_241508(self):
        # 域名列表
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)

        content = json.loads(list_domain_response.text)
        all_domain = [domain for domain in content["data"]["list"] if domain["status"] == 4 or
                      domain["status"] == 6]

        domain = random.choice(all_domain)

        # 查询域名
        get_domain_url = self.v1_info['getDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid,
            "domain": domain.get("domain")
        }
        get_domain_response = post_form_head(self.host, get_domain_url, data)
        print(get_domain_response.text)
        print("-------------------验证查询域名是否成功-------------------")
        print('请求url: ' + str(get_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(get_domain_response.text) + ";")
        print("重点验证："  "  expect： 返回中有查询的域名名称")
        assert "服务调用成功" in get_domain_response.text
        assert domain.get("domain") in get_domain_response.text
        assert get_domain_response.elapsed.total_seconds() < 3

    @allure.story(" domain/list ")
    def test_CDN_241509(self):
        # 域名列表
        list_domain_url = self.v1_info['listDomain']
        data = {
            "ctyunAcctId": self.ctyunacctid
        }
        list_domain_response = post_form_head(self.host, list_domain_url, data)
        print(list_domain_response.text)
        print("-------------------验证域名列表是否成功-------------------")
        print('请求url: ' + str(list_domain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(list_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in list_domain_response.text
        assert list_domain_response.elapsed.total_seconds() < 3

    @allure.story(" domain/querybyOrigins ")
    def test_CDN_241169(self):
        # 源站查询域名信息
        originsdomain_url = self.v1_info['querybyOrigins']
        data = {
            "ctyunAcctId": self.ctyunacctid,
            "origins": "1.1.1.1"
        }
        origin_domain_response = post_form_head(self.host, originsdomain_url, data)
        print(origin_domain_response.text)
        print("-------------------源站查询域名信息是否成功-------------------")
        print('请求url: ' + str(originsdomain_url) + ";")
        print("请求data: " + str(data) + ";")
        print("返回： " + str(origin_domain_response.text) + ";")
        print("重点验证："  "  expect： 服务调用成功")
        assert "服务调用成功" in origin_domain_response.text
        assert origin_domain_response.elapsed.total_seconds() < 3

    # @pytest.mark.skip("未调通")  # 跳过该测试
    # @pytest.mark.skipif(Init.ENV == 'PE', reason="线上环境无法执行")
    # @allure.story("用户走自助工单，域名新增-配置成功-域名启用-停用-启用-停用-删除")
    # def test_CDN_269265(self):
    #     # 新增域名
    #     create_domain_url = self.v1_info["createDomain"]
    #     payload = self.createV1Domain.create_domain(self.autoctyunid, random.choice(productcode))
    #     create_domain_response = post_json_head(self.host, create_domain_url, payload)
    #     print(create_domain_response.text)
    #     print("-------------------验证新增域名是否成功-------------------")
    #     print('请求url: ' + str(create_domain_url) + ";")
    #     print("请求data: " + str(payload) + ";")
    #     print("返回： " + str(create_domain_response.text) + ";")
    #     print("重点验证："  "  expect： 返回域名名称")
    #     assert "服务调用成功" in create_domain_response.text
    #     assert payload["data"]["domain"] in create_domain_response.text
    #     assert create_domain_response.elapsed.total_seconds() < 3
    #
    #     time.sleep(2)
    #     # 调用工单列表接口，查找新增的域名工单，状态为成功，类型为新增
    #     order_list_url = self.domain_info["listOrder"]
    #     self.auto_domain_list.append(payload["data"]["domain"])
    #     auto_order_payload = self.Auto_orderData.order_default_data(self.auto_domain_list)
    #     auto_order_list_response = self.auto_session.post(self.host + order_list_url, json=auto_order_payload, verify=False,
    #                                                       timeout=10)
    #     print(auto_order_list_response.text)
    #     content = json.loads(auto_order_list_response.text)
    #     orders = content["data"]["list"]
    #
    #     order = [order for order in orders if order["domain"] == payload["data"]["domain"] and
    #              order["orderType"] == "4" and order["status"] == "2"]
    #     if order:
    #         print("已找到域名为{}的新增工单，工单为：{}".format(payload["data"]["domain"], str(order)))
    #     else:
    #         print("未找到域名为{}的新增工单".format(payload["data"]["domain"]))
    #
    #     print("-------------------查询 ListOrder 接口-------------------")
    #     print('请求url: ' + order_list_url)
    #     print("请求data: " + str(auto_order_payload))
    #     print("返回： " + auto_order_list_response.text)
    #     print("重点验证："  " expect： 新增域名在工单列表中，且类型为新增，状态为进行中")
    #     assert order
    #     assert auto_order_list_response.status_code == 200
    #     assert 'core.ok' in auto_order_list_response.text
    #     assert auto_order_list_response.elapsed.total_seconds() < 3
    #
    #     # 自助工单等待时长
    #     time.sleep(120)
    #
    #     # 调用域名列表接口，查找新增成功的域名
    #     domain_list_url = self.domain_info["listDomain"]
    #     params = {
    #         "workspaceId": self.autoworkspaceId,
    #         "page": 1,
    #         "pageSize": 1000
    #     }
    #     domain_list_response = self.auto_session.get(self.host + domain_list_url, params=params, verify=False, timeout=10)
    #     print("-------------------查询 ListV1 接口-------------------")
    #     print('请求url: ' + domain_list_url)
    #     print("请求data: " + str(params))
    #     print("返回： " + domain_list_response.text)
    #     print("重点验证："  " expect： 域名列表中有域名")
    #     assert payload["data"]["domain"] in domain_list_response.text
    #     assert "服务调用成功" in domain_list_response.text
    #
    #     # 编辑域名
    #     edit_domain_payload = self.createV1Domain.edit_domain(self.autoctyunid, payload["data"]["domain"],
    #                                                           payload["data"]["productCode"])
    #     edit_domain_response = post_json_head(self.host, create_domain_url, edit_domain_payload)
    #     print(edit_domain_response.text)
    #     print("-------------------验证编辑域名是否成功-------------------")
    #     print('请求url: ' + str(create_domain_url) + ";")
    #     print("请求data: " + str(edit_domain_payload) + ";")
    #     print("返回： " + str(edit_domain_response.text) + ";")
    #     print("重点验证："  "  expect： 返回域名名称")
    #     assert "服务调用成功" in edit_domain_response.text
    #     assert payload["data"]["domain"] in edit_domain_response.text
    #     time.sleep(2)
    #
    #     # 调用工单列表接口，查找更新的域名工单，状态为进行中，类型为更新
    #     order_list_response_2 = self.auto_session.post(self.host + order_list_url, json=auto_order_payload, verify=False,
    #                                                    timeout=10)
    #     print(order_list_response_2.text)
    #     content_2 = json.loads(order_list_response_2.text)
    #     orders_2 = content_2["data"]["list"]
    #     order_2 = [order for order in orders_2 if order["domain"] == payload["data"]["domain"] and
    #                order["orderType"] == "5" and order["status"] == "2"]
    #     if order_2:
    #         print("已找到域名为{}的更新工单，工单为：{}".format(payload["data"]["domain"], str(order_2)))
    #     else:
    #         print("未找到域名为{}的更新工单".format(payload["data"]["domain"]))
    #     assert order_2
    #
    #     # 工单等待时长
    #     time.sleep(120)
    #
    #     # 调用工单列表接口，查找更新的域名工单，状态为成功，类型为更新
    #     order_list_response_3 = self.session.post(self.host + order_list_url, json=auto_order_payload, verify=False,
    #                                               timeout=10)
    #     print(order_list_response_3.text)
    #     content_3 = json.loads(order_list_response_3.text)
    #     orders_3 = content_3["data"]["list"]
    #     order_3 = [order for order in orders_3 if order["domain"] == payload["data"]["domain"] and
    #                order["orderType"] == "5" and order["status"] == "3"]
    #     if order_3:
    #         print("已找到域名为{}的更新成功工单，工单为：{}".format(payload["data"]["domain"], str(order_3)))
    #     else:
    #         print("未找到域名为{}的更新成功工单".format(payload["data"]["domain"]))
    #     assert order_3
    #
    #     # 停用域名
    #     stop_domain_url = self.v1_info["changeDomain"]
    #     stop_domain_payload = self.createV1Domain.stop_domain(self.autoctyunid, payload["data"]["domain"],
    #                                                           payload["data"]["productCode"])
    #     stop_domain_response = post_form_head(self.host, stop_domain_url, stop_domain_payload)
    #     print(stop_domain_response.text)
    #     print("-------------------验证停用域名是否成功-------------------")
    #     print('请求url: ' + str(stop_domain_url) + ";")
    #     print("请求data: " + str(stop_domain_payload) + ";")
    #     print("返回： " + str(stop_domain_response.text) + ";")
    #     print("重点验证："  "  expect： 处理成功")
    #     assert "服务调用成功" in stop_domain_response.text
    #     assert "处理成功" in stop_domain_response.text
    #
    #     # 自助工单等待时长
    #     time.sleep(120)
    #
    #     # 调用域名列表接口，查找停用成功的域名
    #     domain_list_response = self.auto_session.get(self.host + domain_list_url, params=params, verify=False,
    #                                                  timeout=10)
    #     domain_content = json.loads(domain_list_response.text)
    #     all_domains = domain_content["data"]["list"]
    #     domain = [domain for domain in all_domains if domain["domain"] == payload["data"]["domain"]]
    #     print("-------------------查询 ListV1 接口-------------------")
    #     print('请求url: ' + domain_list_url)
    #     print("请求data: " + str(params))
    #     print("返回： " + domain_list_response.text)
    #     print("重点验证："  " expect： 域名列表中中域名状态为已停止")
    #     assert domain[0].get("status") == 6
    #     assert "服务调用成功" in domain_list_response.text
    #
    #     # 启用域名
    #     start_domain_url = self.v1_info["changeDomain"]
    #     start_domain_payload = self.createV1Domain.start_domain(self.autoctyunid, payload["data"]["domain"],
    #                                                             payload["data"]["productCode"])
    #     start_domain_response = post_form_head(self.host, start_domain_url, start_domain_payload)
    #     print(start_domain_response.text)
    #     print("-------------------验证启用域名是否成功-------------------")
    #     print('请求url: ' + str(start_domain_url) + ";")
    #     print("请求data: " + str(start_domain_payload) + ";")
    #     print("返回： " + str(start_domain_response.text) + ";")
    #     print("重点验证："  "  expect： 处理成功")
    #     assert "服务调用成功" in start_domain_response.text
    #     assert "处理成功" in start_domain_response.text
    #
    #     # 自助工单等待时长
    #     time.sleep(120)
    #
    #     # 调用域名列表接口，查找启用成功的域名
    #     domain_list_response_2 = self.auto_session.get(self.host + domain_list_url, params=params, verify=False,
    #                                                    timeout=10)
    #     domain_content_2 = json.loads(domain_list_response_2.text)
    #     all_domains_2 = domain_content_2["data"]["list"]
    #     domain_2 = [domain for domain in all_domains_2 if domain["domain"] == payload["data"]["domain"]]
    #     print("-------------------查询 ListV1 接口-------------------")
    #     print('请求url: ' + domain_list_url)
    #     print("请求data: " + str(params))
    #     print("返回： " + domain_list_response_2.text)
    #     print("重点验证："  " expect： 域名列表中中域名状态为已启用")
    #     assert domain_2[0].get("status") == 4
    #     assert "服务调用成功" in domain_list_response_2.text
    #
    #     # 第二次停用域名
    #     stop_domain_response_2 = post_form_head(self.host, stop_domain_url, stop_domain_payload)
    #     print(stop_domain_response_2.text)
    #     assert "服务调用成功" in stop_domain_response_2.text
    #     assert "处理成功" in stop_domain_response_2.text
    #
    #     # 自助工单等待时长
    #     time.sleep(120)
    #
    #     # 调用域名列表接口，查找停用成功的域名
    #     domain_list_response_3 = self.auto_session.get(self.host + domain_list_url, params=params, verify=False,
    #                                                    timeout=10)
    #     domain_content_3 = json.loads(domain_list_response_3.text)
    #     all_domains_3 = domain_content_3["data"]["list"]
    #     domain_3 = [domain for domain in all_domains_3 if domain["domain"] == payload["data"]["domain"]]
    #     print("-------------------查询 ListV1 接口-------------------")
    #     print('请求url: ' + domain_list_url)
    #     print("请求data: " + str(params))
    #     print("返回： " + domain_list_response_3.text)
    #     print("重点验证："  " expect： 域名列表中中域名状态为已停止")
    #     assert domain_3[0].get("status") == 6
    #     assert "服务调用成功" in domain_list_response_3.text
    #
    #     # 删除域名
    #     delete_domain_url = self.v1_info["changeDomain"]
    #     delete_domain_payload = self.createV1Domain.delete_domain(self.autoctyunid, payload["data"]["domain"],
    #                                                               payload["data"]["productCode"])
    #     delete_domain_response = post_form_head(self.host, delete_domain_url, delete_domain_payload)
    #     print(delete_domain_response.text)
    #     print("-------------------验证删除域名是否成功-------------------")
    #     print('请求url: ' + str(delete_domain_url) + ";")
    #     print("请求data: " + str(delete_domain_payload) + ";")
    #     print("返回： " + str(delete_domain_response.text) + ";")
    #     print("重点验证："  "  expect： 处理成功")
    #     assert "服务调用成功" in delete_domain_response.text
    #     assert "处理成功" in delete_domain_response.text
    #
    #     # 自助工单等待时长
    #     time.sleep(120)
    #
    #     # 调用域名列表接口，查找删除成功的域名
    #     domain_list_response_4 = self.auto_session.get(self.host + domain_list_url, params=params, verify=False,
    #                                                    timeout=10)
    #     print("-------------------查询 ListV1 接口-------------------")
    #     print('请求url: ' + domain_list_url)
    #     print("请求data: " + str(params))
    #     print("返回： " + domain_list_response_4.text)
    #     print("重点验证："  " expect： 域名列表中无该域名")
    #     assert payload["data"]["domain"] not in domain_list_response_4.text
    #     assert "服务调用成功" in domain_list_response_4.text










