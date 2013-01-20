from django.conf.urls import patterns, include, url
from django.contrib import admin
import spyglass.urls
admin.autodiscover()

from core.views import user_input
from spyglass.views import receive_query

urlpatterns = patterns('',
    url(r'^$', user_input),
    url(r'^receive_query/$', receive_query),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(spyglass.urls)),
)
