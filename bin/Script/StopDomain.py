# _*_ coding: utf-8 _*_

from bin.unit.Domain import Domain

# 停用域名

name = "Domain_Test_6jpM.zhihu.com"
product = "005"

name2 = "Domain_Test_PYQF.zhihu.com"
product2 = "003"

# name为域名名称，product为创建域名时选择的产品类型

Domain().stop_domain(name,product)
Domain().stop_domain(name2,product2)