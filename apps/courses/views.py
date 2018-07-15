from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments

# Create your views here.
class CourseListView(View):
    """
    课程列表页
    """
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

class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request,"course-detail.html",{
            "course":course,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org
        })


class CourseInfoView(View):
    """
    课程章节信息页面
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        return render(request,"course-video.html",{
            "course":course,
            "course_resources":all_resources,
        })


class CourseCommentView(View):
    """
    课程评论页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self,request):
        if not request.user.is_authenticated():
            # 判断用户登录状态，如果用户还没登录返回json
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id",0) #如果值为空，则默认值为0
        comments = request.POST.get("comments","")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            #get方法只能取出一条数据，如果没有数据则会抛出异常，filter方法则会返回一个数组，若无值，则返回一个空数组，而不会抛异常
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')