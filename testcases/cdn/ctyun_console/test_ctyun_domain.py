# -*- coding: utf-8 -*-

"""
CTYUN客户控制台,域名接口

"""

import json
import time
import allure
import pytest
import random
from bin.Init import Init
from bin.unit.Rondom import random_string
from bin.createDomain import CreateDomain

public_key_365 = Init.PUBLIC_KEY
private_key_365 = Init.PRIVATE_KEY
public_key_expire = Init.PUBLIC_KEY_EXPIRE
private_key_expire = Init.PRIVATE_KEY_EXPIRE
headers_json = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/json",
}
headers_form = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                      Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}


@allure.feature("CTYUN客户控制台-域名管理模块")
class TestDomain():

    def setup_class(self):
        print('test start')
        self.base_info = Init.BASE_INFO
        self.domain_info = Init.DOMAIN_INFO
        self.session = Init.CTYUN_SESSION
        # self.bs_session = Init.BS_SESSION
        self.console_host = self.base_info['ctyunHost']
        self.workspace_id = self.base_info['ctyun_workspaceid']
        self.workorder_host = self.base_info['workOrderHost']
        self.createDomain = CreateDomain()

    def teardown_class(self):
        # 清理数据，退出登录等
        print('-------------------test end-------------------')

    @pytest.mark.skip(reason="调试")  # 跳过该测试
    @allure.story('CDN客户控制台域名测试，从随机新增--停用--删除')
    def test_CDN_240819(self):
        random_info = self.createDomain.generate_randomDomain()
        createdomain_url = self.console_host + self.domain_info['createDomain']
        verifydomain_url = self.console_host + self.domain_info['verifyDomain']
        # list_url = console_host + self.domain_info['listDomain']
        # search_url = workOrder_host + self.domain_info['getOrder_id']
        # deal_url = workOrder_host + self.domain_info['dealOrder']
        change_status = self.console_host + self.domain_info['changeDomain']
        check_domain_url = self.console_host + self.domain_info['detailDomain']
        domain = random_info['data']['domain']
        check_domain_data = 'workspaceId=' + self.workspace_id + '&domain=' + domain + ''
        print(check_domain_url)
        print(domain)

        # 创建域名
        verify_response = self.session.get(verifydomain_url, params=check_domain_data,verify=False)
        createdomain_response = self.session.post(createdomain_url, json=random_info, verify=False)
        print(createdomain_response.text)
        print("-------------------验证域名是否备案-------------------")
        print('请求url: ' + str(verifydomain_url))
        print("请求data: " + str(check_domain_data))
        print("返回： " + str(verify_response.text))
        print("重点验证："  "  expect： 返回备案名称和record_status")

        print("-------------------创建域名-------------------")
        print('请求url: ' + str(createdomain_url))
        print("请求data: " + str(random_info))
        print("返回： " + str(createdomain_response.text))
        print("重点验证：" + domain + "  expect： 返回创建成功")

        time.sleep(2)
        check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,verify=False)
        body = json.loads(check_response1.text)
        product_code = body['data']['product_code']
        status_code = body['data']['status']

        print("-------------------控制台查询域名状态-------------------")
        print('请求url: ' + str(check_domain_url))
        print("请求data: " + str(check_domain_data))
        print(
            '接口返回值： ' + str(createdomain_response.text) + '  接口耗时：' + str(createdomain_response.elapsed.microseconds))
        print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
        assert status_code == '3'
        # assert createDomain_response.elapsed.microseconds < 3000

        # 工单系统查询域名--提交域名使得域名新增成功
        # workerOrder_deal(domain)
        time.sleep(2)
        check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)
        print('body: ', check_response2.text)
        status_code2 = json.loads(check_response2.text)['data']['status']
        print(status_code2)
        print("-------------------工单系统处理完域名，然后去控制台查询域名状态-------------------")
        print('业务管理平台分配承载平台，工单系统处理域名均封装，这里不返回信息了')
        print('请求方式：get' + '请求URL：' + check_domain_url)
        print('请求参数：' + str(check_domain_data))
        print('接口返回值： ' + str(check_response2.text) + '  接口耗时：' + str(check_response2.elapsed.microseconds))
        print('重点验证：status_code=' + str(status_code2) + "  expect: 4 已启用")
        assert status_code2 == '4'
        '''
        """
        # 控制台操作停用域名
        https: // iam - test.ctcdn.cn / cdn / gw / domain / ChangeDomainStatus?workspaceId = 10003885 & domain = Auto - random - 40
        Da.ctyun.cn & status = 2 & domainStatus = 4 & businessType = 001 & _t = 1599107868896

        """
        # 停用域名
        stop_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=2&domainStatus=4&businessType=' + product_code
        stopDomain_response = self.session.get(url=change_status, params=stop_data, verify=False)
        time.sleep(2)
        print("-------------------控制台发起域名停用-------------------")
        print('请求方式：get' + '请求URL：' + change_status)
        print('请求参数：' + stop_data)
        print(
            '接口返回值： ' + str(stopDomain_response.text) + '  接口耗时：' + str(stopDomain_response.elapsed.microseconds))
        # 查询域名状态，应该是5
        check_response5 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)
        status_code5 = json.loads(check_response5.text)['data']['status']
        print("-------------------控制台查询域名状态-------------------")
        print('请求url: ' + str(check_domain_url))
        print("请求data: " + str(check_domain_data))
        print(
            '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
        print('重点验证：status_code=' + str(status_code5) + "  expect:  5 停止中")

        assert status_code5 == '5'
        # 工单系统停用
        workOrder_stopDomain(domain)
        time.sleep(2)
        # 去控制台查询该域名状态，应该是6
        check_response3 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)

        print("-------------------工单系统停用后，控制台查询域名状态-------------------")
        print('body: ', check_response3.text)
        status_code3 = json.loads(check_response3.text)['data']['status']
        print('工单系统处理后，停用域名，再查域名状态')
        print('重点验证：status_code=' + status_code3 + "  expect: 6 已停止")

        # 控制台操作删除域名
        del_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=1&domainStatus=6&businessType=' + product_code + ''
        delDomain_response = self.session.get(url=change_status, params=del_data, verify=False)
        print('删除域名返回：', delDomain_response.text)
        time.sleep(2)
        # 查询域名状态，应该是7
        check_response7 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)
        print("-------------------控制台发起域名删除，然后查询该域名状态-------------------")
        status_code7 = json.loads(check_response7.text)['data']['status']
        print(status_code7)
        print('请求方式：get' + '请求URL：' + change_status)
        print('请求参数：' + str(del_data))
        print('接口返回值： ' + str(delDomain_response.text) + '  接口耗时：' + str(delDomain_response.elapsed.microseconds))
        print('重点验证：status_code=' + status_code7 + "  expect: 7 删除中")

        # 工单系统删除
        workOrder_stopDomain(domain)
        time.sleep(2)
        # 去控制台查询该域名状态，应该没有域名了
        check_response4 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)
        print("-------------------工单系统删除之后，控制台查询域名-------------------")
        print('body: ', check_response4.text)
        print('工单系统处理后，删除域名，再查域名状态')
        print('重点验证：返回无权访问，域名已经删除 ' + str(check_response4.text) + "  expect: 未授权的访问,用户不具备权限:do c_domain ")
        assert '没有找到当前域名信息' in check_response4.text

    '''"""
        由于目前域名全是自动分配承载平台，该流程已经跑不通
    """
    '''
    '''

    @pytest.mark.skip(reason="调试")  # 跳过该测试
    # @pytest.mark.repeat(10)
    @allure.story('CDN客户控制台域名测试，只是新增')
    def test_CDN_123456(self):
        console_host = self.base_info['ctyunHost']
        workspace_id = self.base_info['ctyun_workspaceid']
        random_info = self.createDomain.generate_randomDomain()
        domain = random_info['data']['domain']
        createDomain_url = console_host + self.domain_info['createDomain']
        verifyDomain_url = console_host + self.domain_info['verifyDomain']
        check_domain_url = console_host + self.domain_info['detailDomain']
        verify_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
        check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
        print(check_domain_url)
        print(domain)

        # 创建域名
        print('创建域名')
        print('请求方式：post' + '请求URL：' + createDomain_url)
        print('请求参数：' + str(random_info))
        self.session.get(url=verifyDomain_url, params=verify_domain_data, headers=headers_form, verify=False,
                         timeout=10)
        createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
                                                  verify=False, timeout=10)
        print("返回：", createDomain_response.text)
        time.sleep(2)
        check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False, timeout=10)
        print('body: ', check_response1.text)
        body = json.loads(check_response1.text)
        product_code = body['data']['product_code']
        print(product_code)
        status_code = body['data']['status']
        print(status_code)
        print(
            '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
        print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
        assert status_code == '3'
