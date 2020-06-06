"""Communityparttime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import re_path
from django.views import static

from parttime import views

urlpatterns = [
    re_path('^index/$', views.index),
    re_path('^welcome/$', views.welcome),
    re_path('^adminhome/$', views.AdminHome),
    re_path('^adminAccess/$', views.adminlogin),
    re_path('^adminSingnout/$', views.adminSingnout),
    re_path('^toUpdateAdminPwdPage/$', views.update_admin_pwd),
    re_path('^admin/$', views.Admin),
    re_path('^login/$', views.login),
    re_path('^loginout/$', views.loginout),
    re_path('^register/$', views.register),
    re_path('^allPartTimeUser/$', views.allPartTimeUser),
    re_path('^editUser/$', views.editUser),
    re_path('^toAllUserPage/$', views.toAllUserPage),
    re_path('^allPartTimeUser/$', views.allPartTimeUser),
    re_path('^allJobsPage/$', views.allJobsPage),
    re_path('^allJobs/$', views.allJobs),
    re_path('^upjob/$', views.upjobstat),
    re_path('^downjob/$', views.downjobstat),
    re_path('^deletejob/$', views.deletejob),
    re_path('^addJob/$', views.addJob),
    re_path('^Jobdetails/(?P<Jid>(\w+))$', views.Jobdetails),
    re_path('^personalcenter/$', views.personalcenter),
    re_path('^toUserReleasePage/$', views.toUserReleasePage),
    re_path('^mycolection/$', views.mycolection),
    re_path('^updatepwd/$', views.updatepwd),
    re_path('^findUserRelease/$', views.findUserRelease),
    re_path('^mycolectionlist/$', views.mycolectionlist),
    re_path('^collection_job/$', views.collection_job),
    re_path('^updatejob/$', views.updatejob),
    re_path('^vuetest/$', views.vuetest),
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
