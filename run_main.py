# -*- coding:utf-8 -*-
# 1.先设置编码，utf-8可支持中英文，如上，一般放在第一行

# 2.注释：包括记录创建时间，创建人，项目名称。
'''
Created on 2019-5-30
@author: 杜宏
Project:项目结构设计
'''
# 3.导入模块
import os
import unittest
import time
import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# 当前脚本所在文件的真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))


def add_case(caseName="case", rule="test*.py"):
    '''第一步：加载所有测试用例'''
    case_path = os.path.join(cur_path, caseName)  # 用例文件夹
    # 如果不存在这个case文件夹，就自动创建一个
    if not os.path.exists(case_path):
        os.mkdir(case_path)
    print("test case path:%s" % case_path)
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    print(discover)
    return discover


def run_case(all_case, reportName="report"):
    '''第二步：执行所有用例，并把所有结果写入HTML测试报告'''
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, reportName)  # 报告文件夹
    # 如果不存在这个report文件夹，就自动创建一个
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    report_abspath = os.path.join(report_path, now + "result.html")
    print("test report path:%s" % report_abspath)
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="自动化测试报告", description="用例执行情况")
    # 调用add_case函数fanhuiozh
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u"最新生成的测试报告：" + lists[-1])
    # 找到最新的测试报告
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_email(sender, psw, receiver, smtpserver, report_file, port):
    '''第四步：发送最新的测试报告'''
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg["Subject"] = "测试报告"
    msg["from"] = sender
    msg["to"] = receiver
    msg.attach(body)
    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="TestReport.html"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
    msg.attach(att)
    try:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
    except:
        smtp = smtplib.SMTP
        smtp.connect(smtpserver, port)
    # 用户名、密码
    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver.split(','), msg.as_string())
    smtp.quit()
    print("test report email has send out !")


if __name__ == "__main__":
    all_case = add_case()  # 1、加载所有用例
    # 生成测试报告路径
    run_case(all_case)  # 2、执行用例
    # 获取最新的测试报告
    report_path = os.path.join(cur_path, "report")  # 报告文件夹
    report_file = get_report_file(report_path)  # 3、获取最新的测试报告
    # 邮箱配置
    from config import readconfig

    smtp_server = readconfig.smpt_server
    port = readconfig.port
    sender = readconfig.sender
    psw = readconfig.psw
    receiver = (readconfig.receiver)
    send_email(sender, psw, receiver, smtp_server, report_file, port) #4、最后发送邮件
