# -*- coding: utf-8 -*-

from bin.Sha256Ext import get_form_head,post_form_head,post_json_head
from bin.unit.Rondom import random_string
# from bin.Mysql import DbConnect
from bin.Init import Init
import allure
import pytest


@allure.feature("客户控制台v1接口证书接口测试")
class TestCert:

    def setup_class(self):
        print('test start')
        self.v1_info = Init.V1_INFO
        self.base_info = Init.V1_BASE_INFO
        self.host = self.base_info["host"]
        self.ctyunacctid = self.base_info["ctyunAcctId"]
        self.email = self.base_info["email"]
        self.cert = self.base_info["cert"]
        self.public_key = Init.PUBLIC_ZHIHUA_KEY
        self.pravate_key = Init.PRIVATE_KEY_ZHIHUA
        self.expire_crt = Init.PUBLIC_KEY_EXPIRE
        self.expire_private_key = Init.PRIVATE_KEY_EXPIRE
        # self.db = DbConnect()

    def teardown_class(self):
        # 做清数据，退出登录等
        # self.db.close()
        print('test end')

    @allure.testcase("创建证书--查询--删除证书--证书列表")
    def test_CDN_241170(self):
        createcert_url = self.v1_info["createCert"]
        getcert_url = self.v1_info["getCert"]
        deletecert_url = self.v1_info["deleteCert"]
        certlist_url = self.v1_info["certList"]
        cert_name = "V1_Test_" + random_string(3)
        print("证书名称：" + cert_name)
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":self.public_key,
            "key":self.pravate_key,
            "email":self.email
        }
        response = post_form_head(self.host,createcert_url,data)
        print("请求url：" + str(createcert_url))
        print("返回：" + str(response.text))
        assert "服务调用成功" in response.text

        # 数据库验证，新增证书是否落库
        # 环境分隔，不再校验
        # sql = "SELECT * FROM `ecfSecret`.`certificate_metadata` where name = \"%s\"" % cert_name
        # r = self.db.select(sql)
        # print("查询结果：",sql)
        # assert cert_name in r[0]["name"]

        # 查询证书
        get_cert_data = {
            "ctyunAcctId":self.ctyunacctid,
            "secretName":cert_name
        }
        get_cert_response = post_form_head(self.host,getcert_url,get_cert_data)
        print(get_cert_response.text)
        print("请求url：" + str(getcert_url))
        print("返回：" + str(get_cert_response.text))
        print("重点校验：" + cert_name + "except:返回里有证书名")
        assert "服务调用成功" in response.text
        assert cert_name in get_cert_response.text

        # 删除证书
        delete_cert_data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name
        }
        delete_cert_response = post_form_head(self.host,deletecert_url,delete_cert_data)
        print(delete_cert_response.text)
        print("请求url：" + str(deletecert_url))
        print("返回：" + str(delete_cert_response.text))
        assert "服务调用成功" in response.text

        # # 数据库验证
        # del_r = self.db.select(sql)
        # print("删除证书后查询结果：",del_r)
        # assert del_r == ()

        # 证书列表
        cert_list_response = get_form_head(self.host,self.ctyunacctid,certlist_url)
        print(cert_list_response.text)
        print("请求url：" + str(certlist_url))
        print("返回：" + str(cert_list_response.text))
        print("重点校验：" + cert_name + "except:返回里有无证书名")
        assert cert_name not in cert_list_response.text

    @allure.testcase("查询证书域名组")
    # @pytest.mark.skip("调试ok") # 跳过该测试
    def test_CDN_241171(self):
        domain_cert_url = self.v1_info["listdomainbyCert"]

        # 查询证书对应的域名组
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":self.cert
        }
        domain_cert_response = post_form_head(self.host,domain_cert_url,data)
        print(domain_cert_response.text)
        print("请求url：" + str(domain_cert_url))
        print("返回：" + str(domain_cert_response.text))
        print("重点校验：" + self.cert + "except:返回里有域名组")
        assert "服务调用成功" in domain_cert_response.text

    @allure.testcase("新增同名证书")
    def test_CDN_241172(self):
        createcert_url = self.v1_info["createCert"]
        cert_name = "V1_Test_" + random_string(3)
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":self.public_key,
            "key":self.pravate_key,
            "email":self.email
        }
        response = post_form_head(self.host,createcert_url,data)
        print("请求url：" + str(createcert_url))
        print("返回：" + str(response.text))
        assert "服务调用成功" in response.text

        samename_data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":self.public_key,
            "key":self.pravate_key,
            "email":self.email
        }
        same_response = post_form_head(self.host,createcert_url,samename_data)
        print("请求url：" + str(createcert_url))
        print("请求数据：" + str(samename_data))
        print("返回：" + str(same_response.text))
        assert "新增证书异常：已存在重名的证书" in same_response.text

    @allure.testcase("新增过期证书")
    def test_CDN_241173(self):
        createcert_url = self.v1_info["createCert"]
        cert_name = "V1_Test_" + random_string(3)
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":self.expire_crt,
            "key":self.expire_private_key,
            "email":self.email
        }
        response = post_form_head(self.host,createcert_url,data)
        print("请求url：" + str(createcert_url))
        print("返回：" + str(response.text))
        assert "新增证书异常：证书已过期" in response.text

    @allure.testcase("新增格式错误证书")
    def test_CDN_241174(self):
        createcert_url = self.v1_info["createCert"]
        cert_name = "V1_Test_" + random_string(3)
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":"abc",
            "key":"abc",
            "email":self.email
        }
        response = post_form_head(self.host,createcert_url,data)
        print("请求url：" + str(createcert_url))
        print("返回：" + str(response.text))
        assert "新增证书异常：tls: failed to find any PEM data in certificate input" in response.text

    @allure.testcase("新增公私钥不匹配证书")
    def test_CDN_241175(self):
        createcert_url = self.v1_info["createCert"]
        cert_name = "V1_Test_" + random_string(3)
        data = {
            "ctyunAcctId":self.ctyunacctid,
            "name":cert_name,
            "certs":self.public_key,
            "key":self.expire_private_key,
            "email":self.email
        }
        response = post_form_head(self.host,createcert_url,data)
        print("请求url：" + str(createcert_url))
        print("返回：" + str(response.text))
        assert "新增证书异常：tls: private key does not match public key" in response.text






