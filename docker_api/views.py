#-*- coding: utf-8 -*-
from django.shortcuts import render
import random
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import ContainerDocument
from serializers import ContainerSerializer
import docker
import string

def GenPassword(length):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])#得出的结果中字符会有重复的


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def has_container(request):
    res = {'code':1}
    if request.method == 'POST':
        try:
            c = ContainerDocument.objects.get(user=request.user.username)
            data = ContainerSerializer(c)
            if c:
                res = data.data
                res['code'] = 0
        except:
            pass

    return JSONResponse(res)

@csrf_exempt
def create_container(request):
    res = {'code':1}
    if request.method == 'POST':
    #if True:
        c = ContainerDocument.objects(user=request.user.username).first()
        if c:
            res['msg'] = u'容器已存在'
            return JSONResponse(res)

        try:
            dockerClient = docker.Client(base_url='unix://tmp/docker.sock')
            config = dockerClient.create_host_config(privileged=False, 
                cap_drop=['MKNOD'], 
                mem_limit='100M', 
                memswap_limit='100M', 
                mem_swappiness=90, 
                cpu_period=1000,
                network_mode='guest') 
            
            hostname = 'host_by_%s'%request.user.username
            user = request.user.username
            name = hostname 
            pwd = GenPassword(6)
            container = dockerClient.create_container(
                image='guest',
                hostname=hostname,
                name=name,
                host_config=config,
                entrypoint=['/startup.sh',user,pwd],
            )
            response = dockerClient.start(container=container.get('Id'))

            res['hostname'] = hostname
            res['user'] = user
            res['pwd'] = pwd
            res['code'] = 0  
        except:
            return JSONResponse(res)


        c = ContainerDocument(user=request.user.username,hostname=hostname,pwd=pwd)
        c.save()

        #serializer = GoodsSerializer(data=data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return JSONResponse(serializer.data, status=201)
        #return JSONResponse(serializer.errors, status=400)
    return JSONResponse(res)
