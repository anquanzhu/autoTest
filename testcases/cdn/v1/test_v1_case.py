# -*- coding: utf-8 -*-

from bin.Sha256Ext import get_form_head
from bin.Yaml import readYaml, choose_v1yaml
from bin.unit.Rondom import get_time
from bin.Init import Init
import allure
import pytest


@allure.feature("客户控制台v1接口用户分析接口测试")
class TestCase(object):
    def setup_class(self):
        print('test start')
        self.v1_info = Init.V1_INFO
        self.base_info = Init.V1_BASE_INFO
        self.host = self.base_info["host"]
        self.ctyunacctid = self.base_info["ctyunAcctId"]

    def teardown_class(self):
        # 做清数据，退出登录等
        print('test end')

    @allure.testcase("查询产品列表")
    def test_CDN_241163(self):
        url = self.v1_info["productList"]
        response = get_form_head(self.host,self.ctyunacctid,url)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        print("重点校验：" + "bss_product" + "except:返回里有bss产品")
        assert "服务调用成功" in response.text
        assert "bss_product" in response.text

    @allure.testcase("查询区域列表")
    def test_CDN_241165(self):
        url = self.v1_info["areaList"]
        response = get_form_head(self.host,self.ctyunacctid,url)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        print("重点校验：" + "地区" + "except:返回里有全部地区")
        assert "服务调用成功" in response.text
        assert "全部地区" in response.text

    @allure.testcase("查询运营商列表")
    def test_CDN_241164(self):
        url = self.v1_info["ispList"]
        response = get_form_head(self.host,self.ctyunacctid,url)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        print("重点校验：" + "运营商" + "except:返回里有中国电信")
        assert "服务调用成功" in response.text
        assert "中国电信" in response.text

    @pytest.mark.skip("日志服务未通")  # 跳过测试
    @allure.testcase("查询日志列表")
    def test_CDN_241166(self):
        url = self.v1_info["logFile"]
        start_time = get_time("else", "13timestamp", "0,0,0,-30,0")
        end_time = get_time("now", "13timestamp")
        params = "startTime=%s&endTime=%s" % (start_time, end_time)
        response = get_form_head(self.host,self.ctyunacctid,url,params)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        print("重点校验：" + "日志" + "except:返回里有域名")
        assert "服务调用成功" in response.text

    # @pytest.mark.skip("用户子账号，调试ok")
    @allure.testcase("查询子用户域名列表")
    def test_CDN_241167(self):
        url = self.v1_info["listbySubuser"]
        workspaceid = self.base_info["workspaceid"]
        subuserid = self.base_info["subuserId"]
        params = "workspaceId=%s&subuserId=%s" % (workspaceid, subuserid)
        response = get_form_head(self.host,self.ctyunacctid,url,params)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        assert "服务调用成功" in response.text

    @allure.testcase("查询工作区下子用户列表")
    def test_CDN_241168(self):
        url = self.v1_info["getSubusers"]
        workspaceid = self.base_info["workspaceid"]
        params = "workspaceId=%s" % workspaceid
        response = get_form_head(self.host,self.ctyunacctid,url, params)
        print("请求url：" + str(url))
        print("返回：" + str(response.text))
        print("重点校验：" + "主账号" + "except:返回里有主账号/子账号")
        assert "服务调用成功" in response.text
        assert "主账号信息" in response.text
