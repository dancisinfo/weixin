from django.conf.urls import patterns, include, url

from django.contrib import admin
from zhengqian.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zhengqian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^access$',access),
	url(r'^point$',rec_point),
	url(r'^weixin$',weixin),
	url(r'^pay$',pay),
)
