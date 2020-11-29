# -*- coding: utf-8 -*-
import time
from datetime import datetime, date, timedelta

__relevance = ''
key_list = []
value_list = []


def get_dict_allkeys(dict_a):
    """
    多维/嵌套字典数据无限遍历，获取json返回结果的所有key值集合
    :param dict_a:
    :return: key_list
    """
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            key_list.append(temp_key)
            get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    key_list.append(temp_key)
                    get_dict_allkeys(temp_value)
    return key_list


def get_dict_allvalues(dict_a):
    """
    多维/嵌套字典数据无限遍历，获取json返回结果的所有value值集合
    :param dict_a:
    :return: value_list
    """
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            value_list.append(temp_value)
            get_dict_allvalues(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    value_list.append(temp_value)
                    get_dict_allvalues(temp_value)
    return value_list


def get_value(data, value):
    """
    获取json中的值
    :param data: json数据
    :param value: 值
    :return:
    """
    global __relevance
    if isinstance(data, dict):
        if value in data:
            __relevance = data[value]
        else:
            for key in data:
                __relevance = get_value(data[key], value)
    elif isinstance(data, list):
        for key in data:
            if isinstance(key, dict):
                __relevance = get_value(key, value)
                break
    return __relevance


def get_unix_time(time_str):
    # time_strp = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')  # 字符串转换为时间对象
    # get_time = datetime.strftime('%Y-%m-%d %H:%M:%S')  # 转换为需要的时间格式
    unix_time = int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))  # 获取Unix时间戳
    # print(unix_time)
    return unix_time


if __name__ == '__main__':
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    today = time.strftime("%Y-%m-%d", time.localtime())
    sevenday = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d %H:%M:%S")
    month = (date.today() + timedelta(days=-29)).strftime("%Y-%m-%d %H:%M:%S")
    day_time = int(time.mktime(datetime.now().date().timetuple()))
    print(day_time)
    get_unix_time(now)
    '''
    昨天 ":1599408000,"   2020-09-07 00:00:00  2020-09-07 23:59:59
    7天 startTime":1598976000,"endTime":1599526809    2020-09-02 00:00:00   2020-09-08 09:00:09 (当前时间)
    '''
