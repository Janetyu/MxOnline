# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'Janet'
__date__ = '2018/7/16 0:12'

class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)