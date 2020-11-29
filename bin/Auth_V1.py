# -*- coding: utf-8 -*-


import requests

import time

import hmac

import base64

import pytest

import json

# 定义常量

# 框架鉴权使用
from bin.Init import Init

# URL = "https://iam-test.ctcdn.cn/cdn/gw/v1/cert/Get?ctyunAcctId=0dba69812ab444c4adc90edbf080b210&secretName=zq-pt"

base_info = Init.BASE_INFO
# ctyun_id = "0dba69812ab444c4adc90edbf080b210"
ctyun_id = base_info['ctyunAcctId']
APP = base_info['APP']
APP_SECRET = base_info['APP_SECRET']
AC = base_info['AC']
API = Init.V1_INFO['getCert']
API1 = Init.V1_INFO['createCert']
# 业务鉴权使用

CLIENT_APP_SECRET = APP_SECRET

CLIENT_KEY_ID = APP

public_key_365 = Init.PUBLIC_KEY
private_key_365 = Init.PRIVATE_KEY


def decode(key, content):
    h = hmac.new(

        bytes(base64.urlsafe_b64decode(key + "===")),

        bytes(content.encode('utf-8')),

        'SHA256'

    ).digest()
    #
    # print('h=', h)
    # print(type(h))

    temp = str(base64.urlsafe_b64encode(bytes(h))).replace('=', '')
    # print("temp:",temp)
    # print("count:", len(temp))

    signature = temp[2:-1]
    # print("count2: ",len(signature))
    print("sign: ", signature)

    return signature


def get_client_sign(key, content):
    h = hmac.new(

        bytes(key.encode('utf-8')),

        bytes(content.encode('utf-8')),

        'SHA256'

    ).digest()

    client_sign = str(base64.b64encode(bytes(h)))[2:-1]

    print('ss', client_sign)
    print(type(client_sign))
    print(len(client_sign))

    return client_sign


def get_head(api, params):
    """

    业务资源验证

    :return:

    """

    now = str(int(round(time.time() * 1000)))

    sign_str = APP + "\n" + now + "\n" + api + '?' + params

    print(sign_str)

    temp = int(now) / 86400000  # 这里和Py2 不一样，得到的是一个float小数

    t_now = int(temp)

    print('t_now=', t_now)

    APP_SECRET2 = decode(APP_SECRET, APP + ":" + str(t_now))

    print('APP_SECRET2=', APP_SECRET2)

    signature = decode(APP_SECRET2, sign_str)

    print('signature=', signature)

    # app_str = APP + ':' + now

    headers = {

        "x-alogic-now": now,

        "x-alogic-app": APP,

        "x-alogic-signature": signature,

        "x-alogic-ac": AC

    }

    print(headers)

    '''
        测试代码
    '''

    # URL = base_info['host'] + API + '?ctyunAcctId=' + ctyun_id + '&' + params
    #
    # print(URL)

    # response = requests.post(url=URL, headers=headers, verify=False)
    #
    # print(response.text)
    #
    # response = json.loads(response.text)
    #
    # if response["code"] == "core.ok":
    #
    #     return {"code": 0, "msg": "passed"}
    #
    # else:
    #
    #     return {"code": -1, "msg": response["reason"]}

    return headers


def get_json_head(api):
    """

      业务资源验证

      :return:

      """

    now = str(int(round(time.time() * 1000)))

    sign_str = APP + "\n" + now + "\n" + api

    print("sign_str:", sign_str)

    temp = int(now) / 86400000

    t_now = int(temp)

    APP_SECRET2 = decode(APP_SECRET, APP + ":" + str(t_now))

    signature = decode(APP_SECRET2, sign_str)

    # app_str = APP + ':' + now

    headers = {

        "x-alogic-now": now,

        "x-alogic-app": APP,

        "x-alogic-signature": signature,

        "x-alogic-ac": AC

    }
    # print('headers: ', headers)
    # client_signature = get_client_sign(CLIENT_APP_SECRET, '')
    #
    # print("client_signature: ", client_signature)
    # print(len(client_signature))
    '''
        测试代码
    '''

    # data = {
    #
    #     "ctyunAcctId": ctyun_id,
    #
    #     # "keyId": CLIENT_KEY_ID,
    #
    #     # "signature": client_signature,
    #     # "workspaceId": "10003885",
    #
    #     "name": "zq124000",
    #
    #     "certs": public_key_365,
    #
    #     "key": private_key_365
    #
    # }
    #
    # URL = base_info['host'] + api
    # print(URL)
    # # print(type(json.dumps(str(data))))
    # # print("data: ", json.dumps(data))
    # print("data_type:", type(data))
    # # temp = str(data)
    # print(data)
    # play_load = json.dumps(data)
    # print(play_load)
    # print(type(json.loads(play_load)))
    # print("data: ", json.loads(play_load))
    #
    # # response = requests.post(URL111, json.dumps(data), headers=headers, verify=False)
    #
    # response = requests.post(URL, headers=headers, verify=False, data=data)
    # print(response.text)
    #
    # assert 'core.ok' in response.text
    return headers


if __name__ == "__main__":
    # ret = get_form_head(content="", api=API, params='secretName=CTYUN_TEST')

    get_json_head(API1)

# get_client_sign(CLIENT_APP_SECRET, content="aaa")

# print(ret)
