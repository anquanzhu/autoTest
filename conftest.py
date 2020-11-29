# # -*- coding: utf-8 -*-
# import json
# import os, sys
#
# import pytest
# import requests
# from bin.Init import Init
# from bin.Upload_Result import Upload_Result
#
# upload = Upload_Result()
# headers_json = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
#                                   Chrome/67.0.3396.99 Safari/537.36",
#     "Content-Type": "application/json",
# }
#
# case_nums = 0
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_collection_modifyitems(items):
#     # print("len::", len(items))
#     global case_nums
#     case_nums = case_nums + int(len(items))
#     print("用例总数case_nums： ", case_nums)
#     return case_nums
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     out = yield
#     rep = out.get_result()
#     # setattr(item, "rep_" + rep.when, rep)
#     # print("rep:", rep)
#     '''
#     rep: <TestReport 'test_cert.py::Test_cert::test_CDN_238495' when='teardown' outcome='passed'>
#     '''
#     # print("nodeid: ",rep.nodeid)
#     # print("len::", len(items))
#     # print("1111111111111", case_nums)
#     i = 0
#     if rep.when == 'call':
#         i = i + 1
#         if 'test_CDN' in rep.nodeid:
#             id = str(rep.nodeid).split('::')[-1].replace("test_CDN_", "")
#             id = int(id)
#         else:
#             id = ''
#         if rep.outcome == 'skipped':
#             ispass = 2
#             # resultinfo = "测试skipped"
#         elif rep.outcome == "failed":
#             ispass = 0
#
#         else:
#             ispass = 1
#             # resultinfo = "测试通过"
#
#         info = upload.update_result(id, ispass)
#         # print("sssss: ", info)
#         i = i + 1
#         if i > 200:
#             print("i:", info)
#         if i == case_nums:
#             print("用例总数： ", str(i))
#             print("推送测试用例平台: ", info)
#             response = requests.post('https://36.111.140.76:8443/automatedTest/updateCaseResult', json.dumps(info),
#                                      headers=headers_json,
#                                      verify=False)
#             print(response.text)
