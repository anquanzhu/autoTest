# -*- coding: utf-8 -*-
import json
import time

from bin.Init import Init
from bin.unit import Log
from bin.unit.Rondom import random_int

base_info = Init.BASE_INFO
domain_info = Init.DOMAIN_INFO
workOrder_host = base_info['workOrderHost']
log = Log.Log()
session = Init.BS_SESSION
session_workOrder = Init.WO_SESSION
headers_json = base_info['headers_json']
headers_form = base_info['headers_form']
header = base_info['header_form_wo']
header_post = base_info['header_json_wo']


def workOrder_Flow_Domain(domain):
    # 处理工单流程：停用/启用/删除
    search_url = workOrder_host + domain_info['getOrder_id']
    deal_url = workOrder_host + domain_info['dealOrder']
    time.sleep(5)
    # 工单系统查询域名--提交域名
    search_data1 = '{"work_order":{"order_title":"' + domain + '","sort":"desc","current_staff_id":"20","status_cd":"orderOnway"},"paging":{"page":1,"per_page":10}}'
    # 查询工单系统，获取order_no
    workerOrder_response1 = session_workOrder.post(url=search_url, data=search_data1, headers=header, timeout=10)
    print('1', workerOrder_response1.text)
    content = json.loads(workerOrder_response1.text)
    # order_no = body['work_order'][0]['order_no']
    if content['work_order'] != []:
        order_id = content['work_order'][0]['order_id']
        order_no = content['work_order'][0]['order_no']
        order_typecode = content['work_order'][0]['order_type_code']
        cnname = content['work_order'][0]['acct_name']
        flow_current_status = content['work_order'][0]['flow_current_status']
    else:
        print('工单异常')
        return
    stop_data = {"drive_work_orders": [
        {"order_type_code": order_typecode, "order_no": str(order_no), "current_action": "deal",
         "flow_current_status": "waitExecDomainConf", "current_staff_id": "20", "current_sys": "workOrderMgmt",
         "current_staff_name": cnname, "work_order_configs": [{"name": "工单公用属性", "code": "workOrderAttr",
                                                               "work_order_attrs": [
                                                                   {"name": "是否大客户", "code": "isKeyAccount",
                                                                    "value": "yes"},
                                                                   {"name": "紧急程度", "code": "urgency", "value": "0"},
                                                                   {"name": "CNAME", "code": "cname"},
                                                                   {"name": "是否通知第三方", "code": "isNotifyThird",
                                                                    "value": "yes"},
                                                                   {"name": "工单状态", "code": "domainOrderStatus",
                                                                    "value": "3"},
                                                                   {"name": "简单概述", "code": "overview"}]}]}]}
    time.sleep(5)
    workerOrder_response3 = session_workOrder.request("POST", url=deal_url, data=json.dumps(stop_data),
                                                      headers=header_post, timeout=10)
    print(workerOrder_response3.text)
    if '400' in workerOrder_response3.text:
        workerOrder_response4 = session_workOrder.request("POST", url=deal_url, data=json.dumps(stop_data),
                                                          headers=header_post, timeout=10)
        print('重试停用接口：', workerOrder_response4.text)
    time.sleep(3)


"""
    工单流程变动，修改代码
    1. 通过域名查工单号
    2. 通过工单号查工单信息， 如果已经分配了承载平台可以直接办结
    3. 没有配置承载平台需要配置，然后返回2
    4. 工单办结，退单
"""


def deal_new_domain(domain, domain_status):
    """

    :param domain:
    :param domain_status: 3 - 成功， 4 - 失败
    :return:
    """
    # 通过域名查询Order_no, 工单号  主要分为自助和非自助的
    #  自助： autoCreateDomainConfigOrder   非自助：createDomainConfigOrder
    # "order_type_code":"createDomainConfigOrder,modifyDomainConfigOrder,operDomainConfigOrder,autoCreateDomainConfigOrder,
    # autoModifyDomainConfigOrder,autoOperDomainConfigOrder"
    deal_url = workOrder_host + domain_info['dealOrder']
    search_url = workOrder_host + domain_info['getOrder_id']
    search_data = {"work_order": {"order_title": domain, "sort": "desc", "current_staff_id": "20",
                                  "status_cd": "orderOnway"}, "paging": {"page": 1, "per_page": 10}}
    # search_data1 = {"work_order": {"order_title": domain, "order_type_code": order_type, "sort": "desc",
    #                                "current_staff_id": "20", "status_cd": "orderOnway"},
    #                 "paging": {"page": 1, "per_page": 10}}
    time.sleep(2)
    wo_response1 = session_workOrder.request("POST", url=search_url, data=json.dumps(search_data),
                                             headers=header_post, timeout=10)
    print(1, wo_response1.text)
    if json.loads(wo_response1.text)['work_order'] != []:
        # order_id = json.loads(wo_response1.text)['work_order'][0]['order_id']
        order_no = json.loads(wo_response1.text)['work_order'][0]['order_no']
        order_typecode = json.loads(wo_response1.text)['work_order'][0]['order_type_code']
        cnname = json.loads(wo_response1.text)['work_order'][0]['acct_name']
        flow_current_status = json.loads(wo_response1.text)['work_order'][0]['flow_current_status']
    else:
        print('工单异常')
        return

    conf_hosting_info = {"order_type": order_typecode, "drive_work_orders": [
        {"order_no": str(order_no), "order_title": "新增域名-" + cnname + "-" + domain,
         "order_type_code": order_typecode, "current_action": "deal", "current_staff_id": "20",
         "current_sys": "workOrderMgmt", "current_staff_name": cnname, "flow_current_status": flow_current_status,
         "el_value": "yes", "next_task_user_codes": [], "notice_methods": [], "remark": "", "work_order_configs": [
            {"name": "工单公用属性", "code": "workOrderAttr",
             "work_order_attrs": [{"name": "承载平台", "code": "platform", "value": "001,007"}]}]}]}

    # 如果配置了承载平台
    cname = 'auto' + random_int('1000, 100000')
    sub_domain_info = {"drive_work_orders": [
        {"order_type_code": order_typecode, "order_no": str(order_no), "current_action": "deal",
         "flow_current_status": "waitExecDomainConf", "current_staff_id": "20", "current_sys": "workOrderMgmt",
         "current_staff_name": cnname, "work_order_configs": [{"name": "工单公用属性", "code": "workOrderAttr",
                                                               "work_order_attrs": [
                                                                   {"name": "是否大客户", "code": "isKeyAccount",
                                                                    "value": "yes"},
                                                                   {"name": "紧急程度", "code": "urgency", "value": "0"},
                                                                   {"name": "配置范围", "code": "confScope", "value": "1"},
                                                                   {"name": "测试URL", "code": "testUrl"},
                                                                   {"name": "异网CNMAE", "code": "diffNetCNMAE"},
                                                                   {"name": "CNAME", "code": "cname",
                                                                    "value": cname},
                                                                   {"name": "工单状态", "code": "domainOrderStatus",
                                                                    "value": domain_status},
                                                                   {"name": "简单概述", "code": "overview"}]}]}]}

    mod_domain_info = {"drive_work_orders": [
        {"order_type_code": order_typecode, "order_no": str(order_no), "current_action": "deal",
         "flow_current_status": "waitExecDomainConf", "current_staff_id": "20", "current_sys": "workOrderMgmt",
         "current_staff_name": cnname, "work_order_configs": [{"name": "工单公用属性", "code": "workOrderAttr",
                                                               "work_order_attrs": [
                                                                   {"name": "是否大客户", "code": "isKeyAccount",
                                                                    "value": "yes"},
                                                                   {"name": "紧急程度", "code": "urgency", "value": "0"},
                                                                   {"name": "配置范围", "code": "confScope", "value": "1"},
                                                                   {"name": "测试URL", "code": "testUrl"},
                                                                   {"name": "第三方是否完成", "code": "isThirdFinish",
                                                                    "value": "yes"},
                                                                   {"name": "工单状态", "code": "domainOrderStatus",
                                                                    "value": "3"},
                                                                   {"name": "简单概述", "code": "overview"}]}]}]}

    # 根据当前工单状态判断是否有配置承载平台
    if flow_current_status != 'waitExecDomainConf':
        hosting_response = session_workOrder.request("POST", url=deal_url, data=json.dumps(conf_hosting_info),
                                                     headers=header_post, timeout=10)
        print('hosting_response: ', hosting_response.text)
        time.sleep(2)
        # 编辑
        if order_typecode == "autoModifyDomainConfigOrder":
            mod_response = session_workOrder.request("POST", url=deal_url, data=json.dumps(mod_domain_info),
                                                     headers=header_post, timeout=10)
            print('mod_response:', mod_response.text)
        else:
            sub_wo_response1 = session_workOrder.request("POST", url=deal_url, data=json.dumps(sub_domain_info),
                                                         headers=header_post, timeout=10)
            print('sub_wo_response2:', sub_wo_response1.text)
    else:
        # 编辑
        if order_typecode == "autoModifyDomainConfigOrder" or order_typecode == "modifyDomainConfigOrder":
            mod_response = session_workOrder.request("POST", url=deal_url, data=json.dumps(mod_domain_info),
                                                     headers=header_post, timeout=10)
            print('mod_response:', mod_response.text)

        else:
            sub_wo_response2 = session_workOrder.request("POST", url=deal_url, data=json.dumps(sub_domain_info),
                                                         headers=header_post, timeout=10)
            print('sub_wo_response2:', sub_wo_response2.text)


def workorder_fail_domain(domain):
    deal_url = workOrder_host + domain_info['dealOrder']
    search_url = workOrder_host + domain_info['getOrder_id']
    search_data = {"work_order": {"order_title": domain, "sort": "desc", "current_staff_id": "20",
                                  "status_cd": "orderOnway"}, "paging": {"page": 1, "per_page": 10}}
    # search_data1 = {"work_order": {"order_title": domain, "order_type_code": order_type, "sort": "desc",
    #                                "current_staff_id": "20", "status_cd": "orderOnway"},
    #                 "paging": {"page": 1, "per_page": 10}}
    wo_response1 = session_workOrder.request("POST", url=search_url, data=json.dumps(search_data),
                                             headers=header_post, timeout=10)
    print(1, wo_response1.text)
    if json.loads(wo_response1.text)['work_order'] != []:
        order_id = json.loads(wo_response1.text)['work_order'][0]['order_id']
        order_no = json.loads(wo_response1.text)['work_order'][0]['order_no']
        order_typecode = json.loads(wo_response1.text)['work_order'][0]['order_type_code']
        cnname = json.loads(wo_response1.text)['work_order'][0]['acct_name']
        flow_current_status = json.loads(wo_response1.text)['work_order'][0]['flow_current_status']
    else:
        print('工单异常')
        return

    conf_hosting_info = {"order_type": order_typecode, "drive_work_orders": [
        {"order_no": str(order_no), "order_title": "新增域名-" + cnname + "-" + domain,
         "order_type_code": order_typecode, "current_action": "deal", "current_staff_id": "20",
         "current_sys": "workOrderMgmt", "current_staff_name": cnname, "flow_current_status": flow_current_status,
         "el_value": "yes", "next_task_user_codes": [], "notice_methods": [], "remark": "", "work_order_configs": [
            {"name": "工单公用属性", "code": "workOrderAttr",
             "work_order_attrs": [{"name": "承载平台", "code": "platform", "value": "001,007"}]}]}]}

    # 如果配置了承载平台
    cname = 'auto' + random_int('1000, 100000')
    sub_domain_info = {"drive_work_orders": [
        {"order_type_code": order_typecode, "order_no": str(order_no), "current_action": "deal",
         "flow_current_status": "waitExecDomainConf", "current_staff_id": "20", "current_sys": "workOrderMgmt",
         "current_staff_name": cnname, "work_order_configs": [{"name": "工单公用属性", "code": "workOrderAttr",
                                                               "work_order_attrs": [
                                                                   {"name": "是否大客户", "code": "isKeyAccount",
                                                                    "value": "yes"},
                                                                   {"name": "紧急程度", "code": "urgency", "value": "0"},
                                                                   {"name": "配置范围", "code": "confScope", "value": "1"},
                                                                   {"name": "测试URL", "code": "testUrl"},
                                                                   {"name": "异网CNMAE", "code": "diffNetCNMAE"},
                                                                   {"name": "CNAME", "code": "cname",
                                                                    "value": cname},
                                                                   {"name": "工单状态", "code": "domainOrderStatus",
                                                                    "value": "4"},
                                                                   {"name": "简单概述", "code": "overview"}]}]}]}
    # 编辑失败
    mod_domain_info = {"drive_work_orders": [
        {"order_type_code": order_typecode, "order_no": str(order_no), "current_action": "deal",
         "flow_current_status": "waitExecDomainConf", "current_staff_id": "20", "current_sys": "workOrderMgmt",
         "current_staff_name": cnname, "work_order_configs": [{"name": "工单公用属性", "code": "workOrderAttr",
                                                               "work_order_attrs": [
                                                                   {"name": "是否大客户", "code": "isKeyAccount",
                                                                    "value": "yes"},
                                                                   {"name": "紧急程度", "code": "urgency", "value": "0"},
                                                                   {"name": "配置范围", "code": "confScope", "value": "1"},
                                                                   {"name": "测试URL", "code": "testUrl"},
                                                                   {"name": "第三方是否完成", "code": "isThirdFinish",
                                                                    "value": "yes"},
                                                                   {"name": "工单状态", "code": "domainOrderStatus",
                                                                    "value": "4"},
                                                                   {"name": "简单概述", "code": "overview"}]}]}]}

    # 根据当前工单状态判断是否有配置承载平台
    if flow_current_status != 'waitExecDomainConf':
        hosting_response = session_workOrder.request("POST", url=deal_url, data=json.dumps(conf_hosting_info),
                                                     headers=header_post, timeout=10)
        print('hosting_response: ', hosting_response.text)
        time.sleep(2)
        sub_wo_response1 = session_workOrder.request("POST", url=deal_url, data=json.dumps(sub_domain_info),
                                                     headers=header_post, timeout=10)
        print('sub_wo_response2:', sub_wo_response1.text)
    else:
        # 编辑
        if order_typecode == "autoModifyDomainConfigOrder" or order_typecode == "modifyDomainConfigOrder":
            mod_response = session_workOrder.request("POST", url=deal_url, data=json.dumps(mod_domain_info),
                                                     headers=header_post, timeout=10)
            print('mod_response:', mod_response.text)

        else:
            sub_wo_response2 = session_workOrder.request("POST", url=deal_url, data=json.dumps(sub_domain_info),
                                                         headers=header_post, timeout=10)
            print('sub_wo_response2:', sub_wo_response2.text)


if __name__ == '__main__':
    # workerOrder_deal('Auto-random-4b6d.ctyun.cn')
    # bs_hosting_platform('Auto-random-caDF.ctyun.cn')
    # bs_hosting_platform('15988792702290')
    # bs_end_domain('15984359193770')
    # workerOrder_deal('Auto-random-1Ba3.ctyun.cn')
    # workOrder_stopDomain('Auto-random-Ef4e.ctyun.cn')
    # workorder_fail_domain("Domain_Test_e74a.zhihu.com")
    # workOrder_Flow_Domain("V1_Test_ZQWC.zhihu.com")
    # deal_new_domain("V1_Test_dnRt.zhihu.com", "3")
    workOrder_Flow_Domain('Auto-aiMBAR.ctyun.cn')
