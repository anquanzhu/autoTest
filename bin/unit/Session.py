# -*- coding: utf-8 -*-


"""
登录，使用session发送请求；

"""
import json
import time

import requests
# from bin.Init import Init
from bin.Yaml import choose_Yaml, readYaml, get_env
from bin.unit import Log
from bin.unit.Rondom import get_time

env = get_env()


class Session():
    def __init__(self):
        self.log = Log.Log()
        self.base_info = choose_Yaml()

    def get_session(self):
        """
        获取客户控制台session
        :param env: 环境变量
        :return:
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Connection": "close"
        }
        if env == "ITE" or env == 'ite':
            login_url = self.base_info['loginHost']
            parm = self.base_info['loginInfo']
            session_test = requests.session()
            session_test.post(login_url, parm, headers=headers, verify=False)
            session_test.get(self.base_info['vipAuthHost'], headers=headers, verify=False)
            # session_test.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            print(session_test.cookies)
            return session_test

        elif env == "ATE" or env == 'ate':
            login_url = self.base_info['loginHost']
            parm = self.base_info['loginInfo']
            session_auto = requests.session()
            session_auto.post(login_url, parm, headers=headers, verify=False)
            session_auto.get(self.base_info['vipAuthHost'], headers=headers, verify=False)
            # session_auto.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            print(session_auto.cookies)
            return session_auto


        elif env == "pe" or env == 'PE':
            login_url = self.base_info['loginHost']
            parm = self.base_info['loginInfo']
            session_product = requests.session()
            session_product.post(login_url, parm, headers=headers, verify=False)
            session_product.get(self.base_info['vipAuthHost'], headers=headers, verify=False)
            self.log.info('cookies: %s' % session_product.cookies.get_dict())
            # 调试cookie 是否有效
            # re = session_product.get(
            #     'https://console.ctcdn.cn/iam/gw/workspace/menu/GetTree?domain=cdn.header.dropdown&locale=zh-cn&workspaceId=10002005',
            #     verify=False)
            print(session_product.cookies)
            # print(re.text)
            return session_product

        else:
            print("get cookies error")
            self.log.error('get cookies error, please checkout!!!')

    def get_iam_private_session(self):
        '''
        获取工单系统的登录session
        工单系统没有生产环境权限，故不用
        :return: session
        '''
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEzfQ.zWkVj5oehTUt9l0_O3i_o1i4wtoo7Aj21j0HWVD95bs"
        }

        if env == "ITE" or env == 'ite':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            session_test = requests.session()
            session_test.post(login_url, parm, headers=header, verify=False)
            auth_url = self.base_info['workOrderAuthHost']
            session_test.get(url=auth_url, headers=header, verify=False)
            print(session_test.cookies.get_dict())
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            # data = '{"work_order":{"order_title":"Auto-random-f403.ctyun.cn","sort":"desc","current_staff_id":"20","status_cd":"orderOnway"},"paging":{"page":1,"per_page":10}}'
            # ss=session_test.post(url='http://work-order-test.ctyuncdn.cn/v1/workorder/searchWorkOrder', data=data,headers=header,)
            # print(ss.text)
            return session_test

        elif env == "ATE" or env == 'ate':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            session_auto = requests.session()
            session_auto.post(login_url, parm, headers=header, verify=False)
            # session_product.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            print(session_auto.cookies)
            return session_auto

        else:
            print("get cookies error")
            self.log.error('get cookies error, please checkout!!!')

    def get_bs_session(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                          Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if env == 'ITE' or env == 'ite':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            session_test = requests.session()
            session_test.post(login_url, parm, headers=header, verify=False)
            # session_test.get('http://work-order-test.ctyuncdn.cn/v1/auth/getUserInfo', headers=header, verify=False)
            session_test.get(auth_url, headers=header, verify=False)
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            # re = session_test.get(
            #     'http://bs-test.ctyuncdn.cn/api/v3/sysParam/getIamSwitch'
            #     )
            # print(re.text)
            # print(session_test.cookies)
            return session_test

        elif env == 'ATE' or env == 'ate':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            session_auto = requests.session()
            session_auto.post(login_url, parm, headers=header, verify=False)
            session_auto.get('http://work-order-test.ctyuncdn.cn/v1/auth/getUserInfo', headers=header, verify=False)
            session_auto.get(auth_url, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            re = session_auto.get(url='http://bs-test.ctyuncdn.cn/api/v1/ticket/domain/list',
                                  params='check_status=2&status=&action=&page_size=20&page=1&domain=Auto-random-eA12.ctyun.cn')
            print(re.text)
            print(session_auto.cookies)
            return session_auto

        elif env == 'PE' or env == 'pe':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            session_product = requests.session()
            session_product.post(login_url, parm, headers=header, verify=False)
            # session_product.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_product.cookies.get_dict())
            print(session_product.cookies)
            return session_product
        else:
            print("get cookies error")
            self.log.error('get cookies error, please checkout!!!')

    def get_ctyun_session(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                                  Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if env == 'ITE' or env == 'ite':
            login_url = self.base_info['ctyunLoginUrl']
            parm = self.base_info['ctyun_loginInfo']
            ctyun_auth = 'https://cdn-test-new.ctyun.cn/cdn/console/index.html'
            session_test = requests.session()
            login_rep = session_test.post(login_url, params=parm, headers=header, verify=False)
            # print(login_rep.text)

            # session_test.get(url=au, headers=header, verify=False)
            session_test.get(url=ctyun_auth, headers=header, verify=False)
            # session_test.get(url=env_auth, headers=header, verify=False)
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            # re = session_test.get(
            #     url='https://cdn-test-new.ctyun.cn/cdn/gw/cert/CertList?workspaceId=10039265&page=1&perPage=10',
            #     headers=header,
            #     verify=False
            # )
            # print(re.text)
            # print('222', session_test.cookies)
            return session_test

        elif env == 'ATE' or env == 'ate':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            session_auto = requests.session()
            session_auto.post(login_url, parm, headers=header, verify=False)
            session_auto.get('http://work-order-test.ctyuncdn.cn/v1/auth/getUserInfo', headers=header, verify=False)
            session_auto.get(auth_url, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            re = session_auto.get(url='http://bs-test.ctyuncdn.cn/api/v1/ticket/domain/list',
                                  params='check_status=2&status=&action=&page_size=20&page=1&domain=Auto-random-eA12.ctyun.cn')
            # print(re.text)
            print(session_auto.cookies)
            return session_auto

        elif env == 'PE' or env == 'pe':
            login_url = self.base_info['ctyunLoginUrl']
            parm = self.base_info['ctyun_loginInfo']
            ctyun_auth = 'https://cdn.ctyun.cn/cdn/console/index.html'
            session_product = requests.session()
            session_product.post(login_url, params=parm, headers=header, verify=False)
            session_product.get(url=ctyun_auth, headers=header, verify=False)
            self.log.info('cookies: %s' % session_product.cookies.get_dict())
            # re = session_product.get(
            #     url='https://cdn.ctyun.cn/cdn/gw/cert/CertList?workspaceId=10039265&page=1&perPage=10',
            #     headers=header,
            #     verify=False
            # )
            # print(re.text)
            # print('222', session_product.cookies)
            return session_product
        else:
            print("get cookies error")
            self.log.error('get cookies error, please checkout!!!')

    def get_bs_console_session(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if env == 'ITE' or env == 'ite':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            accountId = self.base_info['ctyunAcctId']
            bsUserName = self.base_info['bsUserName']
            requests.session().close()
            session_test = requests.session()
            session_test.post(login_url, parm, headers=header, verify=False)
            # session_test.get('http://work-order-test.ctyuncdn.cn/v1/auth/getUserInfo', headers=header, verify=False)
            session_test.get(auth_url, headers=header, verify=False)
            # print(re.text)
            # print(session_test.cookies)
            bs_console_url = 'http://bs-test.ctyuncdn.cn/api/v1/account/console/' + accountId
            payload = {"username": bsUserName}
            re1 = session_test.post(bs_console_url, data=json.dumps(payload), headers=header)
            console_url = json.loads(re1.text)['data']
            # print(console_url)
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            session_test.get(console_url)
            # 调试部分
            # re2 = session_test.get(
            #     'http://bs-test.ctyuncdn.cn/bs/cdn/gw/domain/ListDomain?workspaceId=ba69d44a5ea847be85ffe3f486f087db&page=1&page_size=10000'
            # )
            # print("1: ", re1.text)
            # print("2: ", re2.text)
            # print(session_test.cookies)
            return session_test

        elif env == 'ATE' or env == 'ate':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            session_auto = requests.session()
            session_auto.post(login_url, parm, headers=header, verify=False)
            session_auto.get('http://work-order-test.ctyuncdn.cn/v1/auth/getUserInfo', headers=header, verify=False)
            session_auto.get(auth_url, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            re = session_auto.get(url='http://bs-test.ctyuncdn.cn/api/v1/ticket/domain/list',
                                  params='check_status=2&status=&action=&page_size=20&page=1&domain=Auto-random-eA12.ctyun.cn')
            # print(re.text)
            print(session_auto.cookies)
            return session_auto

        elif env == 'PE' or env == 'pe':
            login_url = self.base_info['iamPrivateHost']
            parm = self.base_info['iam_loginInfo']
            auth_url = self.base_info['bsAuthHost']
            accountId = self.base_info['ctyunAcctId']
            bsUserName = self.base_info['bsUserName']
            requests.session().close()
            session_product = requests.session()
            session_product.post(login_url, parm, headers=header, verify=False)
            session_product.get(auth_url, headers=header, verify=False)
            # 'http://bs.ctcdn.cn/api/v1/account/console/5c3882acf16e4b90b190dddc1acf6d2a'
            bs_console_url = 'http://bs.ctcdn.cn/api/v1/account/console/' + accountId
            payload = {"username": bsUserName}
            re_bs_redirect = session_product.post(bs_console_url, data=json.dumps(payload), headers=header)
            # print('BS_URL: ', re_bs_redirect.text)
            console_url = json.loads(re_bs_redirect.text)['data']
            # print(console_url)
            # self.log.info('cookies: %s' % session_product.cookies.get_dict())
            session_product.get(console_url)
            # 调试部分
            # re2 = session_product.get(
            #     'http://bs.ctcdn.cn/bs/cdn/gw/domain/ListDomain?workspaceId=5c3882acf16e4b90b190dddc1acf6d2a&page=1&page_size=10000'
            # )
            # print("2: ", re2.text)
            print(session_product.cookies)
            return session_product
        else:
            print("get cookies error")
            self.log.error('get cookies error, please checkout!!!')

    # def get_auto_session(self):
    #     # 自助配置账号登录session
    #     if env == "ITE" or env == 'ite':
    #         login_url = self.base_info['loginHost']
    #         parm = self.base_info['AutoInfo']
    #         auto_session = requests.session()
    #         auto_session.post(login_url, parm, verify=False)
    #         auto_session.get(self.base_info['AutoUser_URL'], verify=False)
    #         # session_test.get(self.config.sessionHost_test, headers=header, verify=False)
    #         self.log.info('cookies: %s' % auto_session.cookies.get_dict())
    #         print(auto_session.cookies)
    #         return auto_session

if __name__ == '__main__':
    ss = Session()
    # url='http://bs-test.ctyuncdn.cn/bs/cdn/gw/domain/ListDomain?workspaceId=ba69d44a5ea847be85ffe3f486f087db&page=1&page_size=10000&_t=1601022972866'
    # re = ss.get_iam_private_session()
    # data = {"work_order":{"sort":"desc","current_staff_id":"30","status_cd":"orderOnway"},"paging":{"page":1,"per_page":10}}
    # url = "http://work-order-test.ctyuncdn.cn/v1/workorder/searchWorkOrder"
    # response = re.post(url,data)
    # print(response.text)
    # ss.get_auto_session()
