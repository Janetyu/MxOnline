from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin


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


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息页面
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        # 获取所有课程相关的用户
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出该用户的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request,"course-video.html",{
            "course":course,
            "course_resources":all_resources,
            "relate_courses":relate_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 获取所有课程相关的用户
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出该用户的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses
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