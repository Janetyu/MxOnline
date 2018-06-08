from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm


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
                all_orgs.order_by(r"-students")#倒序排列 升序排序
            elif sort == "courses":
                all_orgs.order_by(r"-course_nums")

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