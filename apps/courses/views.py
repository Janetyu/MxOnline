from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

# Create your views here.
class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")#默认按添加时间进行倒序排列

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]#热门推荐课程

        # 排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by(r"-students")  # 倒序排列 升序排序
            elif sort == "hot":
                all_courses = all_courses.order_by(r"-click_nums")

        # 对课程列表进行分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 列表，每页显示数量,request
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request,"course-list.html",{
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses,
        })
