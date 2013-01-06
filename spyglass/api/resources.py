from tastypie import fields
from tastypie.resources import ModelResource
#from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.validation import Validation
from tastypie.authentication import Authentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from spyglass.models import Crawler
from spyglass.models import Site
from spyglass.models import DataField
from spyglass.models import Query

from django.conf import settings

def get_meta():
    package = ".".join(settings.METAMODEL.split('.')[:-1])
    modelclass = settings.METAMODEL.split('.')[-1]
    Metamodel = __import__(package, globals(),locals(), [modelclass], -1)
    Metamodel = eval("Metamodel." + modelclass)
    return Metamodel

Metamodel = get_meta()

class MetaResource(ModelResource):
    class Meta:
        queryset = Metamodel.objects.all()
        resource_name = 'meta'
        allowed_methods = ['get','post']

        validation = Validation()
        authentication = Authentication()
        authorization = DjangoAuthorization()


class SiteResource(ModelResource):
    class Meta:
        queryset = Site.objects.all()
        resource_name = 'site'
        allowed_methods = ['get']

        validation = Validation()
        authentication = Authentication()
        authorization = DjangoAuthorization()


class PathsResource(ModelResource):
    site = fields.ForeignKey(SiteResource, 'site', full=False)
    class Meta:
        queryset = DataField.objects.all()
        resource_name = "paths"
        allowed_methods = ['get']
        validation = Validation()
        authentication = Authentication()
        authorization = DjangoAuthorization()


class QueryResource(ModelResource):
    site = fields.ForeignKey(SiteResource, 'site', full=False)
    class Meta:
        queryset = Query.objects.order_by('next_check')
        resource_name = 'query'

        allowed_methods = ['get','patch']
        validation = Validation()
        authentication = Authentication()
        authorization = DjangoAuthorization()

class CrawlerResource(ModelResource):
    class Meta:
        queryset = Crawler.objects.all()
        resource_name = 'crawler'

        allowed_methods = ['get','patch']
        validation = Validation()
        authentication =  Authentication()
        authorization = DjangoAuthorization()
