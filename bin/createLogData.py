# -*- coding: utf-8 -*-
import json
import random
import time
from datetime import date, timedelta, datetime

from bin.Init import Init
from bin.unit import Log
from bin.unit.Params import get_unix_time

productCode = ['001', '003', '004', '005']

'''
    用于生成日志查询类的查询条件
    1.请求数和带宽流量 有运营商和地区选择， 其他的没有

'''
yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
before_yesterday = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
today = time.strftime("%Y-%m-%d", time.localtime())
sevenday = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d %H:%M:%S")
month = (date.today() + timedelta(days=-29)).strftime("%Y-%m-%d %H:%M:%S")
day_time = int(time.mktime(datetime.now().date().timetuple()))
now_time = get_unix_time(now)
sevenday_time = get_unix_time(sevenday)
month_time = get_unix_time(month)
yesterday_time = get_unix_time(yesterday)
productCode = ['001', '003', '004', '005']
isp = [1, 2, 3, 4, 5, 6, 100]
province = ["110000", "120000", "130000", "140000", "150000", "210000", "220000", "230000", "310000", "320000",
            "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "440000", "450000",
            "460000", "500000", "510000", "520000", "530000", "540000", "610000", "620000", "630000", "640000",
            "650000"]

date = [yesterday_time, sevenday_time, month_time]


class CreateLogData:
    # yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
    # now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # sevenday = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d %H:%M:%S")
    # month = (date.today() + timedelta(days=-29)).strftime("%Y-%m-%d %H:%M:%S")
    # day_time = int(time.mktime(datetime.now().date().timetuple()))
    # now_time = get_unix_time(now)
    # sevenday_time = get_unix_time(sevenday)
    # month_time = get_unix_time(month)
    # yesterday_time = get_unix_time(yesterday)
    # date = [yesterday_time, sevenday_time, month_time]

    def __init__(self):
        self.log = Log.Log()
        self.workspaceId = Init.BASE_INFO['workspaceid']
        self.base_info = Init.BASE_INFO
        self.domain_info = Init.DOMAIN_INFO
        self.session = Init.CONSOLE_SESSION
        self.day_time = int(time.mktime(datetime.now().date().timetuple()))
        self.now_time = get_unix_time(now)
        self.sevenday_time = get_unix_time(sevenday)
        self.month_time = get_unix_time(month)
        self.yesterday_time = get_unix_time(yesterday)
        self.before_yesterday = get_unix_time(before_yesterday)
        self.date = [yesterday_time, sevenday_time, month_time]
        self.ctyun_session = Init.CTYUN_SESSION
        self.bs_session = Init.BS_SESSION
        # self.bs_session=Init.BS_SESSION

    def get_bs_domain_list(self, ctyunacctid):
        list_domain = self.base_info['bsHost'] + self.domain_info['listDomain']
        list_data = 'workspaceId=' + ctyunacctid + '&page=1&page_size=10000'
        list_response = self.bs_session.get(url=list_domain, params=list_data, headers=self.base_info['headers_form'],
                                            verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            # if 'Auto' in domain:
            domain_list.append(domain)
        # print(domain_list)
        return domain_list

    def get_bs_cp_domain(self, host, workspaceid, product_code):

        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.bs_session.get(url=list_domain, params=list_data,
                                            headers=self.base_info['headers_form'],
                                            verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            code = temp[i]['productCode']
            if product_code == code:
                domain_list.append(domain)
        # print(domain_list)
        return domain_list

    def get_domain_list(self):
        list_domain = self.base_info['host'] + self.domain_info['listDomain']
        list_data = 'workspaceId=' + self.workspaceId + '&page=1&page_size=1000'
        list_response = self.session.get(url=list_domain, params=list_data, headers=self.base_info['headers_form'],
                                         verify=False, timeout=10)
        print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            # if 'Auto' in domain:
            domain_list.append(domain)
        # print(domain_list)
        return domain_list

    def get_ctyun_domain_list(self, host, workspaceid):
        """
        由于可能使用不同控制台，不用用户的情况，那么Host， workspaceid不宜写死。
        :param host:
        :param workspaceid:
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.ctyun_session.get(url=list_domain, params=list_data,
                                               headers=self.base_info['headers_form'],
                                               verify=False, timeout=10)
        print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        print("body:", body)
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            # if 'Auto' in domain:
            domain_list.append(domain)
        # print(domain_list)
        return domain_list

    def get_ctyun_cp_domain(self, host, workspaceid, product_code):
        """
        由于可能使用不同控制台，不用用户的情况，那么Host， workspaceid不宜写死。
        :param host:
        :param workspaceid:
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.ctyun_session.get(url=list_domain, params=list_data,
                                               headers=self.base_info['headers_form'],
                                               verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            code = temp[i]['productCode']
            if product_code == code:
                domain_list.append(domain)
        # print(domain_list)
        return domain_list

    def get_available_domain_list(self):
        list_domain = self.base_info['host'] + self.domain_info['listDomain']
        list_data = 'workspaceId=' + self.workspaceId + '&do=c_order&from=order'
        list_response = self.session.get(url=list_domain, params=list_data, headers=self.base_info['headers_form'],
                                         verify=False, timeout=10)
        print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == '4' or status == 4:
                domain_list.append(domain)
        print(domain_list)
        return domain_list

    def get_cp_domain(self, product_code):
        list_domain = self.base_info['host'] + self.domain_info['listDomain']
        list_data = 'workspaceId=' + self.workspaceId + '&page=1&page_size=10000'
        list_response = self.session.get(url=list_domain, params=list_data, headers=self.base_info['headers_form'],
                                         verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            code = temp[i]['productCode']
            if product_code == code:
                domain_list.append(domain)
        # print(domain_list)
        return domain_list

    # 所有日志查询通用的默认数据
    def common_query_data(self):
        default_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                 "domain": self.get_domain_list(), "startTime": day_time,
                                 "endTime": now_time}}
        # print(type(default_data))
        return default_data

    def get_multi_data(self):

        data_list = []
        data_list.append(self.common_query_data())
        for code in productCode:
            cp_data = {"data": {"workspaceId": self.workspaceId, "productType": [code], "isp": [], "province": [],
                                "domain": self.get_cp_domain(code), "startTime": day_time,
                                "endTime": now_time}}

            data_list.append(cp_data)

        for isp_code in isp:
            isp_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [isp_code], "province": [],
                                 "domain": self.get_domain_list(), "startTime": day_time,
                                 "endTime": now_time}}
            data_list.append(isp_data)

        for i in range(3):
            province_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [],
                                      "province": [random.choice(province)],
                                      "domain": self.get_domain_list(), "startTime": day_time,
                                      "endTime": now_time}}
            data_list.append(province_data)

        for date_code in date:
            date_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "isp": [], "province": [],
                                  "domain": self.get_domain_list(), "startTime": date_code,
                                  "endTime": now_time}}
            data_list.append(date_data)

        # print(len(data_list), data_list)

        return data_list

    def get_user_data(self):
        user_data_list = []
        for code in productCode:
            user_data = {
                "data": {"workspaceId": self.workspaceId, "productType": [code], "domain": self.get_cp_domain(code),
                         "startTime": day_time, "endTime": now_time}}
            user_data_list.append(user_data)
        default_data = {"data": {"workspaceId": self.workspaceId, "productType": [], "domain": self.get_domain_list(),
                                 "startTime": day_time, "endTime": now_time}}
        user_data_list.append(default_data)
        return user_data_list

    def get_used_domain_list(self):
        list_domain = self.base_info['host'] + self.domain_info['listDomain']
        list_data = 'workspaceId=' + self.workspaceId + '&page=1&page_size=10000'
        list_response = self.session.get(url=list_domain, params=list_data, headers=self.base_info['headers_form'],
                                         verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == 4 and '*' not in domain:
                domain_list.append(domain)
        # print(domain_list)
        domain_header = ['http://', 'https://']
        values_domain = []
        for domain in domain_list:
            temp1 = domain_header[0] + domain
            temp2 = domain_header[1] + domain
            values_domain.append(temp1)
            values_domain.append(temp2)
        # print(values_domain)

        return values_domain

    def get_ctyun_used_domain_list(self, host, workspaceid):
        """
        解决CTYUN获取刷新预取URL的问题
        :param host
        :param workspaceid
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.ctyun_session.get(url=list_domain, params=list_data,
                                               headers=self.base_info['headers_form'],
                                               verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == 4 and '*' not in domain:
                domain_list.append(domain)
        # print(domain_list)
        domain_header = ['http://', 'https://']
        values_domain = []
        for domain in domain_list:
            temp1 = domain_header[0] + domain
            temp2 = domain_header[1] + domain
            values_domain.append(temp1)
            values_domain.append(temp2)
        # print(values_domain)

        return values_domain

    def get_ctyun_all_domain(self, host, workspaceid):
        """
        解决CTYUN获取刷新预取URL的问题
        :param host
        :param workspaceid
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.ctyun_session.get(url=list_domain, params=list_data,
                                               headers=self.base_info['headers_form'],
                                               verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == 4 and '*' in domain:
                domain_list.append(domain)
        # print(domain_list)
        domain_header = ['http://', 'https://']
        values_domain = []
        for domain in domain_list:
            temp1 = domain_header[0] + domain
            temp2 = domain_header[1] + domain
            values_domain.append(temp1)
            values_domain.append(temp2)
        # print(values_domain)

        return values_domain

    def get_bs_used_domain_list(self, host, workspaceid):
        """
        解决CTYUN获取刷新预取URL的问题
        :param host
        :param workspaceid
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.bs_session.get(url=list_domain, params=list_data,
                                            headers=self.base_info['headers_form'],
                                            verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == 4 and '*' not in domain:
                domain_list.append(domain)
        # print(domain_list)
        domain_header = ['http://', 'https://']
        values_domain = []
        for domain in domain_list:
            temp1 = domain_header[0] + domain
            temp2 = domain_header[1] + domain
            values_domain.append(temp1)
            values_domain.append(temp2)
        # print(values_domain)

        return values_domain

    def get_bs_all_domain(self, host, workspaceid):
        """
        解决CTYUN获取刷新预取URL的问题
        :param host
        :param workspaceid
        :return:
        """
        list_domain = host + self.domain_info['listDomain']
        list_data = 'workspaceId=' + workspaceid + '&page=1&page_size=10000'
        list_response = self.bs_session.get(url=list_domain, params=list_data,
                                            headers=self.base_info['headers_form'],
                                            verify=False, timeout=10)
        # print(list_response.text)
        body = json.loads(list_response.text)
        domain_list = []
        temp = body['data']['list']
        for i in range(len(temp)):
            domain = temp[i]['domain']
            status = temp[i]['status']
            if status == 4 and '*' in domain:
                domain_list.append(domain)
        # print(domain_list)
        domain_header = ['http://', 'https://']
        values_domain = []
        for domain in domain_list:
            temp1 = domain_header[0] + domain
            temp2 = domain_header[1] + domain
            values_domain.append(temp1)
            values_domain.append(temp2)
        # print(values_domain)

        return values_domain


if __name__ == '__main__':
    a = CreateLogData()
    # a.get_ctyun_domain_list('http://bs.ctcdn.cn/bs', '0dba69812ab444c4adc90edbf080b210')
    a.get_domain_list()
