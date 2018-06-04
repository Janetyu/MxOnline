# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/1 21:13'
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM

def send_register_email(email,send_type="register"):
    #需要把邮件验证的信息放进数据库，因为用户激活时需要在数据库中查看链接是否存在
    email_record = EmailVerifyRecord()
    random_str = generate_random_str(16)
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #定义邮件内容
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "幕学在线网注册激活链接"
        email_body = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(random_str)

        #参数：subject, message, from_email, recipient_list,
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "幕学在线网密码重置链接"
        email_body = "请点击下面的链接重置您的密码：http://127.0.0.1:8000/reset/{0}".format(random_str)

        # 参数：subject, message, from_email, recipient_list,
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

def generate_random_str(randomlength=8):
    #生成随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str
