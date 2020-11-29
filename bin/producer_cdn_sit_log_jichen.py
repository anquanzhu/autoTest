# -*- coding: utf-8 -*-
import os
import json
import string
import time
from datetime import datetime
import random
import copy

import pymysql
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from multiprocessing import Process

# server_list = ['ctl-nm-hhht-yxxya6-dnscskf-004.ctyuncdn.net:5044', 'ctl-nm-hhht-yxxya6-rzfx2-001.ctyuncdn.net:5044']
# server_list = ['192.168.2.40:6667', '192.168.2.42:6667']
# 集成环境
server_list = ['182.140.235.58:5044', '182.140.235.59:5044']
succ = 0
err = 0


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


def random_string(num_len):
    """
    从a-zA-Z0-9生成制定数量的随机字符
    :param num_len: 字符串长度
    :return:
    """
    try:
        num_len = int(num_len)
    except ValueError:
        raise Exception("从a-zA-Z0-9生成指定数量的随机字符失败！长度参数有误  %s" % num_len)
    strings = ''.join(random.sample(string.hexdigits, +num_len))
    return strings


def write_to_kafka(filename='data/sample.log', topic='akamaiYun'):
    username = 'DebugTopic'
    password = 'ThisisTheDebugUser147@201907'
    producer = KafkaProducer(bootstrap_servers=server_list, security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN',
                             sasl_plain_username=username, sasl_plain_password=password, \
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
                future = producer.send(topic, line.strip()).add_callback(on_send_success).add_errback(on_send_error)
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
    requestTime = time.strftime("%d/%b/%Y:%H:%M:%S +0800", time.localtime(now))
    fd.write(str(now))
    fd.write("\n")
    cnt = 1
    # 本地的，广东电信，江西教育网，河北电信，鹏博士，铁通，科技网, 各省份
    clientIp_list = ['210.35.144.1', '210.35.144.2', '210.35.144.3', '210.35.144.4', '210.35.144.5', '125.88.39.164',
                     '222.222.169.89', '192.168.0.133', '49.222.112.0', '49.222.112.1', '49.222.112.2', '49.222.112.3',
                     '49.222.112.4', '49.222.112.5', '49.222.112.6', '49.222.112.7', '110.201.112.0', '110.201.112.1',
                     '110.201.112.2', '110.201.112.3', '110.201.112.4', '110.201.112.5', '110.201.112.6',
                     '110.201.112.7', '110.201.112.8', '159.226.159.0', '114.44.227.87', '202.167.235.128',
                     '61.139.0.1', '222.59.0.1', '120.27.128.1', '59.79.112.1', '58.44.0.1', '58.49.128.1', '58.30.0.1',
                     '36.111.140.26', '58.39.1.2', '60.13.64.1', '60.13.64.2', '60.13.64.3', '60.13.64.4', '60.13.64.5',
                     '60.13.64.6', '60.13.64.7', '60.13.64.8']
    httpcode_list = {'200': 90, '301': 5, '400': 2, '501': 3}
    # referer_list = {'referer1': 10, 'referer2': 2, 'referer3': 9, 'referer4': 3, 'referer5': 7, 'referer6': 8,
    #                 'referer7': 10, 'referer8': 10, 'referer9': 3, 'referer10': 10, 'referer11': 3}
    status_list = {'HIT': 90, 'MISS': 10}
    day_time = int(time.mktime(datetime.now().date().timetuple()))
    for timestamp in range(day_time, now, 100):
        cnt += 1
        clientIp = random.choice(clientIp_list)
        httpcode = random_weight(httpcode_list)
        referer_list = ['-', '']
        referer = random.choice(referer_list)
        status = random_weight(status_list)
        for i in range(0, 10):
            log_sample = {"serverIp": "14.215.109.226",
                          "timestamp": str(timestamp),
                          "respondTime": 1,
                          "httpCode": httpcode, "eventTime": "00:00:04", "clientIp": clientIp, "clientPort": "27051",
                          "method": "GET", "protocol": "http",
                          "channel": channel,
                          "url": "http://" + channel + '/' + topic + "/" + random_string(4),
                          "httpVersion": "HTTP/1.1",
                          "bodyBytes": "5120",
                          "destIp": "0", "destPort": "8080",
                          "status": status,
                          "referer": referer, "Ua": "okhttp/2.7.5-zhongzh", "fileType": "text/html",
                          "host_name": "14.215.109.226", "source_ip": "14.215.109.226", "source_id": topic,
                          "source_old": "new",
                          "type": topic,
                          'tcpinfo_rtt': "2210",
                          'tcpinfo_rttvar': "tcpinfo --- rttvar",
                          'qypid': '271',
                          'qyid': '55271',
                          'completion': 'completion'}

            log_sample["bodyBytes"] = 1000 * 1000 * 200 * 10
            fd.write(json.dumps(log_sample))
            fd.write("\n")
    fd.close()
    if flag:
        write_to_kafka(filename, topic)


def connect_db():
    info = {
        "host": "36.111.180.188",
        "user": "root",
        "password": "SJKsjk@111111",
        "port": 3306,
        "db": 'cmq',
        "charset": 'utf8'
    }
    # 连接数据库
    db = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, autocommit=True, **info)
    # 获取游标
    cursor = db.cursor()
    return cursor


def create_table(table_info={}):
    log_sample = {"serverIp": "14.215.109.226",
                  "timestamp": str(1689093485),
                  "respondTime": 100,
                  "httpCode": '200', "eventTime": "00:00:04", "clientIp": '1.1.1.1', "clientPort": "27051",
                  "method": "GET", "protocol": "http",
                  "channel": 'www.baidu.com',
                  "url": "http://" + 'www.baidu.com',
                  "httpVersion": "HTTP/1.1",
                  "bodyBytes": "5120",
                  "destIp": "0", "destPort": "8080",
                  "status": 'hit',
                  "referer": '/a/b/b', "Ua": "okhttp/2.7.5-zhongzh", "fileType": "text/html",
                  "host_name": "14.215.109.226", "source_ip": "14.215.109.226", "source_id": 'ctyun',
                  "source_old": "new",
                  "type": 'ctyun',
                  'tcpinfo_rtt': "2210",
                  'tcpinfo_rttvar': "tcpinfo --- rttvar",
                  'qypid': '271',
                  'qyid': '55271',
                  'completion': 'completion'}
    normal_list = log_sample.keys()
    print(normal_list)
    # 创建student表
    normal_log = '''
        create table normal_log(
            id int not null AUTO_INCREMENT,
            serverIp varchar(30) not null COMMENT 'serverIp',
            timestamp varchar(20) not null COMMENT '时间戳', 
            respondTime int(8) COMMENT '响应时间', 
            httpCode varchar(5) COMMENT 'httpCode',
            eventTime time COMMENT '时间',
            clientIp varchar(20) DEFAULT NULL COMMENT 'IP地址',
            clientPort varchar(8)  DEFAULT NULL COMMENT 'IP端口',
            method enum('GET','POST','PUT','DELETE') DEFAULT NULL COMMENT '请求方式',
            protocol enum('http','https') DEFAULT NULL,
            channel varchar(20) not null,
            url varchar(100) not null,
            httpVersion varchar(20)  DEFAULT NULL,
            bodyBytes varchar(10)  DEFAULT NULL,
            destIp varchar(20) DEFAULT NULL,
            destPort varchar(8) DEFAULT NULL,
            status varchar(6)  DEFAULT NULL,
            referer varchar(100) DEFAULT NULL,
            Ua varchar(20)  DEFAULT NULL,
            fileType varchar(10) DEFAULT NULL,
            host_name varchar(20) DEFAULT NULL,
            source_ip varchar(20) DEFAULT NULL,
            source_id varchar(10)  DEFAULT NULL,
            source_old varchar(8) DEFAULT NULL,
            type varchar(10)  DEFAULT NULL,
            tcpinfo_rtt varchar(10)  DEFAULT NULL,
            tcpinfo_rttvar varchar(20) DEFAULT NULL,
            qypid varchar(10)  DEFAULT NULL,
            qyid varchar(10)  DEFAULT NULL,
            completion varchar(10)  DEFAULT NULL,
            PRIMARY KEY ('id')
        )
    '''


if __name__ == '__main__':
    tp = 'ctYun'
    timestamp = str(time.time() // 300 * 300)
    # domain_list = ['cmq004.test004.cn', 'cmq002.ksedu.cn', 'cmq003.ksedu.cn', 'www.cmqtest07.com', 'rr.cmqtest.com',
    #                'tt.cmqtest.com']
    domain_list = ['V1_Test_5Ba2.zhihu.com', 'V1_Test_4Aa8.zhihua.com']
    for domain in domain_list:
        filepath = "C:\python37\Scripts\logsystem\data/" + domain + "_" + timestamp + ".log"
        generate_normal_log(filepath, domain, tp, 1)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now)
    # ---------------------
