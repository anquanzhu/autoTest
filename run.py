# -*- coding: utf-8 -*-


"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""
import os
import sys
import time

import pytest
from bin.GetSuite import walkfile
from bin.copyFile import copy_file
from bin.unit.Log import Log
from bin.writeXml import writeXML, write_scdn_XML, write_iam_XML

cdn_path = os.path.abspath('.') + "\\testcases\\cdn"
scdn_path = os.path.abspath('.') + "\\testcases\\scdn"
iam_path = os.path.abspath('.') + "\\testcases\\iam"
xml_cdn_path = os.path.abspath('.') + "/report/cdn_console/xml"
html_cdn_path = os.path.abspath('.') + "/report/cdn_console/html"
xml_scdn_path = os.path.abspath('.') + "/report/scdn_console/xml"
html_scdn_path = os.path.abspath('.') + "/report/scdn_console/html"
xml_iam_path = os.path.abspath('.') + "/report/iam/xml"
html_iam_path = os.path.abspath('.') + "/report/iam/html"


def allure_test(testcase_path, xml_path, html_path):
    # 定义测试集
    args = ['--alluredir={path_allure}'.format(path_allure=xml_path)]
    # ff = os.path.abspath('.') + "\\vip_console\\test_vip_tools.py"
    # demo_args = ['-s', ff]

    if not os.path.exists(html_path):
        os.mkdir(html_path)
    if testcase_path is not None:
        test_args = ['-s', testcase_path]
        pytest.main(test_args + args)
    else:
        print("用户未选择执行项目，默认执行CDN控制台项目接口自动化")
        test_args = ['-s', os.path.abspath('.') + "\\testcases\\cdn"]
        pytest.main(test_args + args)
    #
    # 生成HTML报告
    os.system('allure generate {path_allure} -o {path_html} --clean'
              .format(path_allure=xml_path, path_html=html_path))


def del_xml_file(xml_report_path):
    # 看趋势，存储10次左右的执行结果，然后再清理xml_report文件夹
    if not os.path.exists(xml_report_path):
        os.mkdir(xml_report_path)
    xml_fileList = walkfile(xml_report_path)
    file_count = len(xml_fileList)
    print("当前有【 " + str(file_count) + " 】个allure报告文件！！！")
    # 一次大约是1500个左右的xml文件，大于20000个的时候清理
    if file_count > 1000:
        for path in xml_fileList:
            if os.path.exists(xml_report_path + "/" + path):  # 如果文件存在
                # print(xml_report_path+"/"+path)
                os.remove(xml_report_path + "/" + path)
    print("XML删除完成！！")


def generate_report():
    """不同的项目生成不同的测试报告，归类"""

    argv_len = len(sys.argv)
    temp = None
    print("默认命令： python run.py pe cdn "
          "[pe 生产环境，ite 集成测试环境 // cdn cdn控制台项目 scdn 安全控制台 iam iam项目 all 所有项目]")
    if argv_len > 2:
        temp = sys.argv[2]
    print(temp)
    if temp is not None:
        if temp == 'cdn' or temp == 'CDN':
            del_xml_file(xml_cdn_path)
            writeXML()
            allure_test(cdn_path, xml_cdn_path, html_cdn_path)
        elif temp == 'scdn' or temp == 'SCDN':
            del_xml_file(xml_scdn_path)
            write_scdn_XML()
            allure_test(scdn_path, xml_scdn_path, html_scdn_path)
        elif temp == 'iam' or temp == 'IAM':
            del_xml_file(xml_iam_path)
            write_iam_XML()
            allure_test(iam_path, xml_iam_path, html_iam_path)
        elif temp == 'all' or temp == 'ALL':
            del_xml_file(xml_cdn_path)
            del_xml_file(xml_scdn_path)
            del_xml_file(xml_iam_path)
            writeXML()
            write_scdn_XML()
            write_iam_XML()
            allure_test(cdn_path, xml_cdn_path, html_cdn_path)
            allure_test(scdn_path, xml_scdn_path, html_scdn_path)
            allure_test(iam_path, xml_iam_path, html_iam_path)
        else:
            print("输入的项目简写有误，请检查！！！")
    else:
        print("请输入需要执行的项目！！！ ")
        print("默认执行CDN控制台接口自动化测试用例")
        del_xml_file(xml_cdn_path)
        writeXML()
        allure_test(cdn_path, xml_cdn_path, html_cdn_path)


if __name__ == '__main__':
    log = Log()
    # file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) # 文件所在位置往上二层目录
    file_path = str(os.path.join(os.path.dirname(__file__)))  # 文件所在位置往上一层目录

    generate_report()

    # 开启allure web服务,linux系统下无法使用
    # os.system('allure open {path_html}'.format(path_html=html_report_path))

    # 推送测试结果到 测试用例平台
    # time.sleep(3)
    # Upload_Result().get_allure_report()
