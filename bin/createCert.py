# -*- coding: utf-8 -*-
from bin.GetSuite import read
from bin.unit.Rondom import random_string


def generate_cert(workspaceid):
    public_key = read('/params/cdn/server.crt')
    private_key = read('/params/cdn/server_private.key')
    certName = 'Auto_Cert_' + random_string(6)
    certinfo = {
        "data": {
            "workspaceId": workspaceid,
            "name": certName,
            "certs": public_key,
            "key": private_key,
            "email": "286036139@qq.com"
        }
    }
    return certinfo


if __name__ == '__main__':
    print(generate_cert('100385'))
