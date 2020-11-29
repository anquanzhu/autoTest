# -*- coding: utf-8 -*-


import random

from bin.Yaml import choose_Yaml
from bin.unit.Rondom import random_string
from bin.unit.Session import Session

"""
说明：
Productcode：产品类型
"001"：静态加速
"003"：下载加速
"004"：视频点播加速
"005"：视频直播加速

只有视频直播加速类型产品，请求参数不同，其他类型产品一样，可复用参数

"""

productcode = ["001","003","004"]


class Domain(object):
    def __init__(self):
        self.session = Session().get_session()
        self.host = choose_Yaml()["Host"]
        self.workspaceid = choose_Yaml()["WorkspaceId"]

    def create_commin_domin(self):
        """
        创建通用域名：静态加速域名，下载加速域名，视频点播加速域名
        :return:
        """
        url = "/cdn/gw/domain/CreateDomain"
        name = "Domain_Test_" + random_string(4) + ".zhihu.com"
        data = {
                "data":{
                    "workspaceId":self.workspaceid,
                    "action":1,
                    "userName":"蔡君",
                    "domain":name,
                    "recordNum":"京ICP备13052560号",
                    "productCode":random.choice(productcode),
                    "origin":[
                        {
                            "role":"master",
                            "origin":"1.1.1.1",
                            "port":"80",
                            "weight":1,
                            "protocol":"http"
                        }
                    ],
                    "originProtocol":"http",
                    "basicConf":{
                        "follow302":0},
                    "reqHost":"cc.ctyun.com",
                    "filetypeTtl":[
                        {"fileType":"php,ashx,aspx,asp,jsp,do",
                         "ttl":0,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"js,css,xml,htm,html",
                         "ttl":1800,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"swf,jpg,gif,png,bmp,ico,ts",
                         "ttl":86400,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                         "ttl":31536000,
                         "cacheType":3,
                         "cacheWithArgs":0
                         }
                    ],
                    "ipWhiteList": "127.0.0.1",
                    "whiteReferer":{
                        "allowList":["ab.ctyun.com"],
                        "allowEmpty":"on"
                    },
                    "httpsBasic":{
                        "originProtocol": "http"
                    }
                }
            }
        print("域名name：{}，产品类型product为：{}".format(name,data["data"]["productCode"]))
        response = self.session.post(self.host + url,json=data,verify=False)
        print(response.text)
        return response

    def create_live_domain(self):
        """
        创建视频直播加速域名
        :return:
        """
        url = "/cdn/gw/domain/CreateDomain"
        name = "Domain_Test_" + random_string(4) + ".zhihu.com"
        data = {
            "data":{
                "workspaceId":self.workspaceid,
                "action":1,
                "userName":"蔡君",
                "domain":name,
                "recordNum":"京ICP备13052560号",
                "productCode":"005",
                "liveConf":{
                    "mode":1,
                    "multiProtocol":0,
                    "protocolType":2,
                    "domainType":2,
                    "publishPoint":"app"
                },
                "originProtocol":"http",
                "origin":[
                    {
                        "origin":"",
                        "port":1935,
                        "role":"master",
                        "weight":1
                    }
                ],
                "httpsBasic":{
                    "originProtocol":"http"
                }
            }
        }
        print("域名name：{}，产品类型product为：{}".format(name,data["data"]["productCode"]))
        response = self.session.post(self.host + url,json=data,verify=False)
        print(response.text)
        return response

    def edit_domain(self,name,product):  # eidt_domain("xxx.zhihu.com","001")
        """
        编辑域名
        :param name:
        :param product:
        :return:
        """
        url = "/cdn/gw/domain/CreateDomain"
        if product == "005":
            data = {
                "data":{
                    "workspaceId":self.workspaceid,
                    "action":2,
                    "userName":"蔡君",
                    "domain":name,
                    "recordNum":"京ICP备13052560号",
                    "productCode":product,
                    "liveConf":{
                        "mode":1,
                        "multiProtocol":0,
                        "protocolType":2,
                        "domainType":2,
                        "publishPoint":"app" + random_string(4)
                    },
                    "originProtocol":"http",
                    "origin":[
                        {
                            "origin":"",
                            "port":1935,
                            "role":"master",
                            "weight":1
                        }
                    ],
                    "httpsBasic":{
                        "originProtocol":"http"
                    }
                }
            }
        elif product == "001" or product == "003" or product == "004":
            data = {
                "data":{
                    "workspaceId":self.workspaceid,
                    "action":2,
                    "userName":"蔡君",
                    "domain":name,
                    "recordNum":"京ICP备13052560号",
                    "productCode":product,
                    "origin":[
                        {
                            "role":"master",
                            "origin":"1.1.1.1",
                            "port":"443",
                            "weight":1,
                            "protocol":"https"
                        }
                    ],
                    "originProtocol":"https",
                    "basicConf":{
                        "follow302":0},
                    "reqHost":"cc.ctyun.com",
                    "filetypeTtl":[
                        {"fileType":"php,ashx,aspx,asp,jsp,do",
                         "ttl":0,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"js,css,xml,htm,html",
                         "ttl":1800,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"swf,jpg,gif,png,bmp,ico,ts",
                         "ttl":86400,
                         "cacheType":3,
                         "cacheWithArgs":0
                         },
                        {"fileType":"wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                         "ttl":31536000,
                         "cacheType":3,
                         "cacheWithArgs":0
                         }
                    ],
                    "ipWhiteList": "127.0.0.1",
                    "whiteReferer":{
                        "allowList":["ab.ctyun.com"],
                        "allowEmpty":"on"
                    },
                    "httpsBasic":{
                        "originProtocol": "https"
                    }
                }
            }
        else:
            print("参数错误，请检查product！！！")
            data = ""
        response = self.session.post(self.host + url,json=data,verify=False)
        print(response.text)
        return response

    def stop_domain(self,name,product):
        """
        停用域名
        :param name: 域名名称
        :param product: 产品类型：001/003/004/005，据实际情况而定
        :return:
        """
        url = "/cdn/gw/domain/ChangeDomainStatus"
        params = {
            "workspaceId": self.workspaceid,
            "domain": name,
            "status": 2,
            "domainStatus": 4 ,
            "businessType": product,
            "recordNum": "京ICP备13052560号"
        }
        response = self.session.get(self.host + url,params=params,verify=False)
        print(response.text)
        return response

    def start_domain(self,name,product):
        """
        启用域名
        :param name: 域名名称
        :param product: 产品类型：001/003/004/005，据实际情况而定
        :return:
        """
        url = "/cdn/gw/domain/ChangeDomainStatus"
        params = {
            "workspaceId": self.workspaceid,
            "domain": name,
            "status": 3,
            "domainStatus": 6 ,
            "businessType": product,
            "recordNum":"京ICP备13052560号"
        }
        response = self.session.get(self.host + url,params=params,verify=False)
        print(response.text)
        return response

    def delete_domain(self,name,product):
        """
        删除域名
        :param name: 域名名称
        :param product: 产品类型：001/003/004/005，据实际情况而定
        :return:
        """
        url = "/cdn/gw/domain/ChangeDomainStatus"
        params = {
            "workspaceId": self.workspaceid,
            "domain": name,
            "status": 1,
            "domainStatus": 6 ,
            "businessType": product,
            "recordNum":"京ICP备13052560号"
        }
        response = self.session.get(self.host + url,params=params,verify=False)
        print(response.text)
        return response

    def list_domain(self):
        """
        域名列表
        :return:
        """
        url = "/cdn/gw/domain/ListDomain"
        params = {
            "workspaceId":self.workspaceid,
            "page":1,
            "page_size":10000
        }
        response = self.session.get(self.host + url,params=params,verify=False)
        print(response.text)
        return response






