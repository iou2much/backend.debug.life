from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^api/$', 'list'),
    url(r'^api/(?P<pk>[0-9]+)/$', 'detail'),
    url(r'^api/test/$', 'test'),
)
