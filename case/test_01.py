# -*- coding:utf-8 -*-
# 1.先设置编码，utf-8可支持中英文，如上，一般放在第一行

# 2.注释：包括记录创建时间，创建人，项目名称。
'''
Created on 2019-5-30
@author: 杜宏
Project:项目结构设计
'''
# 3.导入模块
import unittest
import requests
import warnings
from case.login import Jenkins
from common.logger import Log


class Test(unittest.TestCase):
    log = Log()
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        s = requests.session()
        self.jenkins = Jenkins(s)

    def test_01_login(self):
        '''登录接口测试用例'''
        self.log.info("--------------start-------------")
        t = self.jenkins.login()
        self.log.info("调用登录结果：%s" % t[0])
        print(t[0])
        result = t[0]
        print(t[1])  # 登录，获取结果
        self.log.info("判断是否登录成功：%s"%result)
        self.assertEqual(result, "admin")  # 拿结果断言
        self.log.info("--------------end-------------")

    def test_02_save(self):
        '''新建和保存任务接口测试用例'''
        # 第一步：登录
        t = self.jenkins.login()
        self.log.info("调用登录结果：%s" % t[0])
        # 第二步：保存
        result = self.jenkins.save(name="北京-宏哥，流程类接口关联1", jname="学习和使用封装与调用--流程类接口关联1")
        self.log.info("调用保存结果：%s"%result)
        print(result)
        # self.assertEqual(result, "admin")  # 拿结果断言

    def test_03_del(self):
        '''删除新建任务接口测试用例'''
        # 第一步：登录
        t = self.jenkins.login()
        self.log.info("调用登录结果：%s" % t[0])
        # 第二步：保存
        body = self.jenkins.save(name="北京-宏哥，流程类接口关联2", jname="学习和使用封装与调用--流程类接口关联2")
        self.log.info("调用保存结果：%s" % body)
        name = body['name']
        Jenkins_Crumb = body['Jenkins-Crumb']
        # pid = self.common.get_postid(r2_url,body="")
        # 第三步：删除
        result = self.jenkins.del_tie(name, Jenkins_Crumb)
        self.log.info("调用删除结果：%s" %result)
        print(result)
        # self.assertEqual(result["isSuccess"], True)  # 拿结果断言


# if __name__ == "__main__":
#     unittest.main()
