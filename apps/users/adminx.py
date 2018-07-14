# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/5/19 1:07'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner
from .models import UserProfile


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    #全局标题配置
    site_title = "幕学后台管理系统"
    site_footer = "幕学在线网"
    #导航栏收起的效果
    menu_style = "accordion"


# class UserProfileAdmin(object):
    # list_display = ['username','email','first_name','last_name','is_staff']
    # search_fields = ['username','email','first_name','last_name','is_staff']
    # list_filter = ['username','email','first_name','last_name','is_staff']


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index',]
    list_filter = ['title','image','url','index','add_time']


# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)