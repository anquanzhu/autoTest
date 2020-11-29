# # -*- coding: utf-8 -*-
# import json
# import os
# from bin.Init import Init
#
# root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#
#
# def readJson(jsonfile):
#     """
#     读取yaml文件，root_dir为项目的根目录
#     :param yamlname: 从根目录出发，达到的yaml具体路径
#     :return: yaml文件的所有内容，dict 类型
#     """
#     jsonPath = os.path.join(root_dir, jsonfile)
#     # print(jsonPath)
#     with open(jsonPath) as f:
#         json_data = json.load(f)
#     return json_data
#
#
# def get_data(data_path):
#     if data_path == 'bs':
#         file_list = Init.SINGLE_INFO_BS
#     elif data_path == 'vip':
#         file_list = Init.SINGLE_INFO
#     else:
#         file_list = Init.SINGLE_INFO_CTYUN
#     data_dict = []
#     data_list = []
#     for file in file_list:
#         testcases = readJson("testcases/" + data_path + "/" + file)
#         # print('file:', file)
#         case_dict = list(testcases['testcases'].items())
#         # print('list:', case_dict.items())
#         for i in range(len(case_dict)):
#             # allure.testcase(url)
#             case = case_dict[i]
#             # print('case',case)
#             # print('case1',case[1])
#             url = case[1]['url']
#             method = case[1]['method']
#             # allure.step('接口请求方式：', method)
#             if 'body' in case[1].keys():
#                 body = case[1]['body']
#             else:
#                 body = ''
#             data_list.append(url)
#             data_list.append(method)
#             data_list.append(body)
#             data_tuple = tuple(data_list)
#             data_dict.append(data_tuple)
#             data_list = []
#     # print('data:',data_dict)
#     return data_dict
#
#
# if __name__ == '__main__':
#     # aa = readJson('testcases/RECORD-2020-08-26-8-43.json')
#     bb = get_data('bs')
#     # print(aa)
