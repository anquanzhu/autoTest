# _*_ coding: utf-8 _*_


'''
    wwwtest 快速注册
    测试环境快速注册
    http://10.145.240.42/register
    快速实名
    http://203.55.10.36:15003/quickAuth?email=cmq10000@qq.com

    http://zentest.ctyun.com.cn/api/admin/ajax/userLogin
    payload={"userLoginName":"13661302499","userPassword":"@a13579A"}


    http://zentest.ctyun.com.cn/bss/create/business?loginEmail=cmq10000%40qq.com&applyAmount=10000&otherPartyName=cmq10000%40qq.com&remark=cmq10000%40qq.com
    <tr data-businessChargeId = "2f72968aea554cc9871dabb44ac6e965">
    <tr data-businessChargeId = "56851f3a735844b19d44e0607f4edd1e">
    <td>测试/cmq10000@qq.com</td>
    http://zentest.ctyun.com.cn/bss/approve/business?businessChargeId=2f72968aea554cc9871dabb44ac6e965

    http://zentest.ctyun.com.cn/bss/approve/review/business?businessChargeId=2f72968aea554cc9871dabb44ac6e965
'''
import json
import time

import requests
from bs4 import BeautifulSoup

headers_json = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/json",
}

headers_form = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                      Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}


def ctyun_test_register(email, user):
    register_url = 'http://10.145.240.42/register'
    # user_type: enterprise  user_type=personal
    if 'en' in user:
        user_type = 'enterprise'
    else:
        user_type = 'personal'
    email_de = str(email).replace('@', '%40')
    payload = 'return_url=&idtype=&csrf_test_name=0ae24f1f2a3701eef64672f1b3b3c092&email=' + email_de + '&password=a123456!&passconf=a123456!&user_type=' + user_type + '&phone_no=18933910909&auth_code=345623&reg_code=&radio1=3'
    requests.request("POST", url=register_url, data=json.dumps(payload),
                     headers=headers_form, timeout=10)
    print('注册邮箱：', email)
    print('用户类型：', user_type)


def ctyun_test_auth(email):
    auth_url = 'http://203.55.10.36:15003/quickAuth?email=' + email
    re = requests.request("POST", url=auth_url, data='',
                          headers=headers_form, timeout=10)
    if '成功' in re.text:
        print(email + '--实名成功')
    else:
        print(email + '--实名失败！！！')


def ctyun_test_recharge(email, pay):
    header_json = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    header_form = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }

    # 登录zen 系统
    zen_login_url = 'http://zentest.ctyun.com.cn/api/admin/ajax/userLogin'
    payload = {"userLoginName": "13661302499", "userPassword": "@a13579A"}
    # zen_session = requests.session()
    login_re = requests.post(zen_login_url, data=json.dumps(payload), headers=header_json, timeout=10)
    temp=login_re.headers.get('Set-Cookie')
    cookie_list=str(temp).split(';')
    # for co in cookie_list:



    header_json["Cookie"] = login_re.headers.get('Set-Cookie')
    header_form["Cookie"] = login_re.headers.get('Set-Cookie')
    print(header_json)
    time.sleep(3)
    requests.get('http://zentest.ctyun.com.cn/bss/pay/business', headers=header_json, timeout=10)  # 获取cookies

    # 充值
    recharge_url = 'http://zentest.ctyun.com.cn/bss/create/business'
    email_de = str(email).replace('@', '%40')
    payload_recharge = 'loginEmail=' + email_de + '&applyAmount=' + pay + '&otherPartyName=' + email_de + '&remark=' + email_de
    recharge_re = requests.get(recharge_url, data=json.dumps(payload_recharge), headers=header_form, timeout=10)
    print(recharge_re.text)
    soup = BeautifulSoup(recharge_re.text, 'lxml')
    links = soup.get('data-businessChargeId')
    print('L: ', links)

    # 初审+复审
    trial_url1 = 'http://zentest.ctyun.com.cn/bss/approve/business'
    trial_url2 = 'http://zentest.ctyun.com.cn/bss/approve/review/business'
    payload_trial = 'businessChargeId=' + links
    time.sleep(2)
    requests.get(trial_url1, data=json.dumps(payload_trial), headers=header_form, timeout=10)
    time.sleep(2)
    requests.get(trial_url2, data=json.dumps(payload_trial), headers=header_form, timeout=10)


if __name__ == '__main__':
    # ctyun_test_recharge()
    ctyun_test_recharge('cmq10000@qq.com', '5000')
