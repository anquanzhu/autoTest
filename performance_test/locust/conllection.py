from bin.Yaml import get_env
from locust import events, TaskSet, task, HttpLocust
from gevent._semaphore import Semaphore

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()


events.hatch_complete += on_hatch_complete
env = get_env()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    # "Connection": "close"
}


class TestTask(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled
            所有压测的task执行之前等待登录完成
        """
        self.console_host = 'https://iam-test.ctcdn.cn'
        self.workspace_id = "10003885"
        self.login()
        all_locusts_spawned.wait()

    def on_stop(self):
        pass

    @task(10)
    def a_page(self):
        pass

    @task(20)
    def b_page(self):
        api = '/cdn/gw/flowpacket/ProductV3'
        data = 'workspaceId=' + self.workspace_id
        payload = {}
        url = api + '?' + data
        with self.client.post(url=url, data=payload, headers=headers, catch_response=True,
                              name="login_api") as res:
            if res.status_code != 200:
                res.failure("Failed")  # 如果该条用例的状态不是200，将该条用例标记为失败

    def login(self):
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
            session_test = self.client
            session_test.post(login_url, parm, headers=headers, verify=False)
            session_test.get(self.base_info['vipAuthHost'], headers=headers, verify=False)
            # session_test.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_test.cookies.get_dict())
            print(session_test.cookies)
            return session_test

        elif env == "ATE" or env == 'ate':
            login_url = self.base_info['loginHost']
            parm = self.base_info['loginInfo']
            session_auto = self.client
            session_auto.post(login_url, parm, headers=headers, verify=False)
            session_auto.get(self.base_info['vipAuthHost'], headers=headers, verify=False)
            # session_auto.get(self.config.sessionHost_test, headers=header, verify=False)
            self.log.info('cookies: %s' % session_auto.cookies.get_dict())
            print(session_auto.cookies)
            return session_auto


        elif env == "pe" or env == 'PE':
            login_url = self.base_info['loginHost']
            parm = self.base_info['loginInfo']
            session_product = self.client
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


class User(HttpLocust):  # 用户类
    task_set = TestTask
    min_wait = 1000  # 毫秒
    max_wait = 2000  # 毫秒
    stop_timeout = 60  # 单位秒，运行时间
    host = 'https://iam-test.ctcdn.cn'
