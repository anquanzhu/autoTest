"""
    提供一种快速对接口进行性能测试的方法以及结果收集
    1. 用ab 压测，抽离结果并记录 （ab 的压测能力不如wrk， 但是wrk 3年+没更新了，ab的请求准确率（即用户请求数/实际发起用户数 的偏差）高于wrk）
       文档参考 /doc/Apache Bench.md
       locust(python)
    2. 自己使用python的多线程+锁+request 执行压测 （可以收集更多的结果，但是性能压测能力不强）

"""

import os
import subprocess
import time

import xlwt
import xlrd

file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
timestamp = str(time.time() // 300 * 300).split('.')[0]
ip = 'http://www.baidu.com'

# 创建excel,并写入标题
workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet("CDN_API", cell_overwrite_ok=True)
worksheet.write(0, 0, label='请求接口')
worksheet.write(0, 1, label='请求数')
worksheet.write(0, 2, label='失败数')
worksheet.write(0, 3, label='并发数')
worksheet.write(0, 4, label='用户TPS(ms)')
worksheet.write(0, 5, label='服务器TPS(ms)')
worksheet.write(0, 6, label='95%的响应时间(ms)')
worksheet.write(0, 7, label='吞吐率(个/s)')
worksheet.write(0, 8, label='响应数据长度总和')
worksheet.write(0, 9, label='正文数据的总和')

# 追加到xls中
'''
excel = xlrd.open_workbook("E:\\QJBZ\\76.xls")
#获得当前行数
sheet = excel.sheet_by_index(0)
oldrows= sheet.nrows
#创建新的workbook
workbook = copy(excel)
worksheet = workbook.get_sheet(0)
'''

# html_path = file_path + '/report/performance_report/ab.xls'
# 如果是新创建的文档，则current为1，否则就读取之前文档的最后一行
currentrows = 1
for i in range(1, 2):
    # myres = os.popen("ab -n 1000 -c " + str(i) + " " + ip + "/path").readlines()
    cmd = "ab -n 10 -c " + str(i) + " " + ip + "/path"
    print(cmd)
    output = subprocess.Popen(cmd, shell=True,
                              cwd='C:\\python37\\Scripts\\httpd-2.4.46-win32-VS16\\Apache24\\bin',
                              stdout=subprocess.PIPE)
    temp = output.stdout.readlines()
    print(temp)
    myres = []
    for items in temp:
        myres.append(items.decode('utf-8'))
    # print(myres)
    # print(myres[16], myres[17], myres[14], myres[22],myres[23], myres[39], myres[21])
    print('--------------------------------------------------')
    print(myres[8], myres[9], myres[16], myres[17], myres[14], myres[22],myres[23], myres[39], myres[21],myres[19], myres[20])
    # 对应项写入excel中
    comreq = myres[16].split(":")[1]
    worksheet.write(currentrows + i - 1, 0, label=comreq)
    failreq = myres[17].split(":")[1]
    worksheet.write(currentrows + i - 1, 1, label=failreq)
    conlevel = myres[14].split(":")[1]
    worksheet.write(currentrows + i - 1, 2, label=conlevel)
    tps = myres[23].split(":")[1]
    tps = tps.split("[")[0]
    worksheet.write(currentrows + i - 1, 3, label=tps)
    responsetime = filter(None, myres[39].split(" "))
    worksheet.write(currentrows + i - 1, 4, list(responsetime)[1])
    rps = myres[21].split(":")[1]
    rps = rps.split("[")[0]
    worksheet.write(currentrows + i - 1, 5, label=rps)

workbook_path = file_path + '/report/performance_report/CDN_CONSOLE_' + timestamp + '.xls'

workbook.save(workbook_path)
