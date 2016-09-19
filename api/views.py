#-*- coding: utf-8 -*-
from django.shortcuts import render
import time, hmac, hashlib, json

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import GoodsDocument
from serializers import GoodsSerializer
import time

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def list(request):
    if request.method == 'GET':
        goods = GoodsDocument.objects.first()
        serializer = GoodsSerializer(goods , many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GoodsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

@csrf_exempt
def test(request):
    if request.method == 'GET':
        res = {'time':time.time()}
        return JSONResponse(res)

@csrf_exempt
def is_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            res = {'code':0,'username':request.user.username}
            return JSONResponse(res)
    res = {'code':1}
    return JSONResponse(res)

@csrf_exempt
def crawl(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            res = {'code':0,'username':request.user.username}
            return JSONResponse(res)
    res = {'code':1}
    return JSONResponse(res)

@csrf_exempt
def auth_gateone(request):
    postData = JSONParser().parse(request)
    if 'username' not in postData:
        username = "guest"
    else:
        username = postData['username']

    secret = "YjlkNjM1OGIxNmQ1NGU2ZDk4NGY5MDJiMmJkNDc1YzNiN"
    authobj = {
        'api_key': "NzkyMGFmZmUwYjU3NDA3NzgyMzNmYjc0Yjk1MmQ3MDk2N",
        'upn': username,
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])
    authobj['signature'] = hash.hexdigest()
    #valid_json_auth_object = json.dumps(authobj)
    return JSONResponse(authobj)
