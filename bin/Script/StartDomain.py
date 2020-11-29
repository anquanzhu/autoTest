# _*_ coding: utf-8 _*_

from bin.unit.Domain import Domain

# 启用域名

# name = "Domain_Test_6jpM.zhihu.com"
# product = "005"

name = "Domain_Test_PYQF.zhihu.com"
product = "003"

# name为域名名称，product为创建域名时选择的产品类型

Domain().start_domain(name,product)