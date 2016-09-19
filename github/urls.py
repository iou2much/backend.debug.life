#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from github import views

urlpatterns = patterns('github.views',
    url(r'github/$', views.github_auth,name='github_oauth'),
    url(r'github_login/$', views.github_login, name='github_login'),
    url(r'logout/$', views.log_out,name='logout'),
)
