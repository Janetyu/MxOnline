# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/1 13:28'
from django import forms


class LoginForm(forms.Form):
    #注意变量名需要跟表单中的name属性相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)