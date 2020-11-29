# _*_ coding: utf-8 _*_


# 删除域名
from bin.unit.Domain import Domain

name = "Domain_Test_6jpM.zhihu.com"
product = "005"

name2 = "Domain_Test_PYQF.zhihu.com"
product2 = "003"

# name为域名名称，product为创建域名时选择的产品类型

Domain().delete_domain(name,product)
Domain().delete_domain(name2,product2)