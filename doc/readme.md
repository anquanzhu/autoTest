[项目背景]
CDN客户控制台接口自动化测试
[V2.1]
[改动]
1. 项目文件结构变化，支撑IAM、CDN控制台、SCDN控制台三个项目
2. 参数化运行多个项目多个环境，改造执行脚本，测试报告分项目输出
3. 去掉重复的方法调用与废弃的用例


[V2.0]
[项目框架]
基本架构：pytest + allure + request
编写步骤：
    1. 测试用例平台编写用例，复制用例case_id
    2. 到对应的用例文件夹下面编写测试用例，使用test_CDN_case_id 作为名字
    3. 执行： python run.py pe   (pe,ite,ate等等，代表不同环境)

文件结构
├─.idea
│  ├─dictionaries
│  └─inspectionProfiles
├─bin
│  ├─Log
│  ├─Script
│  ├─unit
│  
├─bs_console
│  
├─ctyun_console
├─doc
├─params
├─performance_test
├─report
│  ├─html│ 
│  ├─performance_report
│  └─xml
├─testcases  (已废弃)
│  ├─bs
│  ├─ctyun
│  └─vip
├─v1
│ 
├─vip_console





[V1.0]
[项目特点]
1. 全自动执行接口测试，跨平台(CDN客户控制台，业务管理平台，运维支撑平台，工单系统)，跨流程
2. 一套代码可以执行到任何环境，用户只需要设置 applicaion.yaml 里面的环境变量参数即可
   支持集成测试环境，自动化测试环境，生产环境(可能部分用例无权限)


[项目框架]
基本架构：pytest + allure + request
依赖： doc/chrome-extensions-master.zip (解压后可以直接加载到chrome浏览器，录制HTTP文件)

流程类测试用例在： vip_console bs_console ctyun_console v1
查询类测试用例在： testcases (录制的json文件)
参数文件：params
测试报告：report
日志： bin/Log
基本方法类：bin , bin/unit
├─bin
│  ├─Log
│  ├─unit
├─doc
├─flow
├─params
├─report
└─testcases

[操作方式]
1. 在application.yaml 里面设置项目执行的环境
2. 按需执行项目


[执行方式]
python run.py

[开发文档]
1. 如果是简单查询类接口，直接使用 “chrome-extensions-master.zip” 录制即可
2. 如果接口含有复杂流程，自行编写python代码，以test_XXX开头
   2.1 接口url 写到params/XXX.yaml 
   2.2 接口基本信息写到 params/base_XXX.yaml中