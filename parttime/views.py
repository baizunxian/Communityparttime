import time
import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from parttime.models import PartTimeUser, JobRelation, Jobs, Collection, AdminUser


# Create your views here.

def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'index.html')
    if request.method == "POST":
        page = request.POST.get('pageNum')
        pageSize = request.POST.get('pageSize')
        city_picker = request.POST.get('city_picker')
        Jobname = request.POST.get('Jobname')
        # if city_picker:
        #     province = city_picker.split('/')[0]
        #     city = city_picker.split('/')[1]
        #     area = city_picker.split('/')[2]
        # else:
        #     province = None
        #     city = None
        #     area = None
        start = (int(page) - 1) * int(pageSize)
        end = start + int(pageSize)
        jobs = Jobs.get_jobs(city_picker, Jobname)[start:end]
        jobs_count = Jobs.get_jobs(city_picker, Jobname).count()
        data = list()
        for job in jobs:
            job_dict = dict()
            job_dict['Jid'] = job.Jid
            job_dict['Jobname'] = job.Jobname
            job_dict['Jobloc'] = job.Jobloc
            job_dict['JobSalary'] = job.JobSalary
            job_dict['JobContact'] = job.JobContact
            job_dict['Jobphonenumber'] = job.Jobphonenumber
            job_dict['JobHired'] = job.JobHired
            job_dict['JobDeatails'] = job.JobDeatails
            job_dict['Province_and_city'] = job.Province_and_city
            job_dict['Jobtime'] = job.Jobtime.strftime("%Y-%m-%d %H:%M:%S")
            data.append(job_dict)
        respe = {
            "msg": "success",
            "code": "0",
            "count": jobs_count,
            "data": data
        }
    return JsonResponse(respe)


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if PartTimeUser.objects.filter(PUsername=username).filter(PPassword=password).count() > 0:
            user_id = PartTimeUser.objects.get(PUsername=username).Pid
            request.session['user'] = username
            request.session['user_id'] = user_id
            return JsonResponse('OK', safe=False)
        else:
            return JsonResponse('false', safe=False)


def loginout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['user']
            del request.session['user_id']
        except KeyError as e:
            print(e)
        return redirect('/index/')


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == "POST":
        PUsername = request.POST.get('PUsername')
        PPassword = request.POST.get('PPassword')
        PSex = request.POST.get('PSex')
        PPhoneNumber = request.POST.get('PPhoneNumber')
        PIDCard = request.POST.get('PIDCard')
        PLocation = request.POST.get('PLocation')
        if PartTimeUser.objects.filter(PUsername=PUsername).exists():
            return JsonResponse('False', safe=False)
        else:
            user = PartTimeUser()
            user.PUsername = PUsername
            user.PPassword = PPassword
            user.PSex = PSex
            user.PPhoneNumber = PPhoneNumber
            user.PIDCard = PIDCard
            user.PLocation = PLocation
            user.save()
            return JsonResponse("OK", safe=False)


def welcome(request):
    return render(request, 'welcome.html')


def AdminHome(request):
    return render(request, 'adminhome.html')


def Admin(request):
    return render(request, 'admin.html')


def update_admin_pwd(request):
    """
    管理员修改密码
    :param request:
    :return:
    """
    if request.method == "POST":
        admin_user_id = request.session.get('admin_user_id')
        old_pwd = request.POST.get('oldpwd')
        new_pwd = request.POST.get('newpwd')
        print(new_pwd)
        if old_pwd and new_pwd:
            admin_user_info = AdminUser.objects.get(Aid=admin_user_id)
            if old_pwd == admin_user_info.Apassword:
                admin_user_info.Apassword = new_pwd
                admin_user_info.save()
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('ERROR', safe=False)
        else:
            return JsonResponse('False', safe=False)
    else:
        return render(request, 'updateAdminPwd.html')


def adminSingnout(request):
    """
    管理员退出
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['admin_user']
            del request.session['admin_user_id']
        except KeyError as e:
            print(e)
        return redirect('/index/')


def adminlogin(request):
    """
    管理员登录
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get('username')
        userpwd = request.POST.get('userpwd')
        if username and userpwd:
            admin_user_info = AdminUser.objects.filter(Aname=username).filter(Apassword=userpwd)
            if admin_user_info:
                user_id = AdminUser.objects.get(Aname=username)
                request.session['admin_user'] = user_id.Aname
                request.session['user_id'] = user_id.Aid
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('False', safe=False)
    else:
        return render(request, 'admin.html')


def editUser(request):
    return render(request, 'editUser.html')


def Jobdetails(request, Jid):
    job_detail = Jobs.objects.get(Jid=Jid)
    user_id = request.session.get('user_id')
    if Collection.objects.filter(FJobFav_id=user_id, Jid_id=Jid):
        collection_start = '1'
    else:
        collection_start = '0'
    return render(request, 'jobdetails.html', {'job_detail': job_detail, 'collection_start': collection_start})


def toAllUserPage(request):
    return render(request, 'allPartTimeUser.html')


def allPartTimeUser(request):
    """
    获取所有用户
    """
    if request.method == "GET":
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        start = (int(page) - 1) * int(limit)
        end = start + int(limit)
        user_list = PartTimeUser.objects.all()[start:end]
        user_list_count = PartTimeUser.objects.all().count()
        data = list()
        for user in user_list:
            user_dict = dict()
            user_dict['Pid'] = user.Pid
            user_dict['PUsername'] = user.PUsername
            user_dict['PPassword'] = user.PPassword
            user_dict['PSex'] = user.PSex
            user_dict['PPhoneNumber'] = user.PPhoneNumber
            user_dict['PIDCard'] = user.PIDCard
            user_dict['PLocation'] = user.PLocation
            data.append(user_dict)
        respe = {
            "msg": "success",
            "code": "0",
            "count": user_list_count,
            "data": data
        }
        return JsonResponse(respe)


def allJobsPage(request):
    return render(request, 'allJobsPage.html')


def allJobs(request):
    """
    获取所有job
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    jobs = Jobs.objects.all()[start:end]
    jobs_count = Jobs.objects.all().count()
    data = list()
    for job in jobs:
        job_dict = dict()
        job_dict['Jid'] = job.Jid
        job_dict['Jobname'] = job.Jobname
        job_dict['Jobloc'] = job.Jobloc
        job_dict['JobSalary'] = job.JobSalary
        job_dict['JobContact'] = job.JobContact
        job_dict['Jobphonenumber'] = job.Jobphonenumber
        job_dict['Province_and_city'] = job.Province_and_city
        job_dict['JobHired'] = job.JobHired
        job_dict['JobDeatails'] = job.JobDeatails
        job_dict['Jobtime'] = job.Jobtime.strftime("%Y-%m-%d %H:%M:%S")
        data.append(job_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": jobs_count,
        "data": data
    }
    return JsonResponse(respe)


def upjobstat(request):
    """
    更新job状态，为生效状态
    :param request:
    :return:
    """
    if request.method == "POST":
        Jid = request.POST.get('Jid')
        job = Jobs.objects.get(Jid=Jid)
        if job.JobHired == '0':
            return JsonResponse('FALSE', safe=False)
        else:
            job.JobHired = '0'
            job.save()
            return JsonResponse('OK', safe=False)


def downjobstat(request):
    """
    更新job状态，为失效状态
    :param request:
    :return:
    """
    if request.method == "POST":
        Jid = request.POST.get('Jid')
        job = Jobs.objects.get(Jid=Jid)
        if job.JobHired == '1':
            return JsonResponse('FALSE', safe=False)
        else:
            job.JobHired = '1'
            job.save()
            return JsonResponse('OK', safe=False)


def deletejob(request):
    """
    删除job
    :param request:
    :return:
    """
    if request.method == "POST":
        Jid = request.POST.get('Jid')
        Jobs.objects.get(Jid=Jid).delete()
        return JsonResponse("OK", safe=False)


def addJob(request):
    """
    添加job
    :param request:
    :return:
    """
    if request.method == "POST":
        Jobname = request.POST.get('Jobname', '')
        Jobloc = request.POST.get('Jobloc', '')
        JobSalary = request.POST.get('JobSalary', '')
        JobContact = request.POST.get('JobContact', '')
        Jobphonenumber = request.POST.get('Jobphonenumber', '')
        JobDeatails = request.POST.get('JobDeatails', '')
        user_id = request.POST.get('user_id')
        city_picker = request.POST.get('city-picker', None)
        Jobs.objects.create(
            Jobname=Jobname,
            Jobloc=Jobloc,
            JobSalary=JobSalary,
            JobContact=JobContact,
            Jobphonenumber=Jobphonenumber,
            JobDeatails=JobDeatails,
            Puser_id=user_id,
            Province_and_city=city_picker,
        )
        return JsonResponse('OK', safe=False)
    else:
        return render(request, 'addJob.html')


def personalcenter(request):
    return render(request, 'customer.html')


def toUserReleasePage(request):
    return render(request, 'mypelease.html')


def mycolection(request):
    return render(request, 'mycolection.html')


def updatepwd(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        old_pwd = request.POST.get('oldPwd')
        new_pwd = request.POST.get('newPwd')
        print(new_pwd)
        if old_pwd and new_pwd:
            user_info = PartTimeUser.objects.get(Pid=user_id)
            if old_pwd == user_info.PPassword:
                user_info.PPassword = new_pwd
                user_info.save()
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('False', safe=False)
        else:
            return JsonResponse('False', safe=False)
    else:
        return render(request, 'updatepwd.html')


def findUserRelease(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    user_id = request.session.get('user_id')
    user_jobs = Jobs.objects.filter(Puser_id=user_id)[start:end]
    job_count = Jobs.objects.filter(Puser_id=user_id).count()
    data = list()
    for job in user_jobs:
        job_dict = dict()
        job_dict['Jid'] = job.Jid
        job_dict['Jobname'] = job.Jobname
        job_dict['Jobloc'] = job.Jobloc
        job_dict['JobSalary'] = job.JobSalary
        job_dict['JobContact'] = job.JobContact
        job_dict['Jobphonenumber'] = job.Jobphonenumber
        job_dict['JobHired'] = job.JobHired
        job_dict['Province_and_city'] = job.Province_and_city
        job_dict['JobDeatails'] = job.JobDeatails
        job_dict['Jobtime'] = job.Jobtime.strftime("%Y-%m-%d %H:%M:%S")
        job_dict['Puser'] = job.Puser.PUsername
        data.append(job_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": job_count,
        "data": data
    }
    return JsonResponse(respe)


def mycolectionlist(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    user_id = request.session.get('user_id')
    user_colection = Collection.objects.filter(FJobFav=user_id)[start:end]
    user_colection_count = Collection.objects.filter(FJobFav=user_id).count()
    data = list()
    for job in user_colection:
        job_dict = dict()
        job_dict['Jid'] = job.Jid.Jid
        job_dict['Jobname'] = job.Jid.Jobname
        job_dict['Jobloc'] = job.Jid.Jobloc
        job_dict['JobSalary'] = job.Jid.JobSalary
        job_dict['Province_and_city'] = job.Jid.Province_and_city
        job_dict['JobContact'] = job.Jid.JobContact
        job_dict['Jobphonenumber'] = job.Jid.Jobphonenumber
        job_dict['JobHired'] = job.Jid.JobHired
        job_dict['JobDeatails'] = job.Jid.JobDeatails
        job_dict['Jobtime'] = job.Jid.Jobtime.strftime("%Y-%m-%d %H:%M:%S")
        job_dict['Puser'] = job.Jid.Puser.PUsername
        data.append(job_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": user_colection_count,
        "data": data
    }
    return JsonResponse(respe)


def collection_job(request):
    """
    收藏，取消收藏 job
    collection_start 1 :收藏
    collection_start 0 :未收藏
    :param request:
    :return:
    """
    user_id = request.session.get("user_id")
    job_id = request.POST.get('Jid')
    collection_start = Collection.objects.filter(FJobFav_id=user_id, Jid_id=job_id)
    collection = Collection()
    if collection_start:
        Collection.objects.filter(FJobFav_id=user_id, Jid_id=job_id).delete()
        data = {
            'code': 0,
            'msg': '取消收藏成功！',
            'state': '0'
        }
        return JsonResponse(data)
    else:
        collection.FJobFav_id = user_id
        collection.Jid_id = job_id
        collection.save()
        data = {
            'code': 0,
            'msg': '收藏成功！',
            'state': '1'
        }
        return JsonResponse(data)


def updatejob(request):
    if request.method == "POST":
        print(request.POST)
        Jid = request.POST.get('Jid')
        Jobname = request.POST.get('Jobname')
        Jobloc = request.POST.get('Jobloc')
        city_picker = request.POST.get('city-picker')
        Jobphonenumber = request.POST.get('Jobphonenumber')
        JobDeatails = request.POST.get('JobDeatails')
        JobSalary = request.POST.get('JobSalary')
        JobContact = request.POST.get('JobContact')
        job = Jobs.objects.get(Jid=Jid)
        job.Jobname = Jobname
        job.Jobloc = Jobloc
        job.Province_and_city = city_picker
        job.Jobphonenumber = Jobphonenumber
        job.JobDeatails = JobDeatails
        job.JobSalary = JobSalary
        job.JobContact = JobContact
        job.save()
        return JsonResponse("OK", safe=False)
    else:
        Jid = request.GET.get('Jid')
        job_info = Jobs.objects.get(Jid=Jid)
        return render(request, 'updatejob.html', {"job_info": job_info})


def vuetest(request):
    jobs = Jobs.objects.all()
    return render(request, 'vuetest.html', {"jobs":jobs})
