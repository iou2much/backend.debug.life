#-*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from django.http import HttpResponseRedirect
from backend import settings
from models import User
#from django.contrib.auth.models import User as DjangoUser
#from urllib.parse import urlencode
import urllib,urllib2,json
from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse  
import time
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Create your views here.

GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK
GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL

# 这里不是很明白
def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFERER', 'https://debug.life/')
    host = 'debug.life'#request.META['HTTP_HOST']
    if refer_url.startswith('http') and host not in refer_url:
        refer_url = 'https://debug.life/'
    return refer_url

# 第一步: 请求github第三方登录
def github_login(request):
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'redirect_uri': GITHUB_CALLBACK,
        'state': _get_refer_url(request),
    }
    #github_auth_url = '%s?%s'%(GITHUB_AUTHORIZE_URL,urllib.parse.urlencode(data))
    github_auth_url = '%s?%s'%(GITHUB_AUTHORIZE_URL,urllib.urlencode(data))
    #print('git_hub_auth_url',github_auth_url)
    return HttpResponseRedirect(github_auth_url)

# github认证处理
def github_auth(request):
    template_html = 'account/login.html'

    # 如果申请登陆页面成功后，就会返回code和state(被坑了好久)
    if 'code' not in request.GET:
        return render(request,template_html)

    code = request.GET.get('code')
    state = request.GET.get('state')
    #print('!!!!!! state :',state)

    # 第二步
    # 将得到的code，通过下面的url请求得到access_token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK,
    }

    data = urllib.urlencode(data)

    # 请求参数需要bytes类型
    binary_data = data.encode('utf-8')
    #print('data:', data)

    # 设置请求返回的数据类型
    headers={'Accept': 'application/json'}
    req = urllib2.Request(url, binary_data,headers)
    #print('req:', req)
    response = urllib2.urlopen(req) 
    #print('response :', response )

    # json是str类型的，将bytes转成str
    result = response.read().decode('ascii')
    result = json.loads(result)
    #print ('result : ',result)
    if 'access_token' not in result:
        return HttpResponseRedirect('error')
    access_token = result['access_token']
    # print('access_token:', access_token)

    url = 'https://api.github.com/user?access_token=%s'%(access_token)
    response = urllib2.urlopen(url)
    html = response.read()
    #html = html.decode('ascii')
    html = html.decode('utf-8')
    print ('resp data:' ,html)
    data = json.loads(html)
    username = data['login']
    email = data['email']
    email = 'no@mail.com'
    print('username:', username)
    password = '94b353683ac6149df67d38ff1d641b40'

    # username not exist ,create it 
    try:
        user1 = User.objects.get(username=username)
    except:
        user2 = User(username=username, password=password)#.insert()
        user2.save()
        DjangoUser = get_user_model()
        try:
            dUser = DjangoUser.objects.get(username=username)
        except:
            djangoUser = DjangoUser.objects.create_user(username, email, password)
            djangoUser.save()

            profile = Profile.objects.create(user=user2)
            profile.save()

    #auth
    user = authenticate(username=username, password=password)
    #print('user',user)
    login(request, user)
    #return HttpResponseRedirect(reverse('/'))
    return HttpResponseRedirect(state)


@csrf_exempt
def log_out(request):
    logout(request)
    res = {'code':0}
    return JSONResponse(res)

