# _*_ coding: utf-8 _*_

"""
    业务管理平台通过BSS触发的域名 停用-启用逻辑
    1. 通过接口触发
    2. 如果没有流量包，会直接停用/恢复用户所有域名
    3. 如果有流量包，会查询用户在 wzsy_backend_ziyan.client_flowpacket 的所有流量包
       不停用的条件：  balance >0  status=0(有效)  eff_date<date<exp_date
                    product_id
                    10000 静态加速
                    10002 下载加速
                    10003  视频点播加速
                    10004  视频直播加速
                    10005  全站加速

        BS如果触发停用，那么还会查询 cmdb.domain
       域名状态:  1.审核中 2.审核成功 3.配置中 4.已启用 5.停止中 6.已停止 7.删除中 8.已删除 9.审核失败 10.配置失败 11.停止失败 12.删除失败
       CDN客户控制台域名与工单状态分离之后， 控制台域名状态：  4.已启用 6.已停止  工单管理工单状态： 进行中，成功，失败
       BS判断停用域名，状态范围： 2/3/4/9/10/11  走工单

       BS判断恢复域名，状态范围： 2/5/6/9/10/11  不走工单，直接恢复
       恢复，就是发你那接口 status=1~~；
       恢复不会 对域名进行任何操作，只是会修改cmdb.bss_product.service_status
"""
import requests
import pika
import time
import json


def bs_stopDomain(domain, customerId, customerName):
    # 开发环境
    # host = "36.111.140.92"
    # 测试环境
    host = "36.111.140.48"
    routingKey = "business_operation_queue"
    # 测试环境需加上 开发环境不需要
    userName = "testuser"
    password = "MXFhejJ3c3ghQCMK"

    credentials = pika.PlainCredentials(userName, password)  # mq用户名和密码
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
    channel = connection.channel()

    now = time.time()
    create_time = int(now)
    id = int(now * 100000)

    # domain = "testdomain3.zhihu.com"
    # customerId = "2ce3b241120a4e998a9ae1c53ec4df64"
    # customerName = "蔡君"

    message = {
        "domain": domain,
        "customer_id": customerId,
        "customer_name": customerName,
        "directions": "business_stop_domain",
        "config": "{\"business_flag\":\"business_stop_domain\"}",
        "action": 1,
        "check_status": 2,
        "type": 2,
        "status": 2,
        "id": id,
        "create_time": create_time
    }
    str = json.dumps(message)
    print(type(str))
    print(str)
    channel.basic_publish(exchange="", routing_key=routingKey, body=str)
    connection.close()


def bs_changeDomain(accountid, status):
    # accountid=ba69d44a5ea847be85ffe3f486f087db
    """
    accountid=ba69d44a5ea847be85ffe3f486f087db
    :param accountid:
    :param status: 0 停用   1 恢复
    :return:
    """
    url = "http://bs-test.ctyuncdn.cn/api/v3/account/notify"

    payload = {'account_id': accountid,
               'status': status,
               'token': '800d0db09716433c90f149abf972fe26'}
    files = [

    ]
    headers = {
        'Cookie': 'GWSessionId=de3db03a-4518-4fbb-912a-aeecfca291be'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


"""
INSERT INTO `wzsy_backend_ziyan`.`client_flowpacket` (`resource_id`, `master_order_id`, `client_id`, `product_id`, `billing_area`, `capacity`, `balance`, `eff_date`, `exp_date`, `update_time`, `create_time`, `is_trial_order`, `status`) VALUES ('001188fc3cc54b68b7b41ae549164563', 'a67f56b1bf04446bb830b31f41a9c602', '14444', '10000', '0', '1000000000', '1000000000', '2020-04-26 00:00:00', '2021-04-26 00:00:00', '2020-05-01 20:58:09', '2020-05-01 20:58:09', NULL, '0');

INSERT INTO `wzsy_backend_ziyan`.`client_flowpacket` (`resource_id`, `master_order_id`, `client_id`, `product_id`, `billing_area`, `capacity`, `balance`, `eff_date`, `exp_date`, `update_time`, `create_time`, `is_trial_order`, `status`) VALUES ('001188fc3cc54b68b7b41ae549164564', 'a67f56b1bf04446bb830b31f41a9c602', '14444', '10002', '0', '10000000', '10000000', '2020-04-26 00:00:00', '2021-04-26 00:00:00', '2020-05-01 20:58:09', '2020-05-01 20:58:09', NULL, '0');

INSERT INTO `wzsy_backend_ziyan`.`client_flowpacket` (`resource_id`, `master_order_id`, `client_id`, `product_id`, `billing_area`, `capacity`, `balance`, `eff_date`, `exp_date`, `update_time`, `create_time`, `is_trial_order`, `status`) VALUES ('001188fc3cc54b68b7b41ae549164565', 'a67f56b1bf04446bb830b31f41a9c602', '14444', '10003', '0', '10000000000', '10000000000', '2020-04-26 00:00:00', '2021-04-26 00:00:00', '2020-05-01 20:58:09', '2020-05-01 20:58:09', NULL, '0');

INSERT INTO `wzsy_backend_ziyan`.`client_flowpacket` (`resource_id`, `master_order_id`, `client_id`, `product_id`, `billing_area`, `capacity`, `balance`, `eff_date`, `exp_date`, `update_time`, `create_time`, `is_trial_order`, `status`) VALUES ('001188fc3cc54b68b7b41ae549164566', 'a67f56b1bf04446bb830b31f41a9c602', '14444', '10004', '0', '3000000000', '3000000000', '2020-04-26 00:00:00', '2021-04-26 00:00:00', '2020-05-01 20:58:09', '2020-05-01 20:58:09', NULL, '0');

"""

if __name__ == '__main__':
    bs_changeDomain('ba69d44a5ea847be85ffe3f486f087db', '1')
    # bs_stopDomain('V1_Test_rWkZ.zhihu.com', 'ba69d44a5ea847be85ffe3f486f087db', '陈孟琪')
