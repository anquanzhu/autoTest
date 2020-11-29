# -*- coding: utf-8 -*-
from bin.GetSuite import walkfile, read
from bin.Yaml import choose_Yaml, readYaml, get_env, choose_v1yaml
from bin.unit.Session import Session

'''
   项目参数初始化类，确保每个文件只读取一次。所有用例调用该类里面的变量
'''


class Init:
    # 项目基本参数
    BASE_INFO = choose_Yaml()
    V1_BASE_INFO = choose_v1yaml()
    # 环境变量参数
    ENV = get_env()

    # 各模块参数文件
    DOMAIN_INFO = readYaml('params/cdn/domain.yaml')
    CERT_INFO = readYaml('params/cdn/cert.yaml')
    V1_INFO = readYaml('params/cdn/v1.yaml')
    LOG_INFO = readYaml('params/cdn/log.yaml')
    CTYUN_INFO = readYaml('params/cdn/ctyun.yaml')

    # 证书相关参数
    PUBLIC_KEY = read('/params/cdn/server365.crt')
    PRIVATE_KEY = read('/params/cdn/server_private365.key')
    PUBLIC_KEY_EXPIRE = read('/params/cdn/server_expire.crt')
    PRIVATE_KEY_EXPIRE = read('/params/cdn/server_private_expire.key')
    PUBLIC_ZHIHUA_KEY = read('/params/cdn/server_zhihua.crt')
    PRIVATE_KEY_ZHIHUA = read('/params/cdn/server_private_zhihua.key')

    # Session 部分 [客户控制台，业务控制台，工单系统 ]
    CONSOLE_SESSION = Session().get_session()
    # 业务平台跳转后的控制台cookie
    BS_SESSION = Session().get_bs_console_session()
    WO_SESSION = Session().get_iam_private_session()
    CTYUN_SESSION = Session().get_ctyun_session()

    # 客户控制台，自助配置账号cookie
    # Auto_SESSION = Session().get_auto_session()
