# # -*- coding: utf-8 -*-
#
# """
# 封装request
#
# """
# import json
# import os
# import random
# from bin.unit import Session, Log
# from requests_toolbelt import MultipartEncoder
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
#
#
# class Request:
#
#     def __init__(self):
#         """
#         :param env:
#         """
#         self.session = Session.Session()
#         self.get_session = self.session.get_session()
#         self.get_iam_session = self.session.get_iam_private_session()
#         self.log = Log.Log()
#
#     def get_request(self, url, data):
#         """
#         Get请求
#         :param url:
#         :param data:
#         :param header:
#         :return:
#
#         """
#
#         try:
#             if data is None:
#                 response = self.get_session.get(url=url, verify=False)
#             # elif '{' in data:
#             #     response = session.get(url=url, params=data, verify=False, headers=headers_json)
#             else:
#                 response = self.get_session.get(url=url, data=data, verify=False)
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             self.log.error(e)
#             return ()
#
#         time_consuming = response.elapsed.microseconds / 1000
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         # try:
#         #     response_dicts['json'] = response.json()
#         # except Exception as e:
#         #     # print('Response is not json: ', e)
#         #     self.log.error(e)
#         #     response_dicts['json'] = ''
#         response_dicts['body'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#         # print(response_dicts)
#         return response_dicts
#
#     def post_request(self, url, data):
#         """
#         Post请求
#         :param url:
#         :param data:
#         :param header:
#         :return:
#
#         """
#
#         try:
#             if data is None:
#                 response = self.get_session.post(url=url, verify=False)
#             else:
#                 # session.__setattr__(headers,headers_json)
#                 response = self.get_session.post(url=url, data=data, verify=False)
#             # else:
#             #     print('form')
#             #     response = session.post(url=url, params=data, verify=False, headers=headers_form)
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             self.log.info('%s%s' % ('Exception url: ', url))
#             return ()
#
#         # time_consuming为响应时间，单位为毫秒
#         time_consuming = response.elapsed.microseconds / 1000
#         # time_total为响应时间，单位为秒
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         # try:
#         #     response_dicts['json'] = response.json()
#         # except Exception as e:
#         #     Log.Log().error(e)
#         #     response_dicts['json'] = ''
#
#         response_dicts['body'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#
#         return response_dicts
#
#     def workOrder_get(self, url, data):
#         """
#         Get请求
#         :param url:
#         :param data:
#         :param header:
#         :return:
#
#         """
#
#         try:
#             if data is None:
#                 response = self.get_iam_session.get(url=url, verify=False, headers=header)
#             # elif '{' in data:
#             #     response = session.get(url=url, params=data, verify=False, headers=headers_json)
#             else:
#                 response = self.get_iam_session.get(url=url, data=data, headers=header)
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             self.log.error(e)
#             return ()
#
#         time_consuming = response.elapsed.microseconds / 1000
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         # try:
#         #     response_dicts['json'] = response.json()
#         # except Exception as e:
#         #     # print('Response is not json: ', e)
#         #     self.log.error(e)
#         #     response_dicts['json'] = ''
#         response_dicts['body'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#         # print(response_dicts)
#         return response_dicts
#
#     def workOrder_post(self, url, data, head):
#         """
#         Post请求
#         :param url:
#         :param data:
#         :param header:
#         :return:
#
#         """
#
#         try:
#             if data is None:
#                 response = self.get_iam_session.post(url=url, headers=head)
#             else:
#                 response = self.get_iam_session.post(url=url, data=data, headers=head)
#                 print('post success! ')
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             self.log.info('%s%s' % ('Exception url: ', url))
#             return ()
#
#         # time_consuming为响应时间，单位为毫秒
#         time_consuming = response.elapsed.microseconds / 1000
#         # time_total为响应时间，单位为秒
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         # try:
#         #     response_dicts['json'] = response.json()
#         # except Exception as e:
#         #     Log.Log().error(e)
#         #     response_dicts['json'] = ''
#
#         response_dicts['body'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#
#         return response_dicts
#
#     def post_request_multipart(self, url, data, header, file_parm, file, f_type):
#         """
#         提交Multipart/form-data 格式的Post请求
#         :param url:
#         :param data:
#         :param header:
#         :param file_parm:
#         :param file:
#         :param type:
#         :return:
#         """
#         # if not url.startswith('https://'):
#         #     url = '%s%s' % ('https://', url)
#         #     print(url)
#         url = self.host + url
#         print(url)
#         try:
#             if data is None:
#                 response = self.get_session.post(url=url, headers=header, verify=False)
#             else:
#                 data[file_parm] = os.path.basename(file), open(file, 'rb', encoding='utf-8'), f_type
#
#                 enc = MultipartEncoder(
#                     fields=data,
#                     boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
#                 )
#
#                 header['Content-Type'] = enc.content_type
#                 response = self.get_session.post(url=url, params=data, headers=header, verify=False)
#
#         except self.get_session.RequestException as e:
#             print('%s%s' % ('RequestException url: ', url))
#             print(e)
#             return ()
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             print(e)
#             return ()
#
#         # time_consuming为响应时间，单位为毫秒
#         time_consuming = response.elapsed.microseconds / 1000
#         # time_total为响应时间，单位为秒
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         try:
#             response_dicts['body'] = response.json()
#         except Exception as e:
#             print(e)
#             response_dicts['body'] = ''
#
#         response_dicts['text'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#
#         return response_dicts
#
#     def put_request(self, url, data, header):
#         """
#         Put请求
#         :param url:
#         :param data:
#         :param header:
#         :return:
#
#         """
#         # if not url.startswith('https://'):
#         #     url = '%s%s' % ('https://', url)
#         #     print(url)
#         url = self.host + url
#         print(url)
#         try:
#             if data is None:
#                 response = self.get_session.put(url=url, headers=header, verify=False)
#             else:
#                 response = self.get_session.put(url=url, params=data, headers=header, verify=False)
#
#         except self.get_session.RequestException as e:
#             print('%s%s' % ('RequestException url: ', url))
#             print(e)
#             return ()
#
#         except Exception as e:
#             print('%s%s' % ('Exception url: ', url))
#             print(e)
#             return ()
#
#         time_consuming = response.elapsed.microseconds / 1000
#         time_total = response.elapsed.total_seconds()
#
#         response_dicts = dict()
#         response_dicts['code'] = response.status_code
#         try:
#             response_dicts['body'] = response.json()
#         except Exception as e:
#             print(e)
#             response_dicts['body'] = ''
#         response_dicts['text'] = response.text
#         response_dicts['time_consuming'] = time_consuming
#         response_dicts['time_total'] = time_total
#
#         return response_dicts
#
#
# if __name__ == '__main__':
#     # test = Request('test')
#     # ss = test.get_request(url='https://iam-test.ctcdn.cn/iam/gw/workspace/GetDetail', data='workspaceId=10003885')
#     aa = {'paging': {'total_page': 1, 'page': 1, 'per_page': 10, 'total_record': 1},
#           'status': {'code': 0, 'message': 'ok'}, 'work_order': [
#             {'order_id': 3643, 'order_no': 'WO2020090100003773', 'order_type_code': 'autoCreateDomainConfigOrder',
#              'order_type_code_name': 'CDN-客户自助配置-新增域名工单', 'order_sub_type_code': 'domainConfig',
#              'order_sub_type_code_name': '', 'order_title': '新增域名-陈孟琪-Auto-random-a3Ab.ctyun.cn',
#              'flow_inst_no': 'E5CD21C8A468E7B6', 'flow_current_status': 'onDemandWaitDomainConfCbk',
#              'flow_current_status_name': '配置执行结果回调', 'status_cd': 'orderOnway', 'status_cd_name': '',
#              'status_date': '2020-09-01 16:03:59', 'create_date': '2020-09-01 16:03:58',
#              'update_date': '2020-09-01 16:03:59', 'create_staff_id': '1', 'create_staff_name': '客户控制台',
#              'current_staff_id': '', 'current_staff_name': '域名配置系统', 'create_sys': 'custCons', 'create_sys_name': '',
#              'current_sys': 'workOrderMgmt', 'current_sys_name': '', 'remark': '处理环节[下发配置]', 'acct_name': '陈孟琪',
#              'cust_domain': 'Auto-random-a3Ab.ctyun.cn'}]}
#     bb = json.dumps(aa['work_order'])
#     # print(bb.get('work_order'))
#     # print(type(bb))
#     # print(bb.get('order_id'))
#     print(aa['work_order'][0]['order_id'])
