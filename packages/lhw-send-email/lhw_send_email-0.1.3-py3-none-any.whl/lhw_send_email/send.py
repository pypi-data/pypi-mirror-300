'''
encoding:   -*- coding: utf-8 -*-
@Time           :  2024/9/24 13:32
@Project_Name   :  All_Learning
@Author         :  lhw
@File_Name      :  send.py

功能描述

实现步骤

'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, parseaddr



class SendEmail:
    def __init__(self, fromEmailAddress: str, password: str, destination: list[str], content: str, subject: str,
                 api: str = None, isAtt: bool = False, att_paths: list[str] = None):
        """
        :param fromEmailAddress: 格式 "Name <example@qq.com>"  <>中是邮件服务器(地址)-也可以是qq邮箱地址
        :param password: 邮箱授权码
        :param destination: 格式 "example@qq.com"  邮箱地址,不一定为qq邮箱
        :param content: 内容
        :param subject: 邮件标题
        :param api: 邮件服务器地址(默认为smtp.qq.com)
        :param isAtt: 是否携带附件(默认False,如果为True,则需要更改att_paths参数的内容)
        :param att_paths: 附件的路径
        """

        self.name, self.address = parseaddr(fromEmailAddress)
        self.fromEmailAddress = self.address
        self.password = password
        self.destination = destination
        self.content = content
        self.subject = subject
        self.api = 'smtp.qq.com'

        if api is None:
            self.api = "smtp.qq.com"
        else:
            self.api = api

        self.msg = MIMEMultipart()  # 实例化一个Multipart

        # 添加基本信息
        self.msg['From'] = self._format_addr()
        self.msg['To'] = self.destination[0]  # 接收者邮件地址
        self.msg['Subject'] = self.subject  # 邮件标题

        print('msg:\n', self.msg)

        self.msg.attach(MIMEText(content, 'plain', 'utf-8'))  # 添加一个纯文本

        # 是否携带附件
        if isAtt:
            self.att_paths = att_paths
            for att in att_paths:
                attachment = MIMEText(open(att, 'rb').read(), 'base64', 'utf-8')
                attachment['Content-type'] = 'application/octet-stream'
                attachment['Content-Disposition'] = f'attachment;filename={att.split("/")[-1]}'
                self.msg.attach(attachment)



    def _format_addr(self):
        return formataddr((self.name, self.address))

    def send(self):
        # try:
        # 初始化,建立SMTP,SSL的链接,链接发送方的服务器
        smtp = smtplib.SMTP_SSL(self.api, 465)

        # 登录发送方的邮箱
        smtp.login(self.fromEmailAddress, self.password)

        # 发送
        smtp.sendmail(self.fromEmailAddress, self.destination, self.msg.as_string())

        smtp.quit()

        print(f'发送成功!\n发送邮箱:{self.fromEmailAddress}\n目标邮箱:{self.destination[0]}')
        return f'发送成功!\n发送邮箱:{self.fromEmailAddress}\n目标邮箱:{self.destination[0]}'
# except Exception as e:
#     print(e)
#     return f'发送失败:\n{e}'
