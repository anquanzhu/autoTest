# -*- coding: utf-8 -*-
import json
import random
import time

import allure
import pytest
from bin.Init import Init
from bin.Mysql import DbConnect
from bin.unit.Rondom import random_string
from bin.unit.Session import Session

headers_json = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Content-Type": "application/json",
}
headers_form = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Content-Type": "application/x-www-form-urlencoded",
}
public_key_365 = Init.PUBLIC_KEY
private_key_365 = Init.PRIVATE_KEY
public_key_expire = Init.PUBLIC_KEY_EXPIRE
private_key_expire = Init.PRIVATE_KEY_EXPIRE


@allure.feature("BS 客户控制台-证书模块")
class Test_BS_cert():

    def setup_class(self):
        # print('test start')
        self.base_info = Init.BASE_INFO
        self.cert_info = Init.CERT_INFO
        # self.request = Request('test')
        self.session = Init.BS_SESSION
        self.db = DbConnect()

    def teardown_class(self):
        # 做清数据，退出登录等
        self.db.close()
        print('-------------------test end-------------------')

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    @allure.severity('blocker')
    @allure.story('证书创建成功')
    def test_CDN_243770(self):
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        email = self.base_info['email']
        createCert_url = console_host + self.cert_info['createCert']
        select_cert_url = console_host + self.cert_info['viewCert']
        cert_name = 'Auto_Cert_' + random_string(4)
        createCert_data = {
            "data": {"workspaceId": workspace_id, "name": cert_name, "certs": public_key_365, "key": private_key_365,
                     "email": email}}
        cert_response = self.session.post(url=createCert_url, data=json.dumps(createCert_data), headers=headers_json,
                                          verify=False, timeout=10)
        print("-------------------创建证书-------------------")
        print('请求url: ' + str(createCert_url))
        print("请求data: " + str(createCert_data))
        print("返回： " + str(cert_response.text))
        print("重点验证：" + cert_name + "  expect： 返回里面有证书名")
        assert cert_name in cert_response.text
        assert '服务调用成功' in cert_response.text

        select_data = 'workspaceId=' + workspace_id + '&name=' + cert_name + ''
        select_cert_response = self.session.get(url=select_cert_url, params=select_data, headers=headers_form,
                                                verify=False, timeout=10)
        assert '服务调用成功' in select_cert_response.text

        print("-------------------控制台查询证书是否创建成功-------------------")
        print('请求url: ' + str(select_cert_url))
        print("请求data: " + str(select_data))
        print("返回： " + str(select_cert_response.text))
        print("重点验证：" + cert_name + "  expect： 返回里面有证书名")

        # 线上无数据库权限，这部分验证取消
        # sql = 'select * from ecfSecret.certificate_metadata  where name= \'%s\'' % cert_name
        # r = self.db.select(sql)
        # print("-------------------数据库查询证书是否入库-------------------")
        # print("数据库查询结果：", r)
        # assert cert_name in r[0]['name']

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    @allure.severity("blocker")
    @allure.story('创建证书---查询---删除证书')
    def test_CDN_243771(self):
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        email = self.base_info['email']
        createCert_url = console_host + self.cert_info['createCert']
        select_cert_url = console_host + self.cert_info['viewCert']
        del_cert_url = console_host + self.cert_info['delCert']
        certList_url = console_host + self.cert_info['listCert']
        cert_name = 'Auto_Cert_' + random_string(4)
        createCert_data = {
            "data": {"workspaceId": workspace_id, "name": cert_name, "certs": public_key_365, "key": private_key_365,
                     "email": email}}
        cert_response = self.session.post(url=createCert_url, data=json.dumps(createCert_data), headers=headers_json,
                                          verify=False, timeout=10)
        print("-------------------创建证书-------------------")
        print('请求url: ' + str(createCert_url))
        print("请求data: " + str(createCert_data))
        print("返回： " + str(cert_response.text))
        print("重点验证：" + cert_name + "  expect： 返回里面有证书名")

        assert cert_name in cert_response.text
        assert '服务调用成功' in cert_response.text
        assert cert_response.status_code == 200
        assert cert_response.elapsed.total_seconds() < 3

        select_data = 'workspaceId=' + workspace_id + '&name=' + cert_name + ''
        select_cert_response = self.session.get(url=select_cert_url, params=select_data, headers=headers_form,
                                                verify=False, timeout=10)
        assert '服务调用成功' in select_cert_response.text
        assert cert_response.status_code == 200
        assert cert_response.elapsed.total_seconds() < 3
        print("-------------------控制台查询证书是否创建成功-------------------")
        print('请求url: ' + str(select_cert_url))
        print("请求data: " + str(select_data))
        print("返回： " + str(select_cert_response.text))
        print("重点验证：" + cert_name + "  expect： 返回里面有证书名")

        # 线上无数据库权限，这部分验证取消
        # sql = 'select * from ecfSecret.certificate_metadata  where name= \'%s\'' % cert_name
        # r = self.db.select(sql)
        # print("-------------------数据库查询证书是否入库-------------------")
        # print("数据库查询结果：", r)
        # assert cert_name in r[0]['name']
        # self.db.close() # python 查询数据库有缓存，存储在内存中

        # 删除证书
        del_response = self.session.get(url=del_cert_url, params=select_data, headers=headers_form, verify=False,
                                        timeout=10)
        print("-------------------删除证书-------------------")
        print('请求url: ' + str(del_cert_url))
        print("请求data: " + str(select_data))
        print("返回： " + str(del_response.text))
        assert del_response.status_code == 200
        assert del_response.elapsed.total_seconds() < 3

        # 去数据库查询是否删除成功
        time.sleep(2)
        list_data = 'workspaceId=' + workspace_id + '&page=1&perPage=50'
        list_respones = self.session.get(url=certList_url, params=list_data, headers=headers_form, verify=False,
                                         timeout=10)
        assert cert_name not in list_respones.text
        print("-------------------控制台查询证书是否消失-------------------")
        print('请求url: ' + str(certList_url))
        print("请求data: " + str(list_data))
        print("返回： " + str(list_respones.text))

        # del_r = self.db.select(sql)
        # print("-------------------数据库查询证书是否消失-------------------")
        # print("数据库查询结果：", del_r)
        # assert del_r == ()

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    @allure.severity('normal')
    @allure.story('创建过期的证书')
    def test_CDN_243772(self):
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        email = self.base_info['email']
        createCert_url = console_host + self.cert_info['createCert']
        select_cert_url = console_host + self.cert_info['viewCert']
        cert_name = 'Auto_Cert_' + random_string(4)
        createCert_data = {
            "data": {"workspaceId": workspace_id, "name": cert_name, "certs": public_key_expire,
                     "key": private_key_expire,
                     "email": email}}
        cert_response = self.session.post(url=createCert_url, data=json.dumps(createCert_data), headers=headers_json,
                                          verify=False, timeout=10)
        print("-------------------创建证书-------------------")
        print('请求url: ' + str(createCert_url))
        print("请求data: " + str(createCert_data))
        print("返回： " + str(cert_response.text))
        print("重点验证：" + cert_name + "  expect： 创建证书异常：证书已过期")

        assert '创建证书异常：证书已过期' in cert_response.text
        assert cert_response.status_code == 200
        assert cert_response.elapsed.total_seconds() < 3

        select_data = 'workspaceId=' + workspace_id + '&name=' + cert_name + ''
        select_cert_response = self.session.get(url=select_cert_url, params=select_data, headers=headers_form,
                                                verify=False, timeout=10)
        body1 = eval(select_cert_response.text)
        result = body1['data']['result']
        print("-------------------控制台查询证书是否创建-------------------")
        print('请求url: ' + str(select_cert_url))
        print("请求data: " + str(select_data))
        print("返回： " + str(select_cert_response.text))
        # print(result)
        assert '服务调用成功' in select_cert_response.text
        assert result == '[]'

        # sql = 'select * from ecfSecret.certificate_metadata  where name= \'%s\'' % cert_name
        # r = self.db.select(sql)
        # print("-------------------数据库查询证书是否为空-------------------")
        # print("数据库查询结果：", r)
        # assert r == ()

    @allure.severity('normal')
    @allure.story('创建不存在的证书')
    def test_CDN_243773(self):
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        email = self.base_info['email']
        createCert_url = console_host + self.cert_info['createCert']
        select_cert_url = console_host + self.cert_info['viewCert']
        cert_name = 'Auto_Cert_' + random_string(4)
        createCert_data = {
            "data": {"workspaceId": workspace_id, "name": cert_name, "certs": 'test_certs',
                     "key": 'test_key',
                     "email": email}}
        cert_response = self.session.post(url=createCert_url, data=json.dumps(createCert_data), headers=headers_json,
                                          verify=False, timeout=10)
        print("-------------------创建证书-------------------")
        print('请求url: ' + str(createCert_url))
        print("请求data: " + str(createCert_data))
        print("返回： " + str(cert_response.text))
        print("重点验证：" + cert_name + "  expect： 创建证书异常：证书已过期")

        assert cert_response.status_code == 200
        assert cert_response.elapsed.total_seconds() < 3
        assert '创建证书异常' in cert_response.text
        assert 'core.e' in cert_response.text

    @allure.severity('normal')
    @allure.story('创建已有的证书')
    def test_CDN_244101(self):
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        email = self.base_info['email']
        certList_url = console_host + self.cert_info['listCert']
        createCert_url = console_host + self.cert_info['createCert']
        list_data = 'workspaceId=' + workspace_id + '&page=1&perPage=50'
        list_respones = self.session.get(url=certList_url, params=list_data, headers=headers_form, verify=False,
                                         timeout=10)
        print("list:", list_respones.text)
        exist_certName = []
        temp = json.loads(list_respones.text)['data']['secrets']
        if temp != []:
            for item in temp:
                exist_certName.append(item['name'])
        else:
            exist_certName = []
            print("用户没有已存在的证书，请先创建！")
        cert_name = random.choice(exist_certName)
        createCert_data = {
            "data": {"workspaceId": workspace_id, "name": cert_name, "certs": public_key_365,
                     "key": private_key_365,
                     "email": email}}
        cert_response = self.session.post(url=createCert_url, data=json.dumps(createCert_data), headers=headers_json,
                                          verify=False, timeout=10)
        print("-------------------创建证书-------------------")
        print('请求url: ' + str(createCert_url))
        print("请求data: " + str(createCert_data))
        print("返回： " + str(cert_response.text))
        print("重点验证：" + cert_name + "  expect： 创建证书异常：证书已过期")

        assert cert_response.status_code == 200
        assert cert_response.elapsed.total_seconds() < 3
        assert '创建证书异常：已存在重名的证书' in cert_response.text
        assert 'core.e' in cert_response.text

    @allure.story("证书数量校对")
    def test_CDN_260850(self):
        """
        核对证书管理页面证书数量与概览页证书数量一致，关联到2个CertList接口，url一样，请求方式及请求数据不同
        :return:
        """
        console_host = self.base_info['bsHost']
        workspace_id = self.base_info['ctyunAcctId']
        certList_url = console_host + self.cert_info['listCert']
        params = {
            "workspaceId": workspace_id,
            "page": 1,
            "perPage": 10
        }
        response = self.session.get(certList_url, params=params, verify=False, timeout=10)
        print(response.text)
        content = json.loads(response.text)
        willExpiredCount = content["data"]["willExpiredCount"]
        total = content["data"]["paging"]["total_record"]

        # 概览页证书接口
        views_cert_data = {
            "data": {
                "limit": 9999,
                "workspaceId": workspace_id
            }
        }
        views_cert_response = self.session.post(certList_url, json=views_cert_data, verify=False,
                                                timeout=10)
        views_content = json.loads(views_cert_response.text)
        views_willExpiredCount = views_content["data"]["willExpiredCount"]
        views_total = views_content["data"]["paging"]["total_record"]
        print(views_cert_response.text)
        print("-------------------CertList接口-------------------")
        print('请求url: ' + str(certList_url))
        print("请求data: " + str(views_cert_data))
        print("返回： " + str(views_cert_response.text))
        print("重点验证：" + "  expect： 证书数量一致性")

        assert response.status_code == 200
        assert "服务调用成功" in views_cert_response.text
        assert willExpiredCount == views_willExpiredCount
        assert total == views_total
        assert views_cert_response.elapsed.total_seconds() < 3
