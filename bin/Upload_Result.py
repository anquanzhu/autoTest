import json
import os

import requests
from bin.Init import Init

file_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
headers_json = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/json",
}


class Upload_Result():

    def __init__(self):
        self.result_info = {}
        self.temp = []
        self.base_info = Init.BASE_INFO
        self.planId = self.base_info['planId']

    def update_result(self, id, ispass):
        info = {}
        info['id'] = id
        info['ispass'] = ispass
        # result['planId'] = 238496
        if ispass == 1:
            info['resultinfo'] = '测试通过'
        else:
            info['resultinfo'] = '测试不通过'
        self.temp.append(info)
        # if self.result_info == {}:
        #     self.result_info['caseResultInfo'] = info
        if id not in self.result_info:
            self.result_info['caseResultInfo'] = self.temp
            # result['caseResultInfo'] = temp
        # print(self.result_info)
        self.result_info['planId'] = self.planId
        return self.result_info

    """
    {
"planId" : 8394,
"caseResultInfo" : [{
    "id": 8621, 
    "ispass": 1, 
    "resultinfo": "测试通过" 
},
{
    "id": 123, 
    "ispass": 1, 
    "resultinfo": "测试通过" 
},
{
    "id": 8495, 
    "ispass": 0, 
    "resultinfo": "测试不通过" 
},
    {
    "id": 1234, 
    "ispass": 1, 
    "resultinfo": "测试通过" 
}
]
}
    
    """

    def get_allure_report(self):
        """
        "passed","vip_console.test_vip_refresh.Test_Vip_Refresh#test_CDN_240873","176",""
        :return:
        """
        self.result_info['planId'] = self.planId
        # self.result_info['caseResultInfo'] = self.temp
        info = {}
        # report_data=readJson("report/html/data/suites.csv")
        f = open(file_path + "/report/html/data/suites.csv", 'r', encoding='utf-8')  # 返回一个文件对象
        # print(f)
        for line in f:
            if 'Duration' not in line and 'test_CDN' in line:
                ispass = str(line).split(",")[0].replace('"', '')
                case_name = str(line).split(",")[1].replace('"', '').split("#")
                id = case_name[-1].replace("test_CDN_", "")
                info['id'] = int(id)
                # else:
                #     info['id'] = '100000'
                if ispass == "passed":
                    pass_number = 1
                    info['ispass'] = pass_number
                    info['resultinfo'] = "测试通过"
                elif ispass == "failed":
                    pass_number = 0
                    info['ispass'] = pass_number
                    info['resultinfo'] = "测试不通过"
                else:
                    pass_number = 2
                    info['ispass'] = pass_number
                    info['resultinfo'] = "测试skipped"
                self.temp.append(info)
                info={}
        self.result_info['caseResultInfo'] = self.temp
        print("推送结果： ", self.result_info)
        response = requests.post('https://36.111.140.76:8443/automatedTest/updateCaseResult',
                                 json.dumps(self.result_info),
                                 headers=headers_json,
                                 verify=False)
        print(response.text)
        f.close()


if __name__ == '__main__':
    Upload_Result().get_allure_report()
