from django.conf.urls import patterns, url

urlpatterns = patterns('docker_api.views',
    #url(r'^api/$', ''),
    #url(r'^api/(?P<pk>[0-9]+)/$', 'detail'),
    #url(r'^api/test/$', 'test'),
    url(r'^docker/create/$', 'create_container'),
    url(r'^docker/has_container/$', 'has_container'),
)
