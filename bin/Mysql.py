# -*- coding: utf-8 -*-

import pymysql
from bin.Init import Init


class DbConnect():
    '''
    数据库连接
    '''

    def __init__(self):

        self.db_cofig = Init.BASE_INFO
        self.info = self.db_cofig['db_info']
        # 连接数据库
        self.db = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, autocommit=True, **self.info)
        # 获取游标
        self.cursor = self.db.cursor()

    def select(self, sql):
        '''
        数据库查询
        :return:
        '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def execute(self, sql):
        '''
        数据库执行：新增，修改，删除
        :param sql:
        :return:
        '''
        try:
            self.cursor.execute(sql)
            # 保存
            self.db.commit()
        except:
            # 回滚
            self.db.rollback()

    def close(self):
        '''
        关闭数据库
        :return:
        '''
        self.db.close()

    '''
        清理自动化产生的域名 （配置中的）
    '''
    def delete_doamin(self, expression):
        db_list = ['cmdb.domain_vendor', 'cmdb.domain_config', 'cmdb.domain_origin_config', 'cmdb.domain_ttl_config',
                   'cmdb.domain_live_config', 'cmdb.domain_header_config']
        for db_name in db_list:
            sql = 'delete from %s where domain_id in (select domain_id from cmdb.domain where %s)' % (
                db_name, expression)
            print(sql)
            r = self.execute(sql)
        sql_domain = 'delete from cmdb.domain where %s ' % (expression)
        self.execute(sql_domain)


if __name__ == '__main__':
    db = DbConnect()
    # db.delete_doamin('client_id=\'14444\' and (domain like \'Auto%\' or domain like \'V1%\')')
    db.delete_doamin('client_id=\'14444\' and (domain = \'www.test101wtddsij1.com\')')
