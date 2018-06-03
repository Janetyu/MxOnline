# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/1 13:28'
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    #注意变量名需要跟表单中的name属性相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})
