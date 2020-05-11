# -*- coding:utf-8 -*-
# 1.先设置编码，utf-8可支持中英文，如上，一般放在第一行

# 2.注释：包括记录创建时间，创建人，项目名称。
'''
Created on 2019-5-31
@author: 杜宏
Project:项目结构设计
'''
# 3.导入模块
import os
import codecs
import configparser

cur_path  = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(cur_path, "cfg.ini")
conf = configparser.ConfigParser()
conf.read(configPath,encoding="utf-8")

smpt_server = conf.get("email", "smtp_server")
port = conf.get("email", "port")
sender = conf.get("email", "sender")
psw = conf.get("email", "psw")
receiver = conf.get("email", "receiver")

