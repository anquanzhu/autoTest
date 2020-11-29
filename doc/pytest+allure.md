[Pytest+Allure 相关用法介绍]

[1.用例优先级]
    使用：@allure.severity("normal")
    '''
    blocker　   阻塞缺陷（功能未实现，无法下一步）
    critical　　严重缺陷（功能点缺失）
    normal　　  一般缺陷（边界情况，格式错误）
    minor　     次要缺陷（界面错误与ui需求不符）
    trivial　　 轻微缺陷（必须项无提示，或者提示不规范）
    '''
    
[2.Allure 的层级关系]    
    epic>feature>story>testcase>step>description=attach
    需要注意的是，除了attach可以放在def下面进行打印，其他的都不能放在def下面，只能作为一个声明放在class或者def上面

[3. Pytest 运行方式]
    1. # 定义测试集 (注意带了-s -q 的话，用例里面print 的内容将不会出现在报告里面)
        args = ['--alluredir', xml_report_path]
        # args = ['-s', '-q', '--alluredir', xml_report_path]
        pytest.main(args)  
    2. 只执行某一个套件   
        pytest.main("-v -s subpath1/") 
        pytest.main("-v -s spec_001_modul_test.py")
    3. 只执行某一个优先级的用例套件
        pytest --alluredir=./report/xml_report_path --allure-severities=blocker,critical 
        
[4. Allure 报告里面的趋势图]
    需要提供历史运行记录才会有数据，如果每次执行删除了xml下面的json 文件，则会空
    
[5. Allure 设置环境变量]
    在xml文件夹下面添加environment.xml
     
[6. Allure 如何在Jenkins上设置CI自动执行并发送邮件]
    见： https://www.jianshu.com/p/b74d8b444681
    报告会自动集成到jenkins，邮件可以指定发送，邮件内容里面报告可以发送在线链接或者将报告内容下载打包压缩发送       


# @allure.feature # 用于定义被测试的功能，被测产品的需求点
# @allure.story # 用于定义被测功能的用户场景，即子功能点
# @allure.severity #用于定义用例优先级
# @allure.issue #用于定义问题表识，关联标识已有的问题，可为一个url链接地址
# @allure.testcase #用于用例标识，关联标识用例，可为一个url链接地址
# @allure.attach # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
# @pytest.allure.step # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
# allure.environment(environment=env) #用于定义environment          