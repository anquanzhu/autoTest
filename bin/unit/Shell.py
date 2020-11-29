# -*- coding: utf-8 -*-
import subprocess

from bin.Yaml import readYaml


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o

    def getV1_auth(self, query):
        # cmd='python2 C:\\python37\\Scripts\\autoTest\\bin\\V1Auth.py %s' %(readYaml('params/auth.yaml')['auth'])
        url = query.split('?')[0]
        params = query.split('?')[1]

        queryString = url + " " + str(params).replace('&', " ")
        # print(queryString)
        cmd = 'python2 C:\\python37\\Scripts\\autoTest\\bin\\V1Auth.py %s' % (queryString)
        print(cmd)
        header = self.invoke(cmd)
        print('header', header)
        return header


if __name__ == '__main__':
    ss = '/cdn/gw/v1/domain/Copy?newDomain=a9.bb.test.com&originDomain=test21e.car.com'
    # Shell().getV1_auth("/cdn/gw/v1/domain/Copy?newDomain=a9.bb.test.com&originDomain=test21e.car.com&ctyunAcctId=ba69d44a5ea847be85ffe3f486f087db")
    Shell().getV1_auth(ss)
