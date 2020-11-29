# -*- coding: utf-8 -*-
import os
import json
import string
import threading
import time
import random
import copy
from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from multiprocessing import Process

# server_list = ['ctl-nm-hhht-yxxya6-dnscskf-004.ctyuncdn.net:5044', 'ctl-nm-hhht-yxxya6-rzfx2-001.ctyuncdn.net:5044']
# server_list = ['192.168.2.40:6667', '192.168.2.42:6667']
# 集成环境
# server_list = ['182.140.235.58:5044', '182.140.235.59:5044', '182.140.235.62:5044', '182.140.235.64:5044']
server_list = ["int-chengdu-loganalysis-229-ecloud.com:5044", "int-chengdu-loganalysis-125-ecloud.com:5044",
               "int-chengdu-loganalysis-207-ecloud.com:5044"]
succ = 0
err = 0

"""
1.直播加速和点播加速直接计入PV，其他不计入PV；
  cmq002.ksedu.cn  cmq004.test004.cn

2.下载加速和静态加速按照以下定义：PV统计响应状态码非0且小于400，
    默认类型包括：htm、html、php、asp、shtm、shtml、aspx、xml、xhtml、xsl、cfm、htx、htmls、phtml、jsp、hph3、txt、
    wml、lhtml、pl、cgi、cfm、acgi、srch、qry，
    结尾以"/"（例如http://www.test.com/abc/)或找不到"."的（例如http://www.test.com/abc)也计入PV。
    cmq003.ksedu.cn  a1.baidu.com tt.cmqtest.com
3. UV就是去重后的clientip的数量
"""


def on_send_success(record_metadata):
    global succ
    succ += 1
    pass


def on_send_error(excp):
    print(str(excp))
    global err
    err += 1


def random_weight(weight_data):
    total = sum(weight_data.values())  # 权重求和
    ra = random.uniform(0, total)  # 在0与权重和之前获取一个随机数
    curr_sum = 0
    ret = None

    # keys = weight_data.iterkeys()  # 使用Python2.x中的iterkeys
    keys = weight_data.keys()  # 使用Python3.x中的keys
    for k in keys:
        curr_sum += weight_data[k]  # 在遍历中，累加当前权重值
        if ra <= curr_sum:  # 当随机数<=当前权重和时，返回权重key
            ret = k
            break
    return ret


flow_list = [1122197.01, 1065676.98, 1015723.1,
             981419.63,
             949987.31,
             923279.51,
             881549.79,
             848562.62,
             816728.64,
             787284.61,
             752227.42,
             717876.15,
             686543.18,
             662887.38,
             641440.16,
             618519.03,
             587509.75,
             559998.7,
             529819.21,
             509678.49,
             488852.71,
             442790.85,
             410523.58,
             403429.05,
             391012.09,
             371518.41,
             357166.12,
             347455.19,
             337713.54,
             326923.51,
             315525.51,
             303787.56,
             292978.55,
             285167.22,
             275020.76,
             268061.7,
             252498.66,
             241873.22,
             233844.54,
             228756.28,
             224625.37,
             216969.2,
             210662.48,
             207031.21,
             200666.46,
             195762.76,
             192003.33,
             189039.96,
             184639.73,
             178665.42,
             174842.17,
             174299.91,
             173286.83,
             172012.18,
             171746.92,
             171539.46,
             171894.28,
             172890.33,
             173077.6,
             178312.93,
             181205.59,
             182861.8,
             184096.52,
             190637.02,
             200795.04,
             204066.6,
             210093.88,
             221735.55,
             231526.95,
             238727.64,
             250724.03,
             262462.97,
             277024.86,
             283022.21,
             299607.37,
             320737.31,
             332420.72,
             346895.55,
             368593.57,
             390213.09,
             398941.11,
             300650.55,
             277562.37,
             293372.7,
             382072.98,
             340844.19,
             308794.08,
             289750.46,
             266076.43,
             250104.34,
             306815.44,
             443734.93,
             487206.11,
             515238.93,
             549542.79,
             567450.85,
             574232.13,
             577890.13,
             588340.11,
             619442.73,
             629123.02,
             635182.83,
             644006.51,
             652691.38,
             661268.65,
             673208.74,
             684094.28,
             691252.49,
             697750.46,
             694319.96,
             708298.5,
             712974.3,
             712409.05,
             723109.04,
             724659.87,
             736810.1,
             746882.71,
             745241.29,
             754104.01,
             770221.88,
             768701.04,
             776270.81,
             786971.49,
             799853.36,
             805177.68,
             813032.13,
             828201.33,
             839524.52,
             844099.33,
             865126.15,
             881210.48,
             880105.51,
             869929.82,
             862572.3,
             883996.4,
             916712.16,
             935205.31,
             937762.51,
             947082.35,
             954924.4,
             993980.18,
             1015000.44,
             1060537.87,
             1079251.52,
             1066562.69,
             1080925.51,
             1151159.47,
             1229897.79,
             1292760.11,
             1343423.09,
             1371739.15,
             1394956.95,
             1408257.28,
             1405370.21,
             1397372.33,
             1389452.03,
             1326379.59,
             1253527.32,
             1250292.32,
             1242121.85,
             1213896.56,
             1185983.01,
             1153108.82,
             1117431.5,
             1094036.02,
             1077966.78,
             1068480.9,
             1049769.64,
             1015835.89,
             986610.08,
             995547.43,
             1011082.82,
             990503.7,
             965800.96,
             969958.39,
             994099.72,
             974333.97,
             976255.55,
             974348.7,
             981757.92,
             954095.67,
             914839.67,
             919661.49,
             956804.28,
             936641.14,
             944406.63,
             960576.12,
             971456.41,
             953769.66,
             959243.22,
             964276.68,
             972213.31,
             963037.13,
             921992.67,
             926084.65,
             966036.35,
             967334,
             965267.7,
             976105.6,
             982564.75,
             993278.48,
             1006150.91,
             1012874.61,
             1018297.77,
             993670.73,
             963875.2,
             980655.11,
             1032319.36,
             1014124.91,
             1029716.36,
             1030228.67,
             1044916.39,
             1064900.9,
             1111122.67,
             1126548.88,
             1150387.5,
             1134523.31,
             1142242.61,
             1173058.41,
             1203709.17,
             1235803.93,
             1256114.22,
             1269702.3,
             1291480.36,
             1330424.26,
             1361753.28,
             1354659.89,
             1372374.19,
             1401587.49,
             1396989.95,
             1393770.71,
             1444093.41,
             1478889.23,
             1470741.64,
             1489133.65,
             1533269.46,
             1529755.94,
             1528782.4,
             1557844.27,
             1589857.49,
             1570855.78,
             1553285.23,
             1589427.77,
             1633260.68,
             1641783.76,
             1668296.07,
             1674451.28,
             1698539.54,
             1717698.45,
             1719743.35,
             1732748.33,
             1745627.16,
             1737280.25,
             1730424.86,
             1734323.35,
             1758525.55,
             1777691.23,
             1792236.68,
             1805509.48,
             1805618.78,
             1818019.48,
             1819424.75,
             1819600.28,
             1827745.2,
             1818764.61,
             1781424.48,
             1769374.8,
             1758791.71,
             1738370.58,
             1698303.83,
             1679911.73,
             1718880.64,
             1716683.22,
             1682840.18,
             1646420.18,
             1642294.54,
             1612970.34,
             1556961.92,
             1521405.37,
             1496341.27,
             1464198.29,
             1420631.7,
             1405216.63,
             1352507.03,
             1319144.65,
             1308159.74,
             1256867.95,
             1216201.48
             ]
referer_list1 = ['-', '', '', '-',
                 'https://h5.bestpay.com.cn/subapps/redbagCombo/life-depot/main.html?hybridVersion=3.0&channel=tab&isTab=1',
                 '',
                 'https://m.bestpay.com.cn/',
                 'https://m.bestpay.com.cn/?isHome=true&url=aHR0cHM6Ly9oNS5iZXN0cGF5LmNvbS5jbi9zdWJhcHBzL3JlZGJhZ0NvbWJvL212cC12aXAvbWFpbi5odG1sP2h5YnJpZFZlcnNpb249My4wJmNoYW5uZWw9bWVzc2FnZQAA&encodefn=base64',
                 'https://servicewechat.com/wx77120a925cc97e10/23/page-frame.html',
                 'https://h5.bestpay.com.cn/subapps/quanyi-product-h5/index.html?hybridVersion=3.0',
                 'https://ctcdn.bestpay.cn/orange/upload/client/stock/stock_open/ypay_zxjtopen_v2.0/index.html?hybridVersion=3.0',
                 'https://h5.bestpay.com.cn/subapps/openBestpay/index.html',
                 'https://servicewechat.com/preload/page-frame.html',
                 'https://servicewechat.com/wx77120a925cc97e10/22/page-frame.html',
                 'https://h5.bestpay.com.cn/subapps/openBestpay/yimatong.html',
                 'https://h5.bestpay.com.cn/subapps/nearby-shops-h5/alpha-nearby/index.html?hybridVersion=3.0',
                 'https://h5.bestpay.com.cn/',
                 'https://ctcdn.bestpay.cn/html/h5-page/wx-online-link/OfficialAccounts/main.html?hybridVersion=3.0',
                 'https://activity.bestpay.cn/subapps/openBestpay/index.html?isHome=true&url=https://activity.bestpay.cn/subapps/marketing-reco-h5/referrer-h5/index.html?hybridVersion=3.0',
                 'https://ctcdn.bestpay.cn/finance/consumestage/lightapps2/main.html',
                 'https://m.bestpay.com.cn/?isHome=true&id=51007021',
                 'https://cdn.bestpay.cn/group1/M00/03/78/rBwwjF9tSouEULizAAAAANTrICo07.html',
                 'https://h5.bestpay.com.cn/subapps/h5login/index.html',
                 'https://cfs.bestpay.com.cn/login',
                 'https://e.douyin.com/',
                 '-', '-', '',
                 'https://creator.douyin.com/billboard/cospa',
                 'https://e.douyin.com/site/operation-center/video-manage',
                 'https://www.douyin.com/',
                 'https://www.baidu.com/',
                 'https://servicewechat.com/wxa51b04042501e43a/48/page-frame.html',
                 'http://v95-dy-a.ixigua.com/ea3ccd0fbfbcf9dbe73513a5056b175f/5f952b7f/video/tos/cn/tos-cn-ve-15/743ed249a2f64b78b0bd490dc7e4faf0/?a=1128&br=3123&bt=1041&cr=0&cs=0&dr=0&ds=3&er=&l=202010251149250101980230535A0668AA&lr=aweme_search_suffix&mime_type=video_mp4&qs=0&rc=am9kdXBxcjtneDMzZGkzM0ApZDM3PGdoNmQ0N2g4NGczZWdtY3NjYnFnbTZfLS02LTBzczIyMjBeXy1iMF9iXzIyXzI6Yw%3D%3D&vl=&vr=',
                 'http://v95-hs.ixigua.com/954a93287427f47b1ab29ca81669e5ea/5f9509ec/video/tos/cn/tos-cn-v-0000/8c44de403fcc46b3a5bcf39ce6bd9c3b',
                 'https://tcs.jiyunhudong.com/',
                 'https://www.ixigua.com/6886688915864945163?logTag=XTsp_fOeYX11h3-WUxOHU',
                 'http://v95-dy-a.ixigua.com/15d6de747d305dbb227d97508a5418f1/5f9542bf/video/tos/cn/tos-cn-ve-15/6d6a9376bbbc44a3ba6bcd633b2d8ab2',
                 'http://v95-dy-a.ixigua.com',
                 'http://v95-hs.ixigua.com/d804a331733a920886491258cdd46360/5f95a00f/video/tos/cn/tos-cn-v-0000/ffb7611e7b02491eb363817ab3ead443',
                 'https://www.ixigua.com/6856381261938688526?logTag=qp-nGBhHhSmJcck_cvZ3l',
                 'https://www.toutiao.com/item/6887283608990515716/',
                 'https://servicewechat.com/wxcc986a59cdbab421/57/page-frame.html',
                 'http://v95-dy-a.ixigua.com/7b3478a52e156c31247fb0f3f9668748/5f94f2d2/video/tos/cn/tos-cn-ve-15/49c115d18ccf48468ae9ae9d0380be32/?a=1128&br=3744&bt=1248&cr=0&cs=0&dr=0&ds=3&er=&l=2020102509533501019806620126E5BA74&lr=aweme_search_suffix&mime_type=video_mp4&qs=0&rc=MzZrZnNzN3c1eDMzZWkzM0ApZDVmNzpoZTtkN2U2ZDY3ZWdlMm41azBiaF5fLS1jLTBzczMuYTBjLzVgXmM2MzJhYGM6Yw%3D%3D&vl=&vr='
                 ]
pv_list = ['htm', 'html', 'php', 'asp', 'shtm', 'shtml', 'aspx', 'xml', 'xhtml', 'xsl', 'cfm', 'htx', 'htmls', 'phtml',
           'jsp', 'hph3', 'txt', 'wml', 'lhtml', 'pl', 'cgi', 'cfm', 'acgi', 'srch', 'qry']


def get_referer():
    referer_list = []
    head_refererList = []
    node_referer_list = []
    for re in referer_list1:
        if re == '' or re == '-':
            referer_list.append(re)
        else:
            temp1 = re.split('//')
            temp2 = temp1[1].split('/')
            domain_referer = temp1[0] + '//' + temp2[0]
            head_refererList.append(domain_referer)
            for i in range(len(temp2) - 1):
                node_referer_list.append(temp2[i + 1])
    for head in head_refererList:
        referer_list.append(head + '/' + random.choice(node_referer_list))
        referer_list.append(head + '/' + random.choice(node_referer_list) + '/' + random.choice(node_referer_list))
        referer_list.append(head)
        referer_list.append(head + '/' + random.choice(node_referer_list) + '/' + random.choice(
            node_referer_list) + '/' + random.choice(node_referer_list) + '/' + random.choice(node_referer_list))
        referer_list.append(head + '/' + random.choice(node_referer_list) + '/' + random.choice(
            node_referer_list) + '/' + random.choice(node_referer_list))
        referer_list.append(head + '/' + random.choice(node_referer_list) + '/' + random.choice(
            node_referer_list) + '/' + random.choice(node_referer_list) + '/' + random.choice(
            node_referer_list) + '/' + random.choice(node_referer_list))

    return referer_list


def random_int(scope):
    """
    获取随机整型数据
    :param scope: 数据范围
    :return:
    """
    try:
        start_num, end_num = scope.split(",")
        start_num = int(start_num)
        end_num = int(end_num)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数有误！\n %s" % str(scope))
    if start_num <= end_num:
        num = random.randint(start_num, end_num)
    else:
        num = random.randint(end_num, start_num)
    return str(num)


def random_string(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


# def write_to_kafka(filename='data/sample.log', topic='akamaiYun'):
#     username = 'DebugTopic'
#     password = 'ThisisTheDebugUser147@201907'
#     producer = KafkaProducer(bootstrap_servers=server_list, security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN',
#                              sasl_plain_username=username, sasl_plain_password=password, \
#                              retries=5)
def write_to_kafka(filename='data/sample.log', topic='akamaiYun'):
    # 测试环境的账号密码
    admin = 'admin'
    admin_pwd = 'admin-sec'
    producer = KafkaProducer(bootstrap_servers=server_list, security_protocol="SASL_PLAINTEXT",
                             sasl_mechanism='PLAIN',
                             sasl_plain_username=admin, sasl_plain_password=admin_pwd, \
                             retries=5)
    global succ
    global err
    succ = 0
    err = 0
    i = 0
    cnt = 0
    with open(filename, 'rb') as fd:
        for line in fd.readlines():
            cnt += 1
            if cnt > 10000:
                cnt = 0
                producer.flush()
            try:
                producer.send(topic, line.strip()).add_callback(on_send_success).add_errback(on_send_error)
                i += 1
            except Exception as e:
                # err += 1
                print(str(e))
        fd.close()
    producer.flush()
    print("filename: %s, topic: %s, write: %s, succ: %s, failed: %s " % (filename, topic, i, succ, err))


def generate_normal_log(filename='data/test.log', channel='zhongzh.test.com', topic='ctYun', flag=0):
    fd = open(filename, 'w+')

    now = int(time.time() // 300 * 300)
    # requestTime = time.strftime("%d/%b/%Y:%H:%M:%S +0800", time.localtime(now))
    fd.write(str(now))
    fd.write("\n")
    cnt = 0
    # 本地的，广东电信，江西教育网，河北电信，鹏博士，铁通，科技网, 各省份
    clientIp_list = ['210.35.144.', '125.88.39.',
                     '222.222.169.', '192.168.0.', '49.222.112.', '110.201.112.', '159.226.159.', '114.44.227.',
                     '202.167.235.',
                     '61.139.0.', '222.59.0.', '120.27.128.', '59.79.112.', '58.44.0.', '58.49.128.', '58.30.0.',
                     '36.111.140.', '58.39.1.', '60.13.64.']
    httpcode_list = {'200': 88, '301': 1, '400': 1, '501': 1, '403': 1, '502': 1, '304': 1, '206': 1, '500': 1,
                     '401': 1, '302': 1, '404': 1, '416': 1}
    status_list = {'HIT': 90, 'MISS': 10}
    day_time = int(time.mktime(datetime.now().date().timetuple()))
    for timestamp in range(day_time, now, 100):
        cnt += 1
        # clientIp = random.choice(clientIp_list)+random_int('1,254')
        httpcode = random_weight(httpcode_list)
        referer2 = random.choice(get_referer())
        status = random_weight(status_list)
        day_time = int(time.mktime(datetime.now().date().timetuple()))
        temp = timestamp - day_time
        interal = int(temp / 300)
        flow = int(flow_list[interal] * 1250)
        # url_type = ['video', 'image', 'txt']
        url_type = {'video': 90, 'image': 5, 'txt': 5}
        type = random_weight(url_type)
        if channel in ['cmq002.ksedu.cn', 'cmq004.test004.cn']:
            url = '/' + random_string(32) + '/' + random_string(8) + '/' + type + '/tos/cn/tos-ve-cn-' + random_int(
                '10, 10000') + '/'
        elif channel == 'cmq003.ksedu.cn':
            url = '/' + random_string(8) + '.' + random.choice(pv_list)
        elif channel == 'tt.cmqtest.com':
            url = '/' + random_string(8) + '.'
        else:
            url = '/' + random_string(8) + '.'
        for i in range(0, 10):
            clientIp = random.choice(clientIp_list) + random_int('1,254')
            log_sample = {"serverIp": "14.215.109.226",
                          "timestamp": str(timestamp),
                          "respondTime": 1,
                          "httpCode": httpcode, "eventTime": "00:00:04", "clientIp": clientIp, "clientPort": "27051",
                          "method": "GET", "protocol": "http",
                          "channel": channel,
                          "url": "http://" + channel + url,
                          "httpVersion": "HTTP/1.1",
                          "bodyBytes": "5120",
                          "destIp": "0", "destPort": "8080",
                          "status": status,
                          "referer": referer2, "Ua": "okhttp/2.7.5-zhongzh", "fileType": "text/html",
                          "host_name": "14.215.109.226", "source_ip": "14.215.109.226", "source_id": topic,
                          "source_old": "new",
                          "type": topic,
                          'tcpinfo_rtt': "2210",
                          'tcpinfo_rttvar': "tcpinfo --- rttvar",
                          'qypid': '271',
                          'qyid': '55271',
                          'completion': 'completion'}
            if type == 'video':
                log_sample["bodyBytes"] = flow
            elif type == 'image':
                log_sample["bodyBytes"] = 1250000
            else:
                log_sample["bodyBytes"] = 125000
            # 构造一个流量抛物线
            # if timestamp < (now - 4 * 3600):
            #     log_sample["bodyBytes"] = int(timestamp) * 1000
            # else:
            #     log_sample["bodyBytes"] = int(now - timestamp) * 1000
            fd.write(json.dumps(log_sample))
            fd.write("\n")
    fd.close()
    if flag:
        write_to_kafka(filename, topic)


def work(n):
    tp = 'ctYun'
    timestamp = str(time.time() // 300 * 300)

    # zhouqi_domain_list = ['www.test007.cn', 'zq28.spdb.pay.jclinx.com', 'a.ss.baidu.com', 'b.ss.baidu.com',
    #                       'cmq004.test004.cn']
    fan_domain_list = ['cmq003.ksedu.cn', 'tt.cmqtest.com', 'c.cmqtest07.com', 'cmq004.test004.cn', 'cmq002.ksedu.cn',
                       'V1_Test_HtoW.zhihu.com ']
    for domain in fan_domain_list:
        filepath = "C:\python37\Scripts\logsystem\data/" + domain + "_" + str(timestamp) + "_" + str(n) + ".log"
        generate_normal_log(filepath, domain, tp, 1)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(n, now)


def multi_thread(num):
    """
    简易多线程
    :param num:
    :return:
    """
    i = 0
    while (i < int(num)):
        thread = threading.Thread(target=work, args=('thread-' + num,))
        thread.start()
        i = i + 1
        time.sleep(1)


def multi_write_to_kafka(func, file_prefix, dm_list, topic, flag, n):
    process_list = []
    for dm in dm_list:
        for i in range(0, n):
            timestamp = str(time.time() // 300 * 300)
            p = Process(target=func,
                        args=(file_prefix + str(dm) + "_" + timestamp + "_" + str(i) + ".log", dm, topic, flag,))
            p.start()
            process_list.append(p)
            print(dm, i)
    for p in process_list:
        p.join()


if __name__ == '__main__':
    # multi_thread(1)
    dm_list = ['cmq003.ksedu.cn', 'cmq004.test004.cn']
    file_prefix = "C:\python37\Scripts\logsystem\data/"
    topic = "ctYun"
    flag = 1
    n = 1
    func = generate_normal_log

    # multi_write_to_kafka(func, file_prefix, dm_list, topic, flag, n)
    work(1)

