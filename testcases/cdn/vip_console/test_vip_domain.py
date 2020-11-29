# -*- coding: utf-8 -*-
import allure
from bin.Workorder import *
from bin.createDomain import CreateDomain
from bin.Init import Init
from bin.createLogData import CreateLogData
from bin.unit.Assert import Assert
import pytest
import time

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

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEzfQ.zWkVj5oehTUt9l0_O3i_o1i4wtoo7Aj21j0HWVD95bs"
}

header_post = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEzfQ.zWkVj5oehTUt9l0_O3i_o1i4wtoo7Aj21j0HWVD95bs"
}
'''
1.域名状态:  1.审核中2.审核成功3.配置中4.已启用5.停止中6.已停止7.删除中8.已删除9.审核失败10.配置失败
            11.停止失败12.删除失败 -- 状态合并，保留3-"配置中， 4-"已启用"、5-“停止中”，6-“已停止”、 7-"删除中"

2.前提：  客户状态分为自助（不经过业务管理平台）， 非自助   【工单系统可以配置】
         自助的域名目前支持：视频直播加速 产品 005

3. 备案处于需求变更期，等稳定了再调整
'''


@allure.feature('域名流程测试')
class Test_Vip_Domain():

    def setup_class(self):
        print('test start')
        self.base_info = Init.BASE_INFO
        self.domain_info = Init.DOMAIN_INFO
        self.createDomain = CreateDomain()
        self.assert_common = Assert()
        self.session = Init.CONSOLE_SESSION
        self.bs_session = Init.BS_SESSION
        console_host = self.base_info['host']
        workspace_id = self.base_info['workspaceid']
        self.verifyDomain_url = console_host + self.domain_info['verifyDomain']
        self.check_domain_url = console_host + self.domain_info['detailDomain']
        self.domain_list = CreateLogData().get_domain_list()
        # self.order_list = createOrderData(self.session, console_host, workspace_id).order_domainlist()
        # self.order = createOrderData(self.session, console_host, workspace_id)

    def teardown_class(self):
        # 做清数据，退出登录等
        self.session.close()
        print('test end')

    @pytest.mark.skipif(Init.ENV == 'PE',
                        reason="线上环境无法执行")
    # @pytest.mark.repeat(10)
    @allure.story('CDN客户控制台域名测试，从随机新增--停用--删除')
    def test_Domain_Flow(self):
        """
                工单状态： 2- 进行中 3- 成功  4- 失败
                :return:
                """
        console_host = self.base_info['host']
        workspace_id = self.base_info['workspaceid']
        random_info = self.createDomain.generate_randomDomain()
        createDomain_url = console_host + self.domain_info['createDomain']
        check_domain_url = console_host + self.domain_info['detailDomain']
        domain = random_info['data']['domain']
        productcode = random_info['data']['productCode']
        change_status = console_host + self.domain_info['changeDomain']
        check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''

        # 创建域名
        self.session.get(url=self.verifyDomain_url, params=check_domain_data, headers=headers_form, verify=False,
                         timeout=10)
        createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
                                                  verify=False, timeout=10)
        print(domain)
        print("-------------------------创建 域名 ----------------------------")
        print('请求方式：post' + '请求URL：' + createDomain_url)
        print("请求数据： " + str(random_info))
        print('domain: ' + domain + '   product_code: ' + productcode)
        print("接口返回： " + createDomain_response.text)

        # 域名列表里面无该域名，工单列表有新增域名工单生成
        assert domain not in self.domain_list
        time.sleep(3)
        # assert domain in self.order_list

        # 工单系统处理，配置成功
        deal_new_domain(domain, "3")
        time.sleep(2)
        # 控制台核对下域名状态和其他
        checkDomain_response = self.session.post(url=check_domain_url, data=check_domain_data, headers=headers_form,
                                                 verify=False, timeout=10)
        print("-------------------------验证 域名 ----------------------------")
        print('请求方式：post' + '请求URL：' + str(check_domain_url))
        print('请求参数：' + str(check_domain_data))
        print('返回： ' + checkDomain_response.text)
        check_content = json.loads(checkDomain_response.text)
        assert str(check_content['data']['status']) == '4'  # 表示域名已启用
        assert 'core.ok' in checkDomain_response.text
        assert '服务调用成功' in checkDomain_response.text

        # 停用域名
        stop_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=2&domainStatus=4&businessType=' + productcode
        stopDomain_response = self.session.get(url=change_status, params=stop_data, verify=False)
        time.sleep(2)
        print("-------------------控制台发起域名停用-------------------")
        print('请求方式：get' + '请求URL：' + change_status)
        print('请求参数：' + str(stop_data))
        print('接口返回值： ' + str(stopDomain_response.text))
        # 验证停用

        # 停用工单通过
        time.sleep(3)
        workOrder_Flow_Domain(domain)
        time.sleep(3)

        # 删除域名
        del_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=1&domainStatus=6&businessType=' + productcode + ''
        delDomain_response = self.session.get(url=change_status, params=del_data, verify=False)
        print('删除域名返回：', delDomain_response.text)
        time.sleep(2)
        workOrder_Flow_Domain(domain)
        time.sleep(3)
        # 查询域名
        check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
                                           verify=False)
        print("-------------------工单系统删除之后，控制台查询域名-------------------")
        print('请求方式：get' + '请求URL：' + check_domain_url)
        print('请求参数：' + str(check_domain_data))
        print('重点验证：返回无权访问，域名已经删除 ' + str(check_response2.text) + "  expect: 未授权的访问,用户不具备权限:do c_domain ")
        assert '未授权的访问' in check_response2.text
        assert '用户不具备权限' in check_response2.text
        assert domain in check_response2.text

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    @pytest.mark.skipif(Init.ENV == 'PE',
                        reason="线上环境无法执行")
    # @pytest.mark.repeat(50)
    @allure.story('域名从创建---工单系统配置失败---重新发起---配置成功---域名启用')
    def test_failed_domain(self):
        """
        工单状态： 2- 进行中 3- 成功  4- 失败
        :return:
        """
        console_host = self.base_info['host']
        workspace_id = self.base_info['workspaceid']
        random_info = self.createDomain.generate_randomDomain()
        createDomain_url = console_host + self.domain_info['createDomain']
        check_domain_url = console_host + self.domain_info['detailDomain']
        domain = random_info['data']['domain']
        productcode = random_info['data']['productCode']
        check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''

        # 创建域名
        self.session.get(url=self.verifyDomain_url, params=check_domain_data, headers=headers_form, verify=False,
                         timeout=10)
        createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
                                                  verify=False, timeout=10)
        print(domain)
        print("-------------------------创建 域名 ----------------------------")
        print('请求方式：post' + '请求URL：' + createDomain_url)
        print("请求数据： " + str(random_info))
        print("接口返回： " + createDomain_response.text)

        # 域名列表里面无该域名，工单列表有新增域名工单生成
        assert domain not in self.domain_list
        time.sleep(3)
        # assert domain in self.order_list

        # 工单系统处理，配置失败
        deal_new_domain(domain, "4")

        # 去控制台验证
        assert domain not in self.domain_list  # 配置失败的域名不会出现在域名列表
        order_url = self.domain_info["orderDetail"]
        order_id = self.order.get_OrderId(domain)
        order_payload = {
            "workspaceId": workspace_id,
            "orderId": order_id
        }
        order_response = self.session.get(console_host + order_url, params=order_payload, headers=headers_form,
                                          verify=False, timeout=10)
        print("-------------------查看 OrderDetail 接口-------------------")
        print('请求url: ' + str(console_host + order_url))
        print("请求data: " + str(order_payload))
        print("返回： " + order_response.text)
        print("重点验证："  " expect： 返回值中有工单id")
        content = json.loads(order_response.text)
        status = content['data']['status']
        assert status == "4"
        # 重新发起
        renew_domainInfo = self.createDomain.renew_domain(domain, productcode)
        createDomain_response2 = self.session.post(url=createDomain_url, json=renew_domainInfo, headers=headers_json,
                                                   verify=False, timeout=10)
        print("-------------------------创建 域名 ----------------------------")
        print('请求方式：post' + '请求URL：' + createDomain_url)
        print('请求参数：' + str(renew_domainInfo))
        print('返回： ' + createDomain_response2.text)

        # 工单系统处理，配置成功
        time.sleep(3)
        deal_new_domain(domain, "3")
        # assert domain in self.domain_list
        time.sleep(2)
        # 控制台核对下域名状态和其他
        checkDomain_response = self.session.post(url=check_domain_url, data=check_domain_data, headers=headers_form,
                                                 verify=False, timeout=10)
        print("-------------------------验证 域名 ----------------------------")
        print('请求方式：post' + '请求URL：' + str(check_domain_url))
        print('请求参数：' + str(check_domain_data))
        print('返回： ' + checkDomain_response.text)
        check_content = json.loads(checkDomain_response.text)
        assert str(check_content['data']['status']) == '4'  # 表示域名已启用
        assert 'core.ok' in checkDomain_response.text
        assert '服务调用成功' in checkDomain_response.text

    # @pytest.mark.skip(reason="调试")  # 跳过该测试
    # @pytest.mark.repeat(3)
    @allure.story('CDN客户控制台域名测试，只是新增')
    def test_CDN_240824(self):
        console_host = self.base_info['host']
        workspace_id = self.base_info['workspaceid']
        random_info = self.createDomain.generate_randomDomain()
        domain = random_info['data']['domain']
        productcode = random_info['data']['productCode']
        createDomain_url = console_host + self.domain_info['createDomain']
        verifyDomain_url = console_host + self.domain_info['verifyDomain']
        check_domain_url = console_host + self.domain_info['detailDomain']
        verify_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
        check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''

        # 备案域名+创建域名
        self.session.get(url=verifyDomain_url, params=verify_domain_data, headers=headers_form, verify=False,
                         timeout=10)
        createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
                                                  verify=False, timeout=10)
        print('-------------------------创建域名-------------------------')
        print('请求方式：post' + '请求URL：' + createDomain_url)
        print('domain: ' + domain + '   product_code: ' + productcode)
        print('请求参数：' + str(random_info))
        print("返回：", createDomain_response.text)
        time.sleep(2)
        check_response = self.session.get(url=check_domain_url, params=check_domain_data,
                                          verify=False, timeout=10)
        print('-------------------------验证域名生成域名工单-------------------------')
        print('请求方式：post' + '请求URL：' + check_domain_url)
        print('请求参数：' + str(check_domain_data))
        print("返回：", check_response.text)
        assert domain in check_response.text
        assert '服务调用成功' in check_response.text
