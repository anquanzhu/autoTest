# -*- coding: utf-8 -*-
from bin.Yaml import choose_v1yaml
import requests
import time
import hmac
import base64
import hashlib

'''
python3.6.8 与 python 2.x相比较

编码的转化：python3.x 默认是Unicode字符集

1.hmac.new(key,content) 需要key，content 由 str类型 转换成 bytes类型
2.t_now = int(int(now) / 86400000)  向下取整数
'''

v1_info = choose_v1yaml()

# 定义常量
# 框架鉴权使用
APP = v1_info['APP']
APP_SECRET = v1_info['APP_SECRET']
AC = v1_info['AC']

# 业务鉴权使用
CLIENT_APP_SECRET = APP_SECRET
CLIENT_KEY_ID = APP


def decode(key, content):
    acc_key = key + "==="
    h = hmac.new(
        base64.urlsafe_b64decode(acc_key.encode("utf-8")),
        content.encode("utf-8"),
        hashlib.sha256
    )
    s = (base64.urlsafe_b64encode(h.digest())).decode("utf-8")
    signature = s.replace("=", "")
    return signature


def client_sign(key, content=""):
    h = hmac.new(key.encode("utf-8"), content.encode("utf-8"), hashlib.sha256)
    client_signature = base64.b64encode(h.digest())
    return client_signature


def get_form_head(host, ctyunid, url, params=""):
    """
    资源验证-GET
    :param host:
    :param ctyunid:
    :param url:
    :param params:
    :return:
    """
    now = str(int(round(time.time() * 1000)))
    # print("now：" + str(now))

    if not params:
        form_params = "?ctyunAcctId=" + ctyunid
        sign_str = APP + "\n" + now + "\n" + url + form_params
    else:
        form_params = "?ctyunAcctId=" + ctyunid + "&" + params
        sign_str = APP + "\n" + now + "\n" + url + form_params

    # print("sign_str：" + str(sign_str))

    t_now = int(int(now) / 86400000)
    # print("t_now：" + str(t_now))

    app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
    # print(app_secret2,type(app_secret2))

    signature = decode(app_secret2, sign_str)
    # print(signature,type(signature))

    headers = {
        "x-alogic-now": now,
        "x-alogic-app": APP,
        "x-alogic-signature": signature,
        "x-alogic-ac": AC
    }
    # print("headers：" + str(headers))
    print(host + url + form_params)
    try:
        response = requests.get(host + url + form_params, headers=headers, verify=False,timeout=10)

    # 增加超时重试
    except Exception as e:
        print("响应超时，重跑一次：{}".format(e))
        now = str(int(round(time.time() * 1000)))
        if not params:
            form_params = "?ctyunAcctId=" + ctyunid
            sign_str = APP + "\n" + now + "\n" + url + form_params
        else:
            form_params = "?ctyunAcctId=" + ctyunid + "&" + params
            sign_str = APP + "\n" + now + "\n" + url + form_params
        t_now = int(int(now) / 86400000)
        app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
        signature = decode(app_secret2, sign_str)
        headers = {
            "x-alogic-now": now,
            "x-alogic-app": APP,
            "x-alogic-signature": signature,
            "x-alogic-ac": AC
        }
        print(host + url + form_params)
        response = requests.get(host + url + form_params, headers=headers, verify=False,timeout=15)

    return response


def post_form_head(host, url, data, content=""):
    """
    资源验证-POST
    :param host:
    :param url:
    :param data:
    :param content:
    :return:
    """
    now = str(int(round(time.time() * 1000)))
    sign_str = APP + "\n" + now + "\n" + url
    t_now = int(int(now) / 86400000)
    app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
    signature = decode(app_secret2, sign_str)
    headers = {
        "x-alogic-now": now,
        "x-alogic-app": APP,
        "x-alogic-signature": signature,
        "x-alogic-ac": AC
    }
    # print("headers：" + str(headers))

    # 该签名无实际作用，暂注释掉
    # client_signature = client_sign(CLIENT_APP_SECRET)
    # dict(data)["signature"] = client_signature
    # dict(data)["keyId"] = CLIENT_KEY_ID
    try:
        response = requests.post(host + url, data=data, headers=headers, verify=False,timeout=10)

    # 增加超时重试
    except Exception as e:
        print("响应超时，重跑一次：{}".format(e))
        now = str(int(round(time.time() * 1000)))
        sign_str = APP + "\n" + now + "\n" + url
        t_now = int(int(now) / 86400000)
        app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
        signature = decode(app_secret2, sign_str)
        headers = {
            "x-alogic-now": now,
            "x-alogic-app": APP,
            "x-alogic-signature": signature,
            "x-alogic-ac": AC
        }
        response = requests.post(host + url, data=data, headers=headers, verify=False,timeout=15)

    return response


def post_json_head(host, url, data, content=""):
    """
    资源验证-POST
    :param host:
    :param url:
    :param data:
    :param content:
    :return:
    """
    now = str(int(round(time.time() * 1000)))
    sign_str = APP + "\n" + now + "\n" + url
    t_now = int(int(now) / 86400000)
    app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
    signature = decode(app_secret2, sign_str)
    headers = {
        "x-alogic-now": now,
        "x-alogic-app": APP,
        "x-alogic-signature": signature,
        "x-alogic-ac": AC
    }
    print("headers：" + str(headers))

    # 该签名无实际作用，暂注释掉
    # client_signature = client_sign(CLIENT_APP_SECRET)
    # dict(data)["signature"] = client_signature
    # dict(data)["keyId"] = CLIENT_KEY_ID
    try:
        response = requests.post(host + url, json=data, headers=headers, verify=False,timeout=10)

    # 增加超时重试
    except Exception as e:
        print("响应超时，重跑一次：{}".format(e))
        now = str(int(round(time.time() * 1000)))
        sign_str = APP + "\n" + now + "\n" + url
        t_now = int(int(now) / 86400000)
        app_secret2 = decode(APP_SECRET, APP + ":" + str(t_now))
        signature = decode(app_secret2, sign_str)
        headers = {
            "x-alogic-now": now,
            "x-alogic-app": APP,
            "x-alogic-signature": signature,
            "x-alogic-ac": AC
        }
        response = requests.post(host + url, json=data, headers=headers, verify=False,timeout=15)

    return response
