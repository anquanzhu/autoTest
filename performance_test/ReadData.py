# -*- coding: utf-8 -*-
import io
import time

from bin.Workorder import log

request_data = []


def loadRequestData(filePath):
    log.info("开始读取数据")
    file = open(filePath, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line = line.replace("RequestBody:", "").replace("openkey:", "").strip('\n').split(" ")
        request_data.append(line)
    return len(lines)
