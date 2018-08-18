from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course


# Create your views here.
class OrgView(View):
    '''
    课程机构列表
    '''
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 授课机构排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市
        all_citys = CityDict.objects.all()

        # 机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # name__icontains 表示根据name字段进行搜索，并且不区分大小写
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get("city","")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选机构类别
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get("sort","")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by(r"-students")#倒序排列 升序排序
            elif sort == "courses":
                all_orgs = all_orgs.order_by(r"-course_nums")

        # 机构数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 列表，每页显示数量,request
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request,"org-list.html",{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # ModelForm可以直接将表单数据提交到数据库并保存
            user_ask = userask_form.save(commit=True)
            #返回json，是异步操作
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        is_fav = False
        if request.user.is_authenticated():
            # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):#因为在机构详情页，所以fav_id和fav_type是确定的
                # 判断用户是否收藏
                is_fav = True

        all_courses = course_org.course_set.all()[:3] # 反向获取courses
        all_teachers = course_org.teacher_set.all()[:1] # 反向获取teachers
        return render(request,"org-detail-homepage.html",{
            "org_id": int(org_id),
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "is_fav":is_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):#因为在机构详情页，所以fav_id和fav_type是确定的
                is_fav = True
        all_courses = course_org.course_set.all() # 反向获取courses
        return render(request,"org-detail-course.html",{
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page":current_page,
            "is_fav": is_fav,
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):#因为在机构详情页，所以fav_id和fav_type是确定的
                is_fav = True
        return render(request,"org-detail-desc.html",{
            "course_org":course_org,
            "current_page":current_page,
            "is_fav": is_fav,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self,request,org_id):
        current_page = "org_teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):#因为在机构详情页，所以fav_id和fav_type是确定的
                is_fav = True
        all_teachers = course_org.teacher_set.all() # 反向获取teachers
        return render(request,"org-detail-teachers.html",{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "is_fav": is_fav,
        })


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated():
            # 判断用户登录状态，如果用户还没登录返回json
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        # 判断记录是否存在
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            # 如果记录存在，则用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    讲师列表页
    """
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 教师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # name__icontains 表示根据name字段进行搜索，并且不区分大小写
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))

        # 排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by(r"-click_nums")  # 倒序排列 升序排序

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by(r"-click_nums")[:3]

        # 对讲师进行分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 列表，每页显示数量,request
        # 因为教师比较少，暂时用每页一个教师
        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request,"teachers-list.html",{
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sort":sort,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        has_org_faved = False
        if request.user.is_authenticated():
            # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_faved = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_faved = True

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by(r"-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher":sorted_teacher,
            "has_teacher_faved":has_teacher_faved,
            "has_org_faved":has_org_faved,
        })
