from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^api/$', 'list'),
    url(r'^api/(?P<pk>[0-9]+)/$', 'detail'),
    url(r'^api/test/$', 'test'),
    url(r'^api/is_login/$', 'is_login'),
    url(r'^api/crawl/$', 'crawl'),
    url(r'^api/auth_gateone/$', 'auth_gateone'),
)
