# -*- coding:utf-8 -*-
__author__ = 'Janet'
__date__ = '2018/6/11 0:11'

from django.conf.urls import url,include

from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView

urlpatterns = [

    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name="course_list"),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name="course_detail"),

    # 课程章节信息页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),

    # 添加课程评论页
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),
]
