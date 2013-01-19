from tastypie import fields
from tastypie.resources import ModelResource
#from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.validation import Validation
from tastypie.authentication import Authentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from ..models import Crawler
from ..models import Site
from ..models import DataField
from ..models import Query
from ..common import get_meta

class MetaResource(ModelResource):
    class Meta:
        queryset = get_meta().objects.all()
        resource_name = 'meta'
        allowed_methods = ['get','post','patch']

        validation = Validation()
        authentication = Authentication()
        authorization = Authorization()


class SiteResource(ModelResource):
    class Meta:
        queryset = Site.objects.select_related().all()
        resource_name = 'site'
        allowed_methods = ['get']

        validation = Validation()
        authentication = Authentication()
        authorization = Authorization()


class PathsResource(ModelResource):
    site = fields.ForeignKey(SiteResource, 'site', full=False)
    class Meta:
        queryset = DataField.objects.all()
        resource_name = "paths"
        allowed_methods = ['get']
        validation = Validation()
        authentication = Authentication()
        authorization = Authorization()
        fields = ('xpath', 'site', 'field_name')


class QueryResource(ModelResource):
    site = fields.ForeignKey(SiteResource, 'site', full=False)
    result = fields.ForeignKey(MetaResource, 'result', null=True, blank=True,
                               full=False)
    class Meta:
        queryset = Query.objects.order_by('next_check')
        resource_name = 'query'

        llowed_methods = ['get','patch']
        validation = Validation()
        authentication = Authentication()
        authorization = Authorization()

    # Save all objects to update their timestamps before sending them
    def obj_get_list(self, request=None, **kwargs):
        items = super(QueryResource, self).obj_get_list(self, **kwargs)
        for item in items:
            item.save()
        return items


class CrawlerResource(ModelResource):
    class Meta:
        queryset = Crawler.objects.all()
        resource_name = 'crawler'

        allowed_methods = ['get','patch']
        validation = Validation()
        authentication =  Authentication()
        authorization = Authorization()
