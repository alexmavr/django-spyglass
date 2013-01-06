from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.validation import Validation
from tastypie.authentication import Authentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from core.models import *

class CrawlerResource(ModelResource):
    class Meta:
        queryset = QueryRequest.objects.filter(link=None).order_by('date')
        resource_name = 'query'    
        excludes = ['email']

        allowed_methods = ['get','patch']
        validation = Validation()            # change to FormValidation
        authentication =  ApiKeyAuthentication()    
        authorization = DjangoAuthorization()

        filtering = {
                'id': ALL,
        }

class MetaResource(ModelResource):
    queryrequest = fields.ForeignKey(CrawlerResource,'queryrequest',full=True)
    class Meta:
        queryset = RequestMeta.objects.filter(queryrequest__link=None).order_by('queryrequest__date')
        resource_name = 'meta'    
        allowed_methods = ['get','patch']

        validation = Validation()            # change to FormValidation
        authentication = ApiKeyAuthentication()    
        authorization = DjangoAuthorization()

        filtering = {
                'queryrequest': ALL_WITH_RELATIONS,
        }


#Used in BacmanResource, does it need removal?
class CrawlerMailResource(ModelResource):
    class Meta:
        queryset = QueryRequest.objects.order_by('date')
        resource_name = 'querymail'    

        allowed_methods = ['get','patch']
        validation = Validation()            # change to FormValidation
        authentication =  ApiKeyAuthentication()    
        authorization = DjangoAuthorization()

        filtering = {
                'id': ALL,
        }


class BacmanResource(ModelResource):
    queryrequest = fields.ForeignKey(CrawlerMailResource,'queryrequest',full=True)
    class Meta:
        queryset = FinishedLink.objects.filter(checked=False).order_by('queryrequest__date')
        resource_name = 'bacman'    
        allowed_methods = ['get','patch']

        validation = Validation()            
        authentication =  ApiKeyAuthentication()    
        authorization = DjangoAuthorization()
        
class CrawlerControlResource(ModelResource):
    class Meta:
        queryset = CrawlerControl.objects.all()
        resource_name = 'control'    
        allowed_methods = ['get','patch']
        excludes = ['api_key']
        include_resource_uri = False
        validation = Validation()            
        authentication =  ApiKeyAuthentication()    
        authorization = DjangoAuthorization()
