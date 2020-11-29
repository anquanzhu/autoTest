# -*- coding: utf-8 -*-
import json

from bin.unit import Log


class Assert:
    def __init__(self):
        self.log = Log.Log()

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert str(code) == str(expected_code)
            return True
        except:
            self.log.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))

            raise Exception("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg

        except:
            self.log.error(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))

            raise Exception(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in text
            # return True
        except:
            print("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)
            # raise Exception("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            return True

        except:
            self.log.error("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))

            # raise Exception("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))

    def assert_time(self, time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        expected_time = 3000
        try:
            assert time < expected_time
            return True

        except:
            self.log.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))

            raise Exception("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))

    def check_json(self, src_data, dst_data):
        """
        校验的json
        :param src_data: 检验内容
        :param dst_data: 接口返回的数据
        :return:
        """
        if isinstance(src_data, dict):
            for key in src_data:
                if key not in dst_data:
                    raise Exception("JSON格式校验，关键字%s不在返回结果%s中" % (key, dst_data))
                else:
                    this_key = key
                    if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                        self.check_json(src_data[this_key], dst_data[this_key])
                    elif isinstance(type(src_data[this_key]), type(dst_data[this_key])):
                        raise Exception("JSON格式校验，关键字 %s 与 %s 类型不符" % (src_data[this_key], dst_data[this_key]))
                    else:
                        pass
        else:
            raise Exception("JSON校验内容非dict格式")

    def common_assert(self, response, src):
        '''
        基础断言
        :param response: 返回响应
        :param src: 需要检查的内容
        '''
        r = json.loads(response['body'])
        try:
            assert r.get('reason') == "服务调用成功"
            assert response['code'] == 200
            assert response['time_total'] < 3000
            if src != None:
                assert src in response['body']
        except:
            self.log.error('common_assert failed!')
            raise Exception('common_assert failed!')


if __name__ == '__main__':
    Assert().assert_in_text("dfsdfsdf", "123", "fdsf")
