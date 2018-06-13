# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/11 0:11'

from django.conf.urls import url,include

from .views import CourseListView

urlpatterns = [

    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name="course_list"),

]
