# coding=utf-8
# 1.先设置编码，utf-8可支持中英文，如上，一般放在第一行

# 2.注释：包括记录创建时间，创建人，项目名称。
'''
Created on 2019-5-31
@author: 北京-宏哥
Project:学习和使用封装与调用--流程类接口关联
'''
# 3.导入模块
import requests
from common.logger import Log
# 禁用安全请求警告
import urllib3

urllib3.disable_warnings()
import warnings

warnings.simplefilter("ignore", ResourceWarning)


class Jenkins():
    log = Log()

    def __init__(self, s):
        # s = requests.session()  # 全局参数
        self.s = s

    def login(self):
        '''登录接口'''
        url = "http://localhost:8080/jenkins/j_acegi_security_check"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"
        }  # get方法其它加个ser-Agent就可以了
        d = {"j_username": "admin",
             "j_password": "111111",
             "from": "",
             "Submit": u"登录",
             "remember_me": "on"
             }

        s = requests.session()
        r = s.post(url, headers=headers, data=d)
        # print (r.content.decode('utf-8'))
        # 正则表达式提取账号和登录按钮
        import re
        t = re.findall(r'<b>(.+?)</b>', r.content.decode('utf-8'))  # 用python3的这里r.content需要解码
        print(t[0])
        print(t[1])
        return t

    def save(self, name, jname):
        '''保存新建任务：
        参数 1：name # 任务名称
        参数 2：jname # 中文'''
        url1 = "http://localhost:8080/jenkins/createItem"
        body = {"name": "北京-宏哥",
                "mode": "hudson.model.FreeStyleProject",
                "Jenkins-Crumb": "51a97fc7fbf3792823230d9bdd7ec906",
                "json": {"name": "北京-宏哥",
                         "mode": "hudson.model.FreeStyleProject",
                         "Jenkins-Crumb": "51a97fc7fbf3792823230d9bdd7ec906"

                         }
                }
        print(type(body))

        # def get_postid(self, body,url1):
        # 获取name的值
        rname = body['name']
        print('name:' + name)
        # 获取body的值
        rJenkins_Crumb = body['Jenkins-Crumb']
        print('body的值是：', body['Jenkins-Crumb'])
        r2 = self.s.post(url1, data=body, verify=False)
        return body

    def del_tie(self, name, Jenkins_Crumb):
        '''删除新建任务'''
        url2 = "http://localhost:8080/jenkins/job/" + name + "/doDelete"
        print(url2)
        body1 = {
            "Jenkins-Crumb": Jenkins_Crumb
        }

        r3 = self.s.post(url2, data=body1, verify=False)
        # print(r3.content.decode('utf-8'))
        # 删除成功重定向到主界面（由于抓包没有看到response的结果，只知道重定向主界面）
        print(r3.url)
        return r3.url


if __name__ == "__main__":
    s = requests.session()
    Jenkins(s).login()
