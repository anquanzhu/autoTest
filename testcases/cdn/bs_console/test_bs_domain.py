# # -*- coding: utf-8 -*-
# import allure
# from bin.Workorder import *
# from bin.createDomain import CreateDomain
# from bin.Init import Init
# from bin.unit.Assert import Assert
# import pytest
# import time
#
# headers_json = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
#                                   Chrome/67.0.3396.99 Safari/537.36",
#     "Content-Type": "application/json",
# }
# headers_form = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
#                       Chrome/67.0.3396.99 Safari/537.36",
#     "Content-Type": "application/x-www-form-urlencoded",
# }
#
# header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
#                           Chrome/67.0.3396.99 Safari/537.36",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEzfQ.zWkVj5oehTUt9l0_O3i_o1i4wtoo7Aj21j0HWVD95bs"
# }
#
# header_post = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
#                           Chrome/67.0.3396.99 Safari/537.36",
#     "Content-Type": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEzfQ.zWkVj5oehTUt9l0_O3i_o1i4wtoo7Aj21j0HWVD95bs"
# }
# '''
# 1.域名状态:  1.审核中2.审核成功3.配置中4.已启用5.停止中6.已停止7.删除中8.已删除9.审核失败10.配置失败
#             11.停止失败12.删除失败 -- 状态合并，保留3-"配置中， 4-"已启用"、5-“停止中”，6-“已停止”、 7-"删除中"
#
# 2.前提：  客户状态分为自助（不经过业务管理平台）， 非自助   【工单系统可以配置】
#          自助的域名目前支持：视频直播加速 产品 005
#
# 3. 备案处于需求变更期，等稳定了再调整
# '''
#
#
# @allure.feature('BS域名流程测试')
# class Test_BS_Domain():
#     # def setup(self):
#     #     print("setup: 每个用例开始前执行")
#     #
#     # def teardown(self):
#     #     print("teardown: 每个用例结束后执行")
#
#     def setup_class(self):
#         print('test start')
#         self.base_info = Init.BASE_INFO
#         self.domain_info = Init.DOMAIN_INFO
#         self.createDomain = CreateDomain()
#         self.assert_common = Assert()
#         self.session = Init.BS_SESSION
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         self.verifyDomain_url = console_host + self.domain_info['verifyDomain']
#         self.check_domain_url = console_host + self.domain_info['detailDomain']
#         # self.verify_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#
#     def teardown_class(self):
#         # 做清数据，退出登录等
#         print('test end')
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     # @pytest.mark.repeat(10)
#     @allure.story('CDN客户控制台域名测试，从随机新增--停用--删除')
#     def test_Domain_Flow(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         workOrder_host = self.base_info['workOrderHost']
#         random_info = self.createDomain.generate_randomDomain()
#         createDomain_url = console_host + self.domain_info['createDomain']
#         # list_url = console_host + self.domain_info['listDomain']
#         # search_url = workOrder_host + self.domain_info['getOrder_id']
#         # deal_url = workOrder_host + self.domain_info['dealOrder']
#         change_status = console_host + self.domain_info['changeDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         domain = random_info['data']['domain']
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#         print(check_domain_url)
#         print(domain)
#
#         # 创建域名
#
#         verify_response = self.session.get(url=self.verifyDomain_url, params=check_domain_data, headers=headers_form,
#                                            verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(createDomain_response.text)
#         print("-------------------验证域名是否备案-------------------")
#         print('请求url: ' + str(self.verifyDomain_url))
#         print("请求data: " + str(check_domain_data))
#         print("返回： " + str(verify_response.text))
#         print("重点验证："  "  expect： 返回备案名称和record_status")
#
#         print("-------------------创建域名-------------------")
#         print('请求url: ' + str(createDomain_url))
#         print("请求data: " + str(random_info))
#         print("返回： " + str(createDomain_response.text))
#         print("重点验证：" + domain + "  expect： 返回创建成功")
#
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         status_code = body['data']['status']
#
#         print("-------------------控制台查询域名状态-------------------")
#         print('请求url: ' + str(check_domain_url))
#         print("请求data: " + str(check_domain_data))
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#         # assert createDomain_response.elapsed.microseconds < 3000
#
#         # 工单系统查询域名--提交域名使得域名新增成功
#         workerOrder_deal(domain)
#         time.sleep(2)
#         check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response2.text)
#         status_code2 = json.loads(check_response2.text)['data']['status']
#         print(status_code2)
#         print("-------------------工单系统处理完域名，然后去控制台查询域名状态-------------------")
#         print('业务管理平台分配承载平台，工单系统处理域名均封装，这里不返回信息了')
#         print('请求方式：get' + '请求URL：' + check_domain_url)
#         print('请求参数：' + str(check_domain_data))
#         print('接口返回值： ' + str(check_response2.text) + '  接口耗时：' + str(check_response2.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code2) + "  expect: 4 已启用")
#         assert status_code2 == '4'
#
#         '''
#         # 控制台操作停用域名
#         https: // iam - test.ctcdn.cn / cdn / gw / domain / ChangeDomainStatus?workspaceId = 10003885 & domain = Auto - random - 40
#         Da.ctyun.cn & status = 2 & domainStatus = 4 & businessType = 001 & _t = 1599107868896
#
#         '''
#         # 停用域名
#         stop_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=2&domainStatus=4&businessType=' + product_code
#         stopDomain_response = self.session.get(url=change_status, params=stop_data, verify=False)
#         time.sleep(2)
#         print("-------------------控制台发起域名停用-------------------")
#         print('请求方式：get' + '请求URL：' + change_status)
#         print('请求参数：' + stop_data)
#         print(
#             '接口返回值： ' + str(stopDomain_response.text) + '  接口耗时：' + str(stopDomain_response.elapsed.microseconds))
#         # 查询域名状态，应该是5
#         check_response5 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         status_code5 = json.loads(check_response5.text)['data']['status']
#         print("-------------------控制台查询域名状态-------------------")
#         print('请求url: ' + str(check_domain_url))
#         print("请求data: " + str(check_domain_data))
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code5) + "  expect:  5 停止中")
#
#         assert status_code5 == '5'
#         # 工单系统停用
#         workOrder_stopDomain(domain)
#         time.sleep(2)
#         # 去控制台查询该域名状态，应该是6
#         check_response3 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#
#         print("-------------------工单系统停用后，控制台查询域名状态-------------------")
#         print('body: ', check_response3.text)
#         status_code3 = json.loads(check_response3.text)['data']['status']
#         print('工单系统处理后，停用域名，再查域名状态')
#         print('重点验证：status_code=' + status_code3 + "  expect: 6 已停止")
#
#         # 控制台操作删除域名
#         del_data = 'workspaceId=' + workspace_id + '&domain=' + domain + '&status=1&domainStatus=6&businessType=' + product_code + ''
#         delDomain_response = self.session.get(url=change_status, params=del_data, verify=False)
#         print('删除域名返回：', delDomain_response.text)
#         time.sleep(2)
#         # 查询域名状态，应该是7
#         check_response7 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print("-------------------控制台发起域名删除，然后查询该域名状态-------------------")
#         status_code7 = json.loads(check_response7.text)['data']['status']
#         print(status_code7)
#         print('请求方式：get' + '请求URL：' + change_status)
#         print('请求参数：' + str(del_data))
#         print('接口返回值： ' + str(delDomain_response.text) + '  接口耗时：' + str(delDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + status_code7 + "  expect: 7 删除中")
#
#         # 工单系统删除
#         workOrder_stopDomain(domain)
#         time.sleep(2)
#         # 去控制台查询该域名状态，应该没有域名了
#         check_response4 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print("-------------------工单系统删除之后，控制台查询域名-------------------")
#         print('body: ', check_response4.text)
#         print('工单系统处理后，删除域名，再查域名状态')
#         print('重点验证：返回无权访问，域名已经删除 ' + str(check_response4.text) + "  expect: 未授权的访问,用户不具备权限:do c_domain ")
#         assert '没有找到当前域名信息' in check_response4.text
#
#     '''
#         由于目前域名全是自动分配承载平台，该流程已经跑不通
#     '''
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     @allure.story('域名从创建到业务平台结单处理流程')
#     def test_end_domain(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         random_info = self.createDomain.generate_randomDomain()
#         createDomain_url = console_host + self.domain_info['createDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         domain = random_info['data']['domain']
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#
#         # 创建域名
#         print('创建域名')
#         print('请求方式：post' + '请求URL：' + createDomain_url)
#         print('请求参数：' + str(random_info))
#         self.session.get(url=self.verifyDomain_url, params=self.verify_domain_data, headers=headers_form, verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(domain)
#         print(createDomain_response.text)
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response1.text)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         print(product_code)
#         status_code = body['data']['status']
#         print(status_code)
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#
#         # 业务平台处理单子并结单
#         time.sleep(3)
#         id = bs_workOrder_id(domain)
#         bs_end_domain(id)
#
#         # 去控制台查询该域名状态，应该没有域名了
#         time.sleep(3)
#         check_response = self.session.get(url=check_domain_url, params=check_domain_data,
#                                           verify=False)
#         print('body: ', check_response.text)
#         print('业务管理平台结单后，再查域名状态')
#         print('重点验证：返回无权访问，域名已经删除 ' + str(check_response.text) + "  expect: 未授权的访问,用户不具备权限:do c_domain ")
#         # assert '未授权的访问' in check_response.text
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     # @pytest.mark.repeat(50)
#     @allure.story('域名从创建---工单系统配置失败')
#     def test_failed_domain(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         random_info = self.createDomain.generate_randomDomain()
#         createDomain_url = console_host + self.domain_info['createDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         domain = random_info['data']['domain']
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#
#         # 创建域名
#         print('创建域名')
#         print('请求方式：post' + '请求URL：' + createDomain_url)
#         print('请求参数：' + str(random_info))
#         self.session.get(url=self.verifyDomain_url, params=self.verify_domain_data, headers=headers_form, verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(domain)
#         print(createDomain_response.text)
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response1.text)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         print(product_code)
#         status_code = body['data']['status']
#         print(status_code)
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#
#         # 工单系统处理，配置失败
#         time.sleep(3)
#         workerOrder_failed(domain)
#         # 去控制台查询该域名状态，应该没有域名了
#         time.sleep(2)
#         check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response2.text)
#         body = json.loads(check_response2.text)
#         status_code2 = body['data']['status']
#         print(status_code2)
#         print('重点验证：status_code=' + str(status_code) + "  expect: 10 配置失败")
#         assert status_code2 == '10'
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     # @pytest.mark.repeat(10)
#     @allure.story('CDN客户控制台域名测试，只是新增')
#     def test_createDomain(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         random_info = self.createDomain.generate_workDomain()
#         domain = random_info['data']['domain']
#         createDomain_url = console_host + self.domain_info['createDomain']
#         verifyDomain_url = console_host + self.domain_info['verifyDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         verify_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#         print(check_domain_url)
#         print(domain)
#
#         # 创建域名
#         print('创建域名')
#         print('请求方式：post' + '请求URL：' + createDomain_url)
#         print('请求参数：' + str(random_info))
#         self.session.get(url=verifyDomain_url, params=verify_domain_data, headers=headers_form, verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(createDomain_response.text)
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response1.text)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         print(product_code)
#         status_code = body['data']['status']
#         print(status_code)
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     # @pytest.mark.repeat(50)
#     @allure.story('CDN客户控制台域名测试，从新增--编辑--启用成功')
#     def test_Domain_editFlow(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         random_info = self.createDomain.generate_randomDomain()
#         createDomain_url = console_host + self.domain_info['createDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         domain = random_info['data']['domain']
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#         productCode = random_info['data']['productCode']
#         print(check_domain_url)
#         print(domain)
#
#         # 创建域名
#         print('创建域名')
#         print('请求方式：post' + '请求URL：' + createDomain_url)
#         print('请求参数：' + str(random_info))
#         # 创建域名之前先验证域名是否备案
#         self.session.get(url=self.verifyDomain_url, params=check_domain_data, headers=headers_form, verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(createDomain_response.text)
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response1.text)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         print(product_code)
#         status_code = body['data']['status']
#         print(status_code)
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#         # assert createDomain_response.elapsed.microseconds < 3000
#
#         # 工单系统查询域名--提交域名使得域名新增成功
#         workerOrder_deal(domain)
#         time.sleep(2)
#         check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response2.text)
#         status_code2 = json.loads(check_response2.text)['data']['status']
#         print(status_code2)
#         print('工单系统处理域名后，启用域名，途径业务管理平台')
#         print('请求方式：get' + '请求URL：' + check_domain_url)
#         print('请求参数：' + str(check_domain_data))
#         print('接口返回值： ' + str(check_response2.text) + '  接口耗时：' + str(check_response2.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code2) + "  expect: 4 已启用")
#         assert status_code2 == '4'
#
#         # 编辑域名
#         if product_code == '005':
#             domain_type = random_info['data']['liveConf']['domainType']
#             if domain_type == '2':
#                 edit_data = {
#                     "data": {
#                         "workspaceId": self.workspace_id,
#                         "action": 1,
#                         "domain": domain,
#                         "productCode": "005",
#                         "liveConf": {
#                             "mode": 1,
#                             "multiProtocol": 0,
#                             "protocolType": 2,
#                             "domainType": 2,
#                             "publishPoint": "live,app,edit_Auto"
#                         },
#                         "originProtocol": "http",
#                         "origin": [
#                             {
#                                 "origin": "",
#                                 "port": 1935,
#                                 "role": "master",
#                                 "weight": 1
#                             }
#                         ]
#                     }
#                 }
#             else:
#                 edit_data = {
#                     "data": {
#                         "workspaceId": self.workspace_id,
#                         "action": 1,
#                         "domain": domain,
#                         "recordNum": "京ICP备12022551号",
#                         "productCode": "005",
#                         "liveConf": {
#                             "mode": 1,
#                             "multiProtocol": 1,
#                             "protocolType": 2,
#                             "domainType": 1,
#                             "publishPoint": "live,pull,edit_Auto",
#                             "relatedDomain": "Auto-random-0f6C.ctyun.cn"
#                         },
#                         "httpsPublicContent": Init.PUBLIC_KEY,
#                         "httpsPrivateKey": Init.PRIVATE_KEY,
#                         "certName": "CTYUN_TEST",
#                         "pathTtl": [
#                             {
#                                 "path": "/test/4",
#                                 "ttl": 80,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             }
#                         ],
#                         "filetypeTtl": [
#                             {
#                                 "fileType": "m3u8",
#                                 "ttl": 0,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             },
#                             {
#                                 "fileType": "ts",
#                                 "ttl": 86400,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             }
#                         ],
#                         "ipWhiteList": "127.0.0.3",
#                         "userAgent": {
#                             "type": 0,
#                             "ua": [
#                                 "curl*",
#                                 "*IE"
#                             ]
#                         },
#                         "whiteReferer": {
#                             "allowList": [
#                                 "*.demo.com"
#                             ],
#                             "allowEmpty": "on"
#                         },
#                         "originProtocol": "http",
#                         "origin": [
#                             {
#                                 "origin": "",
#                                 "port": 1935,
#                                 "role": "master",
#                                 "weight": 1
#                             }
#                         ]
#                     }
#                 }
#         else:
#             certName = random_info['data']['certName']
#             public = random_info['data']['httpsPublicContent']
#             private = random_info['data']['httpsPrivateKey']
#             edit_data = {
#                 "data": {
#                     "workspaceId": self.workspace_id,
#                     "action": 1,
#                     "domain": domain,
#                     "productCode": productCode,
#                     "origin": [
#                         {
#                             "role": "master",
#                             "origin": "192.255.0.5",
#                             "port": 10086,  # 修改回源端口
#                             "weight": 1
#                         },
#                         {
#                             "role": "slave",
#                             "origin": "gg.ctyun.cn",
#                             "port": 80,
#                             "weight": 1
#                         }
#                     ],
#                     "originProtocol": "http",
#                     "basicConf": {
#                         "follow302": 0
#                     },
#                     "reqHost": "edit.ctyun.cn",  # 回源Host
#                     "httpsPublicContent": public,
#                     "httpsPrivateKey": private,
#                     "certName": certName,
#                     "pathTtl": [
#                         {
#                             "path": "/test/a",
#                             "ttl": 80,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         }
#                     ],
#                     "filetypeTtl": [
#                         {
#                             "fileType": "php,ashx,aspx,asp,jsp,do",
#                             "ttl": 0,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "js,css,xml,htm,html",
#                             "ttl": 1800,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "jpg,gif,png,bmp,ico,swf,ts,test1,test2",
#                             "ttl": 86400,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
#                             "ttl": 31536000,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         }
#                     ],
#                     "ipWhiteList": "199.231.0.5",
#                     "userAgent": {
#                         "type": 0,
#                         "ua": [
#                             "gg.ctyun.cn"
#                         ]
#                     },
#                     "whiteReferer": {
#                         "allowList": [
#                             "gg.ctyun.cn"
#                         ],
#                         "allowEmpty": "on"
#                     }
#                 }
#             }
#         edit_response = self.session.post(url=createDomain_url, json=edit_data, headers=headers_json,
#                                           verify=False)
#         print('eidt body: ', edit_response.text)
#
#         # 编辑后查询域名状态
#         time.sleep(2)
#         check_response3 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response3.text)
#         body = json.loads(check_response3.text)
#         status_code3 = body['data']['status']
#         print(status_code3)
#         print(
#             '接口返回值： ' + str(check_response3.text) + '  接口耗时：' + str(check_response3.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code3) + "  expect: 3 配置中")
#         assert status_code3 == '3'
#
#         # 工单系统查询域名--提交域名使得域名编辑成功
#         workerOrder_deal(domain)
#         time.sleep(2)
#         check_response4 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response4.text)
#         status_code4 = json.loads(check_response4.text)['data']['status']
#         print(status_code4)
#         print('工单系统处理域名后，启用域名，编辑域名完成')
#         print('请求方式：get' + '请求URL：' + check_domain_url)
#         print('请求参数：' + str(check_domain_data))
#         print('接口返回值： ' + str(check_response4.text) + '  接口耗时：' + str(check_response4.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code4) + "  expect: 4 已启用")
#         assert status_code4 == '4'
#
#     @pytest.mark.skip(reason="调试")  # 跳过该测试
#     # @pytest.mark.repeat(50)
#     @allure.story('CDN客户控制台域名测试，从新增--编辑--工单系统打回---控制台查看结果')
#     def test_Domain_Edit_Faild(self):
#         console_host = self.base_info['bsHost']
#         workspace_id = self.base_info['ctyunAcctId']
#         workOrder_host = self.base_info['workOrderHost']
#         random_info = self.createDomain.generate_randomDomain()
#         createDomain_url = console_host + self.domain_info['createDomain']
#         check_domain_url = console_host + self.domain_info['detailDomain']
#         domain = random_info['data']['domain']
#         check_domain_data = 'workspaceId=' + workspace_id + '&domain=' + domain + ''
#         productCode = random_info['data']['productCode']
#         print(check_domain_url)
#         print(domain)
#
#         # 创建域名
#         print('创建域名')
#         print('请求方式：post' + '请求URL：' + createDomain_url)
#         print('请求参数：' + str(random_info))
#         self.session.get(url=self.verifyDomain_url, params=self.verify_domain_data, headers=headers_form, verify=False)
#         createDomain_response = self.session.post(url=createDomain_url, json=random_info, headers=headers_json,
#                                                   verify=False)
#         print(createDomain_response.text)
#         time.sleep(2)
#         check_response1 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response1.text)
#         body = json.loads(check_response1.text)
#         product_code = body['data']['product_code']
#         print(product_code)
#         status_code = body['data']['status']
#         print(status_code)
#         print(
#             '接口返回值： ' + str(createDomain_response.text) + '  接口耗时：' + str(
#                 createDomain_response.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code) + "  expect: 3 配置中")
#         assert status_code == '3'
#         # assert createDomain_response.elapsed.microseconds < 3000
#
#         # 工单系统查询域名--提交域名使得域名新增成功
#         workerOrder_deal(domain)
#         time.sleep(2)
#         check_response2 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response2.text)
#         status_code2 = json.loads(check_response2.text)['data']['status']
#         print(status_code2)
#         print('工单系统处理域名后，启用域名，途径业务管理平台')
#         print('请求方式：get' + '请求URL：' + check_domain_url)
#         print('请求参数：' + str(check_domain_data))
#         print('接口返回值： ' + str(check_response2.text) + '  接口耗时：' + str(check_response2.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code2) + "  expect: 4 已启用")
#         assert status_code2 == '4'
#
#         # 编辑域名
#         if product_code == '005':
#             domain_type = random_info['data']['liveConf']['domainType']
#             if domain_type == '2':
#                 edit_data = {
#                     "data": {
#                         "workspaceId": self.workspace_id,
#                         "action": 1,
#                         "domain": domain,
#                         "productCode": "005",
#                         "liveConf": {
#                             "mode": 1,
#                             "multiProtocol": 0,
#                             "protocolType": 2,
#                             "domainType": 2,
#                             "publishPoint": "live,app,edit_Auto"
#                         },
#                         "originProtocol": "http",
#                         "origin": [
#                             {
#                                 "origin": "",
#                                 "port": 1935,
#                                 "role": "master",
#                                 "weight": 1
#                             }
#                         ]
#                     }
#                 }
#             else:
#                 edit_data = {
#                     "data": {
#                         "workspaceId": self.workspace_id,
#                         "action": 1,
#                         "domain": domain,
#                         "recordNum": "京ICP备12022551号",
#                         "productCode": "005",
#                         "liveConf": {
#                             "mode": 1,
#                             "multiProtocol": 1,
#                             "protocolType": 2,
#                             "domainType": 1,
#                             "publishPoint": "live,pull,edit_Auto",
#                             "relatedDomain": "Auto-random-0f6C.ctyun.cn"
#                         },
#                         "httpsPublicContent": Init.PUBLIC_KEY,
#                         "httpsPrivateKey": Init.PRIVATE_KEY,
#                         "certName": "CTYUN_TEST",
#                         "pathTtl": [
#                             {
#                                 "path": "/test/4",
#                                 "ttl": 80,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             }
#                         ],
#                         "filetypeTtl": [
#                             {
#                                 "fileType": "m3u8",
#                                 "ttl": 0,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             },
#                             {
#                                 "fileType": "ts",
#                                 "ttl": 86400,
#                                 "cacheType": 3,
#                                 "cacheWithArgs": 0
#                             }
#                         ],
#                         "ipWhiteList": "127.0.0.3",
#                         "userAgent": {
#                             "type": 0,
#                             "ua": [
#                                 "curl*",
#                                 "*IE"
#                             ]
#                         },
#                         "whiteReferer": {
#                             "allowList": [
#                                 "*.demo.com"
#                             ],
#                             "allowEmpty": "on"
#                         },
#                         "originProtocol": "http",
#                         "origin": [
#                             {
#                                 "origin": "",
#                                 "port": 1935,
#                                 "role": "master",
#                                 "weight": 1
#                             }
#                         ]
#                     }
#                 }
#         else:
#             certName = random_info['data']['certName']
#             public = random_info['data']['httpsPublicContent']
#             private = random_info['data']['httpsPrivateKey']
#             edit_data = {
#                 "data": {
#                     "workspaceId": self.workspace_id,
#                     "action": 1,
#                     "domain": domain,
#                     "productCode": productCode,
#                     "origin": [
#                         {
#                             "role": "master",
#                             "origin": "192.255.0.5",
#                             "port": 10086,  # 修改回源端口
#                             "weight": 1
#                         },
#                         {
#                             "role": "slave",
#                             "origin": "gg.ctyun.cn",
#                             "port": 80,
#                             "weight": 1
#                         }
#                     ],
#                     "originProtocol": "http",
#                     "basicConf": {
#                         "follow302": 0
#                     },
#                     "reqHost": "edit.ctyun.cn",  # 回源Host
#                     "httpsPublicContent": public,
#                     "httpsPrivateKey": private,
#                     "certName": certName,
#                     "pathTtl": [
#                         {
#                             "path": "/test/a",
#                             "ttl": 80,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         }
#                     ],
#                     "filetypeTtl": [
#                         {
#                             "fileType": "php,ashx,aspx,asp,jsp,do",
#                             "ttl": 0,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "js,css,xml,htm,html",
#                             "ttl": 1800,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "jpg,gif,png,bmp,ico,swf,ts,test1,test2",
#                             "ttl": 86400,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         },
#                         {
#                             "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
#                             "ttl": 31536000,
#                             "cacheType": 3,
#                             "cacheWithArgs": 0
#                         }
#                     ],
#                     "ipWhiteList": "199.231.0.5",
#                     "userAgent": {
#                         "type": 0,
#                         "ua": [
#                             "gg.ctyun.cn"
#                         ]
#                     },
#                     "whiteReferer": {
#                         "allowList": [
#                             "gg.ctyun.cn"
#                         ],
#                         "allowEmpty": "on"
#                     }
#                 }
#             }
#         edit_response = self.session.post(url=createDomain_url, json=edit_data, headers=headers_json,
#                                           verify=False)
#         print('eidt body: ', edit_response.text)
#
#         # 编辑后查询域名状态
#         time.sleep(2)
#         check_response3 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('body: ', check_response3.text)
#         body = json.loads(check_response3.text)
#         status_code3 = body['data']['status']
#         print(status_code3)
#         print(
#             '接口返回值： ' + str(check_response3.text) + '  接口耗时：' + str(check_response3.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code3) + "  expect: 3 配置中")
#         assert status_code3 == '3'
#
#         # 工单系统查询域名--提交域名使得域名编辑失败
#         time.sleep(3)
#         workerOrder_failed(domain)
#         check_response4 = self.session.get(url=check_domain_url, params=check_domain_data,
#                                            verify=False)
#         print('edit failed body: ', check_response4.text)
#         status_code4 = json.loads(check_response4.text)['data']['status']
#         print(status_code4)
#         print('工单系统处理域名后，启用域名，编辑域名完成')
#         print('请求方式：get' + '请求URL：' + check_domain_url)
#         print('请求参数：' + str(check_domain_data))
#         print('接口返回值： ' + str(check_response4.text) + '  接口耗时：' + str(check_response4.elapsed.microseconds))
#         print('重点验证：status_code=' + str(status_code4) + "  expect: 4 已启用")
#         assert status_code4 == '4'
#
#     '''
#      :TODO 用户从业务管理平台登录后跳转控制台创建域名，证书
#
#     '''
#
# # if __name__ == '__main__':
# # pytest.main(['-s', 'test_domain'])
# # Test_domain.end_domain()
