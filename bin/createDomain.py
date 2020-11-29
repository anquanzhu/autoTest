# -*- coding: utf-8 -*-

# 下载加速
import random

from bin.GetSuite import read
from bin.Init import Init
from bin.Yaml import choose_v1yaml
from bin.unit import Log
from bin.unit.Rondom import random_string, random_int

public_key = read('/params/cdn/server.crt')
private_key = read('/params/cdn/server_private.key')
productCode = ['001', '003', '004']

default_workspaceid = Init.BASE_INFO['workspaceid']


# productCode= 005 是live_video 在线直播，格式和其他的不一样


class CreateDomain:

    def __init__(self, workspaceid=default_workspaceid):
        # self.config = conf.Config()
        self.log = Log.Log()
        self.base_info = choose_v1yaml()
        self.workspace_id = workspaceid
        self.ctyunacctid = self.base_info["ctyunAcctId"]

    def generate_randomDomain(self):
        domain = 'Auto-' + random_string(6) + '.ctyun.cn'
        flag = random_int('1, 2')
        if flag == '1':
            public = public_key
            private = private_key
            certName = "CTYUN_TEST"
        else:
            public = ''
            private = ''
            certName = ''
        random_data = {
            "data": {
                "workspaceId": self.workspace_id,
                "action": 1,
                "domain": domain,
                "recordNum": "京ICP备12022551号",
                "productCode": random.choice(productCode),
                # 测试非法的productCode
                # "productCode": "006",
                "origin": [
                    {
                        "role": "master",
                        "origin": "192.255.0.5",
                        "port": 80,
                        "weight": 1
                    },
                    {
                        "role": "slave",
                        "origin": "gg.ctyun.cn",
                        "port": 80,
                        "weight": 1
                    }
                ],
                "originProtocol": "http",
                "basicConf": {
                    "follow302": 0
                },
                "reqHost": "ss.ctyun.cn",
                "httpsPublicContent": public,
                "httpsPrivateKey": private,
                "certName": certName,
                "pathTtl": [
                    {
                        "path": "/test/a",
                        "ttl": 80,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "filetypeTtl": [
                    {
                        "fileType": "php,ashx,aspx,asp,jsp,do",
                        "ttl": 0,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "js,css,xml,htm,html",
                        "ttl": 1800,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "jpg,gif,png,bmp,ico,swf,ts,test1,test2",
                        "ttl": 86400,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                        "ttl": 31536000,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "ipWhiteList": "199.231.0.5",
                "userAgent": {
                    "type": 0,
                    "ua": [
                        "gg.ctyun.cn"
                    ]
                },
                "whiteReferer": {
                    "allowList": [
                        "gg.ctyun.cn"
                    ],
                    "allowEmpty": "on"
                }
            }
        }

        hit = random_int('1,10')
        if hit == '10':
            data = self.generate_live_video_push()
        elif hit == '9':
            data = self.generate_live_video_pull()
        else:
            data = random_data
        return data

    def generate_live_video_pull(self):
        domain = 'Auto-pull-' + random_string(4) + '.ctyun.cn'

        live_video_data = {
            "data": {
                "workspaceId": self.workspace_id,
                "action": 1,
                "domain": domain,
                "recordNum": "京ICP备12022551号",
                "productCode": "005",
                "liveConf": {
                    "mode": 1,
                    "multiProtocol": 0,
                    "protocolType": 2,
                    "domainType": 2,
                    "publishPoint": "live,app"
                },
                "originProtocol": "http",
                "origin": [
                    {
                        "origin": "",
                        "port": 1935,
                        "role": "master",
                        "weight": 1
                    }
                ]
            }
        }
        return live_video_data

    def generate_live_video_push(self):
        domain = 'Auto-push-' + random_string(4) + '.ctyun.cn'

        live_video_data = {
            "data": {
                "workspaceId": self.workspace_id,
                "action": 1,
                "domain": domain,
                "recordNum": "京ICP备12022551号",
                "productCode": "005",
                "liveConf": {
                    "mode": 1,
                    "multiProtocol": 1,
                    "protocolType": 2,
                    "domainType": 1,
                    "publishPoint": "live,pull",
                    "relatedDomain": "Auto-random-0f6C.ctyun.cn"
                },
                "httpsPublicContent": public_key,
                "httpsPrivateKey": private_key,
                "certName": "CTYUN_TEST",
                "pathTtl": [
                    {
                        "path": "/test/4",
                        "ttl": 80,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "filetypeTtl": [
                    {
                        "fileType": "m3u8",
                        "ttl": 0,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "ts",
                        "ttl": 86400,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "ipWhiteList": "127.0.0.3",
                "userAgent": {
                    "type": 0,
                    "ua": [
                        "curl*",
                        "*IE"
                    ]
                },
                "whiteReferer": {
                    "allowList": [
                        "*.demo.com"
                    ],
                    "allowEmpty": "on"
                },
                "originProtocol": "http",
                "origin": [
                    {
                        "origin": "",
                        "port": 1935,
                        "role": "master",
                        "weight": 1
                    }
                ]
            }
        }
        return live_video_data

    def generate_workDomain(self):

        domain = 'www.qianyi-' + random_int('1, 70000') + '.ele.me '
        flag = random_int('1, 2')
        if flag == '1':
            public = public_key
            private = private_key
            certName = "CTYUN_TEST"
        else:
            public = ''
            private = ''
            certName = ''
        random_data = {
            "data": {
                "workspaceId": self.workspace_id,
                "action": 1,
                "domain": domain,
                "recordNum": "京ICP备12022551号",
                "productCode": random.choice(productCode),
                "origin": [
                    {
                        "role": "master",
                        "origin": "192.255.0.5",
                        "port": 80,
                        "weight": 1
                    },
                    {
                        "role": "slave",
                        "origin": "gg.ctyun.cn",
                        "port": 80,
                        "weight": 1
                    }
                ],
                "originProtocol": "http",
                "basicConf": {
                    "follow302": 0
                },
                "reqHost": "ss.ctyun.cn",
                "httpsPublicContent": public,
                "httpsPrivateKey": private,
                "certName": certName,
                "pathTtl": [
                    {
                        "path": "/test/a",
                        "ttl": 80,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "filetypeTtl": [
                    {
                        "fileType": "php,ashx,aspx,asp,jsp,do",
                        "ttl": 0,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "js,css,xml,htm,html",
                        "ttl": 1800,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "jpg,gif,png,bmp,ico,swf,ts,test1,test2",
                        "ttl": 86400,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    },
                    {
                        "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                        "ttl": 31536000,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "ipWhiteList": "199.231.0.5",
                "userAgent": {
                    "type": 0,
                    "ua": [
                        "gg.ctyun.cn"
                    ]
                },
                "whiteReferer": {
                    "allowList": [
                        "gg.ctyun.cn"
                    ],
                    "allowEmpty": "on"
                }
            }
        }

        hit = random_int('1,10')
        if hit == '10':
            data = self.generate_live_video_push()
        elif hit == '9':
            data = self.generate_live_video_pull()
        else:
            data = random_data

            # data_list = {random_data: 80, live_video_data: 20}
        # wordlist = '{\"work_order\":{\"order_title\":\"新增域名-陈孟琪-' + domain + ', "sort\":\"desc", "current_staff_id\":\"20", "status_cd\":\"orderOnway\"},\"paging\":{\"page\":1,\"per_page\":10}}'
        return data

    def generate_v1Domain(self):
        """
        获取V1格式的域名信息，用于新增V1域名
        :return:
        """
        productcode = ["003", "004", "000", "006"]
        name = "V1_Test_" + random_string(6) + ".ctyun.cn"
        public = read('/params/cdn/server365.crt')
        private = read('/params/cdn/server_private365.key')
        customerName = ['', '陈孟琪_v1']
        domain_data_list = []
        # self.ctyunacctid = "2364d5f2c3f541e8925de5c866341c7a"
        print('self.ctyunacctid: ', self.ctyunacctid)
        domain_data = {
            "data": {
                "ctyunAcctId": self.ctyunacctid,
                "action": 1,
                "domain": name,
                "recordNum": "京ICP备13052560号",
                "recordStatus": 2,
                "productCode": "005",
                "customerName": random.choice(customerName),
                "liveConf": {
                    "mode": 1,
                    "multiProtocol": 0,
                    "protocolType": 2,
                    "domainType": 2,
                    "publishPoint": "app" + random_string(3)
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

        common_domain_data2 = {
            "data": {
                "ctyunAcctId": self.ctyunacctid,
                "action": 1,
                "domain": name,
                "recordNum": "京ICP备13052560号",
                "recordStatus": 2,
                "productCode": "001",
                "customerName": random.choice(customerName),
                "origin": [
                    {
                        "role": "master",
                        "origin": "1.1.1.1",
                        "port": "443",
                        "weight": 1,
                        "protocol": "https"
                    }
                ],
                "originProtocol": "https",
                "basicConf": {
                    "follow302": 0},
                "reqHost": "cc.ctyun.com",
                "filetypeTtl": [
                    {"fileType": "php,ashx,aspx,asp,jsp,do",
                     "ttl": 0,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {"fileType": "js,css,xml,htm,html",
                     "ttl": 1800,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {"fileType": "swf,jpg,gif,png,bmp,ico,ts",
                     "ttl": 86400,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {
                        "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                        "ttl": 31536000,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "httpsPublicContent": public,
                "httpsPrivateKey": private,
                "certName": "CTYUN_TEST",
                "ipWhiteList": "127.0.0.1",
                "whiteReferer": {
                    "allowList": ["ab.ctyun.com"],
                    "allowEmpty": "on"
                },
                "httpsBasic": {
                    "originProtocol": "https"
                }
            }
        }

        live_domain_data = {
            "data": {
                "ctyunAcctId": self.ctyunacctid,
                "action": 1,
                "domain": name,
                "recordNum": "京ICP备13052560号",
                "recordStatus": 2,
                "productCode": "005",
                "customerName": random.choice(customerName),
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

        common_domain_data = {
            "data": {
                "ctyunAcctId": self.ctyunacctid,
                "action": 1,
                "domain": name,
                "recordNum": "京ICP备13052560号",
                "recordStatus": 2,
                "productCode": random.choice(productcode),
                "customerName": random.choice(customerName),
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
                    "follow302": 0},
                "reqHost": "cc.ctyun.com",
                "filetypeTtl": [
                    {"fileType": "php,ashx,aspx,asp,jsp,do",
                     "ttl": 0,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {"fileType": "js,css,xml,htm,html",
                     "ttl": 1800,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {"fileType": "swf,jpg,gif,png,bmp,ico,ts",
                     "ttl": 86400,
                     "cacheType": 3,
                     "cacheWithArgs": 0
                     },
                    {
                        "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                        "ttl": 31536000,
                        "cacheType": 3,
                        "cacheWithArgs": 0
                    }
                ],
                "httpsPublicContent": public,
                "httpsPrivateKey": private,
                "certName": "CTYUN_TEST",
                "ipWhiteList": "127.0.0.1",
                "whiteReferer": {
                    "allowList": ["ab.ctyun.com"],
                    "allowEmpty": "on"
                },
                "httpsBasic": {
                    "originProtocol": "http"
                }
            }
        }
        domain_data_list.append(common_domain_data)
        domain_data_list.append(live_domain_data)
        domain_data_list.append(common_domain_data2)
        domain_data_list.append(domain_data)
        return domain_data_list

    def renew_domain(self, domain, productcode):
        if productcode == '005' and 'pull' in domain:
            domain_info = {
                "data": {
                    "workspaceId": self.workspace_id,
                    "action": 1,
                    "domain": domain,
                    "recordNum": "京ICP备12022551号",
                    "productCode": "005",
                    "liveConf": {
                        "mode": 1,
                        "multiProtocol": 0,
                        "protocolType": 2,
                        "domainType": 2,
                        "publishPoint": "live,app"
                    },
                    "originProtocol": "http",
                    "origin": [
                        {
                            "origin": "",
                            "port": 1935,
                            "role": "master",
                            "weight": 1
                        }
                    ]
                }
            }
        elif productcode == '005' and 'push' in domain:
            domain_info = {
                "data": {
                    "workspaceId": self.workspace_id,
                    "action": 1,
                    "domain": domain,
                    "recordNum": "京ICP备12022551号",
                    "productCode": "005",
                    "liveConf": {
                        "mode": 1,
                        "multiProtocol": 1,
                        "protocolType": 2,
                        "domainType": 1,
                        "publishPoint": "live,pull",
                        "relatedDomain": "Auto-random-0f6C.ctyun.cn"
                    },
                    "httpsPublicContent": public_key,
                    "httpsPrivateKey": private_key,
                    "certName": "CTYUN_TEST",
                    "pathTtl": [
                        {
                            "path": "/test/4",
                            "ttl": 80,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        }
                    ],
                    "filetypeTtl": [
                        {
                            "fileType": "m3u8",
                            "ttl": 0,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        },
                        {
                            "fileType": "ts",
                            "ttl": 86400,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        }
                    ],
                    "ipWhiteList": "127.0.0.3",
                    "userAgent": {
                        "type": 0,
                        "ua": [
                            "curl*",
                            "*IE"
                        ]
                    },
                    "whiteReferer": {
                        "allowList": [
                            "*.demo.com"
                        ],
                        "allowEmpty": "on"
                    },
                    "originProtocol": "http",
                    "origin": [
                        {
                            "origin": "",
                            "port": 1935,
                            "role": "master",
                            "weight": 1
                        }
                    ]
                }
            }
        else:
            flag = random_int('1, 2')
            if flag == '1':
                public = public_key
                private = private_key
                certName = "CTYUN_TEST"
            else:
                public = ''
                private = ''
                certName = ''
            domain_info = {
                "data": {
                    "workspaceId": self.workspace_id,
                    "action": 1,
                    "domain": domain,
                    "recordNum": "京ICP备12022551号",
                    "productCode": productcode,
                    # 测试非法的productCode
                    # "productCode": "006",
                    "origin": [
                        {
                            "role": "master",
                            "origin": "192.255.0.5",
                            "port": 80,
                            "weight": 1
                        },
                        {
                            "role": "slave",
                            "origin": "gg.ctyun.cn",
                            "port": 80,
                            "weight": 1
                        }
                    ],
                    "originProtocol": "http",
                    "basicConf": {
                        "follow302": 0
                    },
                    "reqHost": "ss.ctyun.cn",
                    "httpsPublicContent": public,
                    "httpsPrivateKey": private,
                    "certName": certName,
                    "pathTtl": [
                        {
                            "path": "/test/a",
                            "ttl": 80,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        }
                    ],
                    "filetypeTtl": [
                        {
                            "fileType": "php,ashx,aspx,asp,jsp,do",
                            "ttl": 0,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        },
                        {
                            "fileType": "js,css,xml,htm,html",
                            "ttl": 1800,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        },
                        {
                            "fileType": "jpg,gif,png,bmp,ico,swf,ts,test1,test2",
                            "ttl": 86400,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        },
                        {
                            "fileType": "wmv,mp3,wma,ogg,flv,mp4,avi,mpg,mpeg,f4v,hlv,rmvb,rm,3gp,img,bin,zip,rar,ipa,apk,jar,sis,xap,msi,exe,cab,7z,pdf,doc,docx,xls,xlsx,ppt,pptx,txt",
                            "ttl": 31536000,
                            "cacheType": 3,
                            "cacheWithArgs": 0
                        }
                    ],
                    "ipWhiteList": "199.231.0.5",
                    "userAgent": {
                        "type": 0,
                        "ua": [
                            "gg.ctyun.cn"
                        ]
                    },
                    "whiteReferer": {
                        "allowList": [
                            "gg.ctyun.cn"
                        ],
                        "allowEmpty": "on"
                    }
                }
            }
        return domain_info


if __name__ == '__main__':
    aa = CreateDomain()
    # print(2, count1)
    bb = aa.generate_v1Domain()
