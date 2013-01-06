from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.landing),
    url(r'^admin/', include(admin.site.urls)),
)
