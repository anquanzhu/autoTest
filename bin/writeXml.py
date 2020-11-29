# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

from bin.Yaml import readYaml, get_env
from lxml.etree import HTMLParser

"""
<environment>
    <parameter>
        <key>Test_Type</key>
        <value>接口自动化</value>
    </parameter>
    <parameter>
        <key>Test_Range</key>
        <value>VIP客户控制台</value>
        <value>CTYUN客户控制台</value>
        <value>BS客户控制台</value>
        <value>对外V1接口</value>
    </parameter>
    <parameter>
        <key>ENV</key>
        <value>集成测试环境</value>
    </parameter>
</environment>
"""


def writeXML():
    r = readYaml('application.yaml')
    env = get_env()
    file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    # 创建根节点
    a = ET.Element("environment")
    # h =  HTMLParser.
    # 创建子节点，并添加属性
    b = ET.SubElement(a, "parameter")
    b1 = ET.SubElement(a, "parameter")
    b2 = ET.SubElement(a, "parameter")
    # b.attrib = {"category":"COOKING"}

    # 创建子节点，并添加数据
    key1 = ET.SubElement(b, "key")
    key1.text = "Test_Type"
    key1 = ET.SubElement(b, "value")
    key1.text = r.get('TEST_TYPE')

    key2 = ET.SubElement(b1, "key")
    key2.text = "Test_Range"
    key2 = ET.SubElement(b1, "value")
    key2.text = r.get('ENV_RANGE')

    key3 = ET.SubElement(b2, "key")
    key3.text = "ENV"
    key3 = ET.SubElement(b2, "value")
    if env == 'PE' or env == 'pe':
        key3.text = "生产环境"
    elif env == 'ITE' or env == 'ite':
        key3.text = "集成测试环境"
    elif env == 'ATE' or env == 'ate':
        key3.text = "自动化测试环境"
    else:
        key3.text = "未知环境，请校验ENV参数"

    # 创建elementtree对象，写文件
    tree = ET.ElementTree(a)
    xmlPath = file_path + '/report/cdn_console/xml/environment.xml'
    if os.path.exists(xmlPath):
        os.remove(xmlPath)
    tree.write(xmlPath, encoding='utf-8')


def write_scdn_XML():
    r = readYaml('application.yaml')
    env = get_env()
    file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    # 创建根节点
    a = ET.Element("environment")
    # h =  HTMLParser.
    # 创建子节点，并添加属性
    b = ET.SubElement(a, "parameter")
    b1 = ET.SubElement(a, "parameter")
    b2 = ET.SubElement(a, "parameter")
    # b.attrib = {"category":"COOKING"}

    # 创建子节点，并添加数据
    key1 = ET.SubElement(b, "key")
    key1.text = "Test_Type"
    key1 = ET.SubElement(b, "value")
    key1.text = r.get('TEST_TYPE')

    key2 = ET.SubElement(b1, "key")
    key2.text = "Test_Range"
    key2 = ET.SubElement(b1, "value")
    key2.text = r.get('SCDN_ENV_RANGE')

    key3 = ET.SubElement(b2, "key")
    key3.text = "ENV"
    key3 = ET.SubElement(b2, "value")
    if env == 'PE' or env == 'pe':
        key3.text = "生产环境"
    elif env == 'ITE' or env == 'ite':
        key3.text = "集成测试环境"
    elif env == 'ATE' or env == 'ate':
        key3.text = "自动化测试环境"
    else:
        key3.text = "未知环境，请校验ENV参数"

    # 创建elementtree对象，写文件
    tree = ET.ElementTree(a)
    xmlPath = file_path + '/report/scdn_console/xml/environment.xml'
    if os.path.exists(xmlPath):
        os.remove(xmlPath)
    tree.write(xmlPath, encoding='utf-8')


def write_iam_XML():
    r = readYaml('application.yaml')
    env = get_env()
    file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    # 创建根节点
    a = ET.Element("environment")
    # h =  HTMLParser.
    # 创建子节点，并添加属性
    b = ET.SubElement(a, "parameter")
    b1 = ET.SubElement(a, "parameter")
    b2 = ET.SubElement(a, "parameter")
    # b.attrib = {"category":"COOKING"}

    # 创建子节点，并添加数据
    key1 = ET.SubElement(b, "key")
    key1.text = "Test_Type"
    key1 = ET.SubElement(b, "value")
    key1.text = r.get('TEST_TYPE')

    key2 = ET.SubElement(b1, "key")
    key2.text = "Test_Range"
    key2 = ET.SubElement(b1, "value")
    key2.text = r.get('IAM_ENV_RANGE')

    key3 = ET.SubElement(b2, "key")
    key3.text = "ENV"
    key3 = ET.SubElement(b2, "value")
    if env == 'PE' or env == 'pe':
        key3.text = "生产环境"
    elif env == 'ITE' or env == 'ite':
        key3.text = "集成测试环境"
    elif env == 'ATE' or env == 'ate':
        key3.text = "自动化测试环境"
    else:
        key3.text = "未知环境，请校验ENV参数"

    # 创建elementtree对象，写文件
    tree = ET.ElementTree(a)
    xmlPath = file_path + '/report/iam/xml/environment.xml'
    if os.path.exists(xmlPath):
        os.remove(xmlPath)
    tree.write(xmlPath, encoding='utf-8')


if __name__ == '__main__':
    writeXML()
