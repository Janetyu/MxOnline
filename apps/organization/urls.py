# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/8 19:54'

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView

urlpatterns = [

    #课程机构列表页
    url(r'^list/$',OrgView.as_view(),name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
]
