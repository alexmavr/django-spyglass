from django.conf.urls import patterns, url, include
from tastypie.api import Api
from api.resources import CrawlerResource
from api.resources import QueryResource
from api.resources import PathsResource
from api.resources import SiteResource

#Tastypie API
v1_api = Api(api_name='spyglass')
v1_api.register(CrawlerResource())
v1_api.register(QueryResource())
v1_api.register(SiteResource())
v1_api.register(PathsResource())


urlpatterns = patterns('',
	url(r'^api/', include(v1_api.urls)),
	url(r'^admin_panel/', 'spyglass.views.admin_panel'),
	url(r'^change/(?P<uid>\d+)/(?P<action>\d)', 'spyglass.views.change_crawlie_access'),
)
