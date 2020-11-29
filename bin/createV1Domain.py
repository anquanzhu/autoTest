# -*- coding: utf-8 -*-
import json
import random

from bin.GetSuite import read
from bin.unit.Rondom import random_string
from bin.v1Init import v1Init

productCode = ['001', '003', '004']


# productCode= 005 是live_video 在线直播，格式和其他的不一样

"""
说明：
Productcode：产品类型
"001"：静态加速
"003"：下载加速
"004"：视频点播加速
"005"：视频直播加速

只有视频直播加速类型产品，请求参数不同，其他类型产品一样，可复用参数

"""


class Create_v1_Domain(object):

    def __init__(self):
        self.public_key = v1Init.PUBLIC_KEY
        self.private_key = v1Init.PRIVATE_KEY

    def create_domain(self, ctyunAcctId, productcode):
        """
        创建域名
        :param ctyunAcctId: 天翼云id
        :param productcode: 产品类型
        :return:
        """
        name = "V1_Test_" + random_string(4) + ".zhihu.com"
        if productcode == "005":
            data = {
                "data": {
                    "ctyunAcctId": ctyunAcctId,
                    "action": 1,
                    "domain": name,
                    "recordNum": "京ICP备13052560号",
                    "recordStatus": 2,
                    "productCode": productcode,
                    "customerName": "陈孟琪",
                    "liveConf": {
                        "mode": 1,
                        "multiProtocol": 0,
                        "protocolType": 2,
                        "domainType": 2,
                        "publishPoint": "app"
                    },
                    "originProtocol": "http",
                    "origin": [
                        {
                            "origin": "",
                            "port": 1935,
                            "role": "master",
                            "weight": 1
                        }
                    ],
                    "httpsBasic": {
                        "originProtocol": "http"
                    }
                }
            }
        else:
            data = {
                "data": {
                    "ctyunAcctId": ctyunAcctId,
                    "action": 1,
                    "domain": name,
                    "recordNum": "京ICP备13052560号",
                    "recordStatus": 2,
                    "productCode": productcode,
                    "customerName": "陈孟琪",
                    "origin": [
                        {
                            "role": "master",
                            "origin": "1.1.1.1",
                            "port": "80",
                            "weight": 1,
                            "protocol": "http"
                        }
                    ],
                    "originProtocol": "http",
                    "basicConf": {
                        "follow302": 0
                    },
                    "reqHost": "cc.ctyun.com",
                    "filetypeTtl": [
                        {"fileType": "php,ashx,aspx,asp,jsp,do",
                         "ttl": 0,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {"fileType": "js,css,xml,htm,html",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {"fileType": "swf,jpg,gif,png,bmp,ico,ts",
                         "ttl": 86400,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {
                            "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,"
                                        "rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,"
                                        "cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                            "ttl": 31536000,
                            "cacheType": 3,
                            "cacheWithArgs": 0,
                            "split": 0,
                        }
                    ],
                    "pathTtl": [
                        {"path": "/a",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0
                        },

                        {"path": "/b",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0
                        }
                    ],
                    "ipWhiteList": "127.0.0.1",
                    "whiteReferer": {
                        "allowList": ["ab.ctyun.com"],
                        "allowEmpty": "on"
                    },
                    "blackReferer": {
                        "allowList": ["ac.ctyun.com"],
                        "allowEmpty": "on"
                    },
                    "httpsPublicContent": self.public_key,
                    "httpsPrivateKey": self.private_key,
                    "certName": "CTYUN_TEST",
                    "httpsBasic": {
                        "originProtocol": "http",
                        "httpsForce":"on",
                        "httpForce":"off",
                        "forceStatus":"302"
                    },
                    "ipBlackList": "1.1.1.1,1.1.1.2",
                    "reqHeaders": [
                        {"key": "abc",
                         "value": "测试"
                         }],
                    "respHeaders": [
                        {
                            "key": "Content-Type",
                            "value": "测试2"
                        }
                    ],
                    "errorCode": [
                        {
                            "code": ["404"],
                            "ttl": 10
                        },
                        {
                            "code": ["500"],
                            "ttl": 60
                        }

                    ],
                    "userAgent": {
                        "type": 0,
                        "ua": ["test"]
                    },
                }
            }

        return data

    def full_field_domain(self, ctyunAcctId):
        """
        创建随机域名，全量字段
        :param ctyunAcctId: 天翼云id
        :return:
        """
        name = "V1_Test_" + random_string(4) + ".ctyun.cn"

        data = {
            "data": {
                "ctyunAcctId": ctyunAcctId,
                "action": 1,
                "domain": name,
                "recordNum": "京ICP备13052560号",
                "recordStatus": 2,
                "productCode": random.choice(productCode),
                "customerName": "陈孟琪",
                "specialRequirement": "无",
                "testUrl": "www.ctyun.com",
                "areaScope": 1,
                "sharedHost": "www.ctyun.com",
                "ignoreHeaders": "abc",
                "origin": [
                    {
                        "role": "master",
                        "origin": "1.1.1.1",
                        "port": "80",
                        "weight": 1,
                        "protocol": "http"
                    }
                ],
                "originProtocol": "http",
                "basicConf": {
                    "follow302": 0,
                    "https_return": "off",
                    "httpServerPort": "80",
                    "httpsServerPort": "443",
                    "httpOriginPort": 80,
                    "httpsOriginPort": 443,
                    "xff": 0,
                    "corsOrigin": 0,
                    "buffer": "off",
                    "defaultCacheRule": "off"
                },
                "errorPage": {
                    "code": "404",
                    "url": "http://www.ctyun.com/iam/cdn/v1/domainlist/"
                },
                "uploadConf": {
                    "maxBodySize": "1m",
                    "maxBuffSize": "1k"
                },
                "gzip": {
                    "minLength": "1k",
                    "fileType": "zip",
                },
                # 额外配置(真实)，非真实走自助会失败
                # "expandConf": [{
                #     "content": "cssabcd",
                #     "level": "1",
                #     "priority": 10,
                #     "message": "test"
                # }
                # ],
                "reqHost": "cc.ctyun.com",
                "filetypeTtl": [
                    {"fileType": "php,ashx,aspx,asp,jsp,do",
                     "ttl": 0,
                     "cacheType": 3,
                     "cacheWithArgs": 0,
                     "split": 0,
                     "mode": 0,
                     "priority": 10
                     },
                    {"fileType": "js,css,xml,htm,html",
                     "ttl": 1800,
                     "cacheType": 3,
                     "cacheWithArgs": 0,
                     "split": 0,
                     "mode": 0,
                     "priority": 10
                     },
                    {"fileType": "swf,jpg,gif,png,bmp,ico,ts",
                     "ttl": 86400,
                     "cacheType": 3,
                     "cacheWithArgs": 0,
                     "split": 0,
                     "mode": 0,
                     "priority": 10
                     },
                    {
                        "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,"
                                    "rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,"
                                    "cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                        "ttl": 31536000,
                        "cacheType": 3,
                        "cacheWithArgs": 0,
                        "split": 0,
                        "mode": 0,
                        "priority": 10
                    }
                ],
                "urlRewrite": [{
                    "uri": "/cdn/iam/domain",
                    "targetUri": "/cdn/iam/domainlist",
                    "weight": 1
                }],
                "cacheArgs": {
                    "args":"abc",
                    "disables":"on"
                },
                "pathTtl": [
                    {"path": "/a",
                     "ttl": 1800,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                    },

                    {"path": "/b",
                     "ttl": 1800,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                    }
                ],

                "httpsPublicContent": self.public_key,
                "httpsPrivateKey": self.private_key,
                "certName": "CTYUN_TEST",
                "ipWhiteList": "127.0.0.1",
                "whiteReferer": {
                    "allowList": ["ab.ctyun.com"],
                    "allowEmpty": "on"
                },
                "blackReferer": {
                    "allowList": ["ac.ctyun.com"],
                    "allowEmpty": "on"
                },
                "httpsBasic": {
                    "originProtocol": "http",
                    "httpsForce":"on",
                    "httpForce":"off",
                    "forceStatus":"302"
                },
                "ipBlackList": "1.1.1.1,1.1.1.2",
                "reqHeaders": [
                    {"key": "abc",
                     "value": "测试"
                     }],
                "respHeaders": [
                    {
                        "key": "Content-Type",
                        "value": "测试2"
                    }
                ],
                "errorCode": [
                    {
                        "code": ["404"],
                        "ttl": 10
                    },
                    {
                        "code": ["500"],
                        "ttl": 60
                    }

                ],
                "userAgent": {
                    "type": 0,
                    "ua": ["t", "e", "s", "t"]
                }
            }
        }

        return data

    def edit_domain(self, ctyunAcctId, name, productcode):  # eidt_domain("xxx.zhihu.com","001")
        """
        编辑域名
        :param ctyunAcctId: 天翼云id
        :param name: 域名
        :param product: 产品类型
        :return:
        """

        if productcode == "005":
            data = {
                "data": {
                    "ctyunAcctId": ctyunAcctId,
                    "action": 2,
                    "domain": name,
                    "recordNum": "京ICP备13052560号",
                    "recordStatus": 2,
                    "productCode": "005",
                    # "customerName": "陈孟琪",
                    "liveConf": {
                        "mode": 1,
                        "multiProtocol": 0,
                        "protocolType": 2,
                        "domainType": 2,
                        "publishPoint": "edit"
                    },
                    "originProtocol": "http",
                    "origin": [
                        {
                            "origin": "",
                            "port": 1935,
                            "role": "master",
                            "weight": 1
                        }
                    ],
                    "httpsBasic": {
                        "originProtocol": "http"
                    }
                }
            }
        else:
            data = {
                "data": {
                    "ctyunAcctId": ctyunAcctId,
                    "action": 2,
                    "domain": name,
                    "recordNum": "京ICP备13052560号",
                    "recordStatus": 2,
                    "productCode": productcode,
                    # "customerName": "陈孟琪",
                    "origin": [
                        {
                            "role": "master",
                            "origin": "1.1.1.1",
                            "port": "80",
                            "weight": 1,
                            "protocol": "http"
                        }
                    ],
                    "originProtocol": "http",
                    "basicConf": {
                        "follow302": 0
                    },
                    "reqHost": "cc.ctyun.com",
                    "filetypeTtl": [
                        {"fileType": "php,ashx,aspx,asp,jsp,do",
                         "ttl": 0,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {"fileType": "js,css,xml,htm,html",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {"fileType": "swf,jpg,gif,png,bmp,ico,ts",
                         "ttl": 86400,
                         "cacheType": 3,
                         "cacheWithArgs": 0,
                         "split": 0,
                         },
                        {
                            "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,"
                                        "rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,"
                                        "cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                            "ttl": 31536000,
                            "cacheType": 3,
                            "cacheWithArgs": 0,
                            "split": 0,
                        }
                    ],
                    "pathTtl": [
                        {"path": "/edit",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0
                        },

                        {"path": "/b",
                         "ttl": 1800,
                         "cacheType": 3,
                         "cacheWithArgs": 0
                        }
                    ],
                    "ipWhiteList": "127.0.0.1",
                    "whiteReferer": {
                        "allowList": ["ab.ctyun.com"],
                        "allowEmpty": "on"
                    },
                    "httpsPublicContent": self.public_key,
                    "httpsPrivateKey": self.private_key,
                    "certName": "CTYUN_TEST",
                    "blackReferer": {
                        "allowList": ["ac.ctyun.com"],
                        "allowEmpty": "on"
                    },
                    "httpsBasic": {
                        "originProtocol": "http",
                        "httpsForce":"on",
                        "httpForce":"off",
                        "forceStatus":"302"
                    },
                    "ipBlackList": "1.1.1.1,1.1.1.2",
                    "reqHeaders": [
                        {"key": "abc",
                         "value": "测试"
                         }],
                    "respHeaders": [
                        {
                            "key": "Content-Type",
                            "value": "测试2"
                        }
                    ],
                    "errorCode": [
                        {
                            "code": ["404"],
                            "ttl": 10
                        },
                        {
                            "code": ["500"],
                            "ttl": 60
                        }

                    ],
                    "userAgent": {
                        "type": 0,
                        "ua": ["test"]
                    },
                }
            }
        return data

    def stop_domain(self, ctyunAcctId, name, productcode):
        """
        停用域名
        :param ctyunAcctId: 天翼云id
        :param name: 域名
        :param productcode: 产品类型
        :return:
        """
        data = {
            "ctyunAcctId": ctyunAcctId,
            "domain": name,
            "status": 2,
            "domainStatus": 4,
            "businessType": productcode,
            "recordNum": "京ICP备13052560号",
            "recordStatus": 2,
            "customerName": "陈孟琪"
        }

        return data

    def start_domain(self, ctyunAcctId, name, productcode):
        """
        启用域名
        :param ctyunAcctId: 天翼云id
        :param name: 域名
        :param productcode: 产品类型
        :return:
        """

        data = {
            "ctyunAcctId": ctyunAcctId,
            "domain": name,
            "status": 3,
            "domainStatus": 6,
            "businessType": productcode,
            "recordNum": "京ICP备13052560号",
            "customerName": "陈孟琪",
            "recordStatus": 2
        }

        return data

    def delete_domain(self, ctyunAcctId, name, productcode):
        """
        删除域名
        :param ctyunAcctId: 天翼云id
        :param name: 域名
        :param productcode: 产品类型
        :return:
        """
        data = {
            "ctyunAcctId": ctyunAcctId,
            "domain": name,
            "status": 1,
            "domainStatus": 6,
            "businessType": productcode,
            "recordNum": "京ICP备13052560号",
            "customerName": "陈孟琪",
            "recordStatus": 2
        }

        return data









