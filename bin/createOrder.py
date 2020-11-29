# -*- coding: utf-8 -*-

from bin.Init import Init
from bin.createLogData import CreateLogData
import json
import random

orderType = ["1", "2", "3", "4", "5"]
status = ["0", "2", "3", "4"]


class createOrderData(object):

    def __init__(self, session, host, workspaceid):
        self.domain_info = Init.DOMAIN_INFO
        self.base_info = Init.BASE_INFO
        self.session = session
        self.host = host
        self.workspaceId = workspaceid
        self.log = CreateLogData()

    def order_domainlist_data(self):
        """
        权限域名数据
        :return:
        """
        content = {
            "workspaceId": self.workspaceId,
            "do": "c_order",
            "from": "order"
        }
        return content

    def order_default_data(self, domainlist):
        """
        # 工单默认查询数据
        :return:
        """
        content = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": domainlist,
                "page": 1,
                "pageSize": 1000,
                "page_size": 1000,
                "orderType": "",
                "status": "",
                "startTime": "",
                "endTime": ""
            }
        }
        return content

    def order_domain_data(self, domainlist):
        """
        域名类型查询数据
        :return:
        """
        content = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": [random.choice(domainlist)],
                "page": 1,
                "pageSize": 10,
                "page_size": 10,
                "orderType": "",
                "status": "",
                "startTime": "",
                "endTime": ""
            }
        }
        return content

    def order_type_data(self, domainlist):
        """
        工单类型查询数据
        :return:
        """
        content = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": domainlist,
                "page": 1,
                "pageSize": 10,
                "page_size": 10,
                "orderType": random.choice(orderType),
                "status": "",
                "startTime": "",
                "endTime": ""
            }
        }
        return content

    def order_status_data(self, domainlist):
        """
        工单状态数据
        :return:
        """
        content = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": domainlist,
                "page": 1,
                "pageSize": 10,
                "page_size": 10,
                "orderType": "",
                "status": random.choice(status),
                "startTime": "",
                "endTime": ""
            }
        }
        return content

    def order_time_data(self, domainlist):
        """
        时间查询数据，默认查询昨天
        :return:
        """
        content = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": domainlist,
                "page": 1,
                "pageSize": 10,
                "page_size": 10,
                "orderType": "",
                "status": "",
                "startTime": self.log.yesterday_time,
                "endTime": self.log.day_time
            }
        }
        return content

    def order_domainlist(self):
        """
        工单中域名列表
        :return: 域名列表
        """
        domain_url = self.domain_info["listDomainV2"]
        params = self.order_domainlist_data()
        response = self.session.get(self.host + domain_url, params=params, verify=False)
        print(response.text)
        content = json.loads(response.text)
        # 获取工单域名
        all_domain = [domain.get("name") for domain in content["data"]["list"] if domain["enable"] == "true"]
        return all_domain

    def list_orderid(self, domainlist):
        """
        工单id列表，前10条
        :return:
        """
        orderlist_url = self.domain_info["listOrder"]
        paylod = self.order_default_data(domainlist)
        response = self.session.post(self.host + orderlist_url, json=paylod, verify=False)
        content = json.loads(response.text)
        # 工单id列表
        all_orderid = [order.get("orderId") for order in content["data"]["list"]]
        return all_orderid

    def domain_status_4(self, domainlist):
        """
        失败状态工单的域名列表
        :return:
        """
        orderlist_url = self.domain_info["listOrder"]
        paylod = {
            "data": {
                "workspaceId": self.workspaceId,
                "domainList": domainlist,
                "page": 1,
                "pageSize": 1000,
                "page_size": 1000,
                "orderType": "",
                "status": "4",
                "startTime": "",
                "endTime": ""
            }
        }
        response = self.session.post(self.host + orderlist_url, json=paylod, verify=False)
        content = json.loads(response.text)
        # 失败状态工单的域名列表
        domain_list = [order.get("domain") for order in content["data"]["list"]]

        return domain_list

    def domain_orderlist(self):
        """
        域名列表中的在途工单
        :return: 域名管理中的在途工单列表
        """
        order_list = []
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        content = json.loads(response.text)
        # 判断域名列表下有无在途工单
        if not content["data"]["orderList"]:
            print("域名列表中无在途工单")
            order_list = []
        else:
            orderList = content["data"]["orderList"]
            domainList = content["data"]["list"]
            # 判断工单下的域名真实存在域名列表中
            for order in orderList:
                for domain in domainList:
                    domain_name = order.get("domain")
                    if domain_name in domain.get("domain"):
                        order_list.append(order)

        return order_list

    def domain_manage_list(self, d_status):
        """
        不同状态的域名列表
        :param d_status: 域名状态, 4为已启用，6为已停用
        :return: 不同状态的域名列表
        """
        if d_status != 4 and d_status != 6:
            raise Exception("d_status输入错误！请输入4或6")
        url = self.domain_info["listDomain"]
        params = {
            "workspaceId": self.workspaceId,
            "page": 1,
            "pageSize": 1000
        }
        response = self.session.get(self.host + url, params=params, verify=False, timeout=10)
        content = json.loads(response.text)
        if not content["data"]["list"]:
            print("域名列表为空")
        domain_list = content["data"]["list"]
        # 时间戳，由于旧数据可能无工单，筛选新增时间在1598889600000(即2020/9/1 00:00:00)之后的域名
        unix = 1598889600000
        domain_status_list = [domain for domain in domain_list if domain["status"] == d_status and
                              int(domain["insertDate"]) >= unix]

        return domain_status_list

    def get_OrderId(self, domain):
        """
            通过某个域名查询该域名的在途工单 orderid
            在途工单只能是进行中或者失败状态（失败的话可以重新发起）
            :return:
        """
        orderlist_url = self.domain_info["listOrder"]
        paylod = self.order_default_data(self.order_domainlist())
        print("payload: ", paylod)
        response = self.session.post(self.host + orderlist_url, json=paylod, verify=False)
        content = json.loads(response.text)
        print("content: ", content["data"]["list"])
        order_list = []
        for item in content["data"]["list"]:
            if domain == item['domain']:
                order_list.append(item)
        print("order: ", order_list)
        if not order_list:
            return
        else:
            for temp in order_list:
                if temp['status'] == "2" or temp['status'] == "4":
                    return temp['orderId']


if __name__ == '__main__':
    console_host = "https://iam-test.ctcdn.cn"
    wid = "10003885"
    s = Init.CONSOLE_SESSION
    orders = createOrderData(s, console_host, wid)
    d = orders.get_OrderId('Auto-Qf55HS.ctyun.cn')
    print(d)
